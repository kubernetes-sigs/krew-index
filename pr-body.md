This PR adds the `crashloop` plugin to Krew.

`crashloop` is a `kubectl` plugin for inspecting pod crash history. It correlates warning Events, container last termination state, and previous logs into a single report for one pod. The user-facing effect is faster crash diagnosis without having to manually stitch together `kubectl describe`, event inspection, and `kubectl logs --previous`.

The plugin release submitted here is `v0.1.0` from https://github.com/rohankaran/kubectl-crashloop/releases/tag/v0.1.0. The manifest points at the published darwin amd64, darwin arm64, linux amd64, linux arm64, and windows amd64 archives and includes the matching SHA256 checksums from the release.

Validation performed for this submission:

- Generated the manifest from the published `v0.1.0` release checksums.
- Installed the manifest locally with Krew using the generated manifest.
- Verified the plugin is registered by `kubectl plugin list`.
- Verified execution with `kubectl crashloop demo`.
