# krew-index

This repository is the centralized plugin index for [Krew (kubectl plugin
manager)][krew-site]. It is meant to be useful only for plugin developers.

- **If you are a Krew user:** You can find the list of kubectl plugins at the
  [Krew website](http://krew.sigs.k8s.io/plugins).

- **If you are a kubectl plugin developer:** Read the [Developer
  Guide][dev-guide] to learn how to package and publish a plugin in this
  repository.

[krew-site]: https://krew.sigs.k8s.io/
[krew-repo]: http://sigs.k8s.io/krew
[dev-guide]: https://krew.sigs.k8s.io/docs/developer-guide/

## Submitting new plugins

To learn how to create a new plugin and submit it to `krew-index`, read the
[Developer Guide][dev-guide] and make a
pull request to this repository.

The decision criteria for plugins accepted to the centralized repository are
evaluated on a case-by-case basis as the community arrives to a decision on
the admission criteria for this repository.

If your plugin is rejected from this repository, you can host your own [custom
index](https://krew.sigs.k8s.io/docs/developer-guide/custom-indexes/) repository
to distribute your plugin with Krew.

## Community

### Bug reports

- If you're having an issue with an installed **plugin itself**, file an issue
  for the repository the plugin's source code is hosted at.
- If you're having a problem **installing or upgrading a plugin**, file an issue
  in this repository.
- If you have a problem with the **Krew itself**, please file an issue in the
  [krew][krew-repo] repository.

### Communication channels

- [Slack](https://kubernetes.slack.com/messages/krew) #krew
- [Mailing List](https://groups.google.com/forum/#!forum/kubernetes-sig-cli)
- [Kubernetes Community site](http://kubernetes.io/community/)

### Code of Conduct

Participation in the Kubernetes community is governed by the [Kubernetes Code
of Conduct](https://github.com/kubernetes-sigs/kustomize/blob/master/code-of-conduct.md).
