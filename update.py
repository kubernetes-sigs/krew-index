import json
import os
import re
import requests
import shutil
import git

GithubRepo = "apecloud/kbcli"
kbcliTmpl = """apiVersion: krew.googlecontainertools.github.com/v1alpha2
kind: Plugin
metadata:
  name: kb
spec:
  homepage: https://github.com/apecloud/kbcli
  shortDescription: A Command Line Interface for KubeBlocks
  version: {version}
  description: |
    KubeBlocks is an open-source, cloud-native data infrastructure 
    designed to help application developers and platform engineers 
    manage database and analytical workloads on Kubernetes. 
    It is cloud-neutral and supports multiple cloud service providers, 
    offering a unified and declarative approach to increase productivity 
    in DevOps practices. kbcli is a command line interface for KubeBlocks.
  platforms:
  - selector:
      matchLabels:
        os: darwin
        arch: amd64
    uri: https://github.com/apecloud/kbcli/releases/download/{version}/kbcli-darwin-amd64-{version}.tar.gz
    sha256: {darwin_amd64_sha256}
    bin: kbcli
    files:
    - from: darwin-amd64/kbcli
      to: .
  - selector:
      matchLabels:
        os: darwin
        arch: arm64
    uri: https://github.com/apecloud/kbcli/releases/download/{version}/kbcli-darwin-arm64-{version}.tar.gz
    sha256: {darwin_arm64_sha256}
    bin: kbcli
    files:
    - from: darwin-arm64/kbcli
      to: .
  - selector:
      matchLabels:
        os: linux
        arch: amd64
    uri: https://github.com/apecloud/kbcli/releases/download/{version}/kbcli-linux-amd64-{version}.tar.gz
    sha256: {linux_amd64_sha256}
    bin: kbcli
    files:
    - from: linux-amd64/kbcli
      to: .
  - selector:
      matchLabels:
        os: linux
        arch: arm64
    uri: https://github.com/apecloud/kbcli/releases/download/{version}/kbcli-linux-arm64-{version}.tar.gz
    sha256: {linux_arm64_sha256}
    bin: kbcli
    files:
    - from: linux-arm64/kbcli
      to: .
  - selector:
      matchLabels:
        os: windows
        arch: amd64
    uri: https://github.com/apecloud/kbcli/releases/download/{version}/kbcli-windows-amd64-{version}.zip
    sha256: {windows_amd64_sha256}
    bin: kbcli.exe
    files:
    - from: windows-amd64/kbcli.exe
      to: .
"""

def get_download_url_and_version(repo):
    url = f'https://api.github.com/repos/{repo}/releases/latest'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if 'tag_name' in data:
            tag_name = data['tag_name']
            filtered_urls = []
            if 'assets' in data and len(data['assets']) > 0:
                assets = data['assets']
                for asset in assets:
                    browser_download_url = asset['browser_download_url']
                    filtered_urls.append(browser_download_url)

            return filtered_urls, tag_name
        else:
            print('No tag name found.')
    else:
        print('Error:', response.status_code)

    return None, None

if __name__ == "__main__":
    urls, version = get_download_url_and_version(GithubRepo)
    darwin_amd64_sha256 = ""
    darwin_arm64_sha256 = ""
    linux_amd64_sha256 = ""
    linux_arm64_sha256 = ""
    windows_amd64_sha256 = ""
    for url in urls:
        # download file and get sha256
        filename = url.split('/')[-1]
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # save file
            with open(filename, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            # get sha256 according platform
            # sha256 = os.popen(f'sha256sum {filename}').read().split(' ')[0]
            sha256 = os.popen(f'shasum -a 256 {filename}').read().split(' ')[0]
            # check sha256
            if sha256 == '':
                print('Error: sha256 is empty.')
                exit(1)

            # set sha256 according to filename
            if 'darwin-amd64' in filename:
                darwin_amd64_sha256 = sha256
            elif 'darwin-arm64' in filename:
                darwin_arm64_sha256 = sha256
            elif 'linux-amd64' in filename:
                linux_amd64_sha256 = sha256
            elif 'linux-arm64' in filename:
                linux_arm64_sha256 = sha256
            elif 'windows-amd64' in filename:
                windows_amd64_sha256 = sha256
            # remove file
            os.remove(filename)
        else:
            print('Error:', response.status_code)
            exit(1)
    # generate kbcli.yaml
    kbcli = kbcliTmpl.format(version=version, 
                             darwin_amd64_sha256=darwin_amd64_sha256, 
                             darwin_arm64_sha256=darwin_arm64_sha256, 
                             linux_amd64_sha256=linux_amd64_sha256, 
                             linux_arm64_sha256=linux_arm64_sha256, 
                             windows_amd64_sha256=windows_amd64_sha256)
    with open('kb.yaml', 'w') as f:
        f.write(kbcli)
    
    # clone repo
    github_repo = os.environ.get('GITHUB_REPOSITORY')
    github_token = os.environ.get('GITHUB_TOKEN')
    github_user = github_repo.split('/')[0]
    github_repo_name = github_repo.split('/')[1]

    # check github_token
    if github_token == '':
        print('Error: github_token is empty.')
        exit(1)

    git_repo = git.Repo.clone_from(
                'https://{}@github.com/{}.git'.format(github_token, github_repo),
                github_repo_name,
    )
    git_refs = git_repo.remotes.origin.refs

    if 'feature/kbcli-update' in git_refs:
        # checkout feature/kbcli-update branch
        print("--- Checkout feature/kbcli-update branch ---")
        git_repo.git.checkout('feature/kbcli-update')
    else:
        # create feature/kbcli-update branch
        print("--- Create feature/kbcli-update branch ---")
        git_repo.git.checkout(b='feature/kbcli-update')

    # move kbcli.yaml to clone repo plugins folder
    print("--- Move kbcli.yaml to clone repo plugins folder ---")
    # if kb.yaml exists, remove it
    shutil.move('kb.yaml', os.path.join(github_repo_name, 'plugins', 'kb.yaml'))

    # add kbcli.yaml to git index
    # check if there are changes
    if git_repo.is_dirty() or git_repo.untracked_files:
        # commit and push changes to feature/kbcli-update branch
        print("--- Add kbcli.yaml to git index ---")
        git_repo.index.add('*')
        print("--- Commit and push changes to feature/kbcli-update branch ---")
        git_repo.config_writer().set_value('user', 'email', '{}@users.noreply.github.com'.format("fengluodb"))
        git_repo.index.commit('Update kbcli to {}'.format(version))
        git_repo.git.push('--set-upstream', 'origin', 'feature/kbcli-update')

    print("--- Done ---")
