# krew-index

This is the centralized plugin index for [krew kubectl plugin manager][krew].

* As a kubectl user: Through [krew][krew], you can discover available kubectl
  plugins hosted in this repository.
* As a kubectl plugin developer:  You can publish your plugins in this
  repository and make it available to others.

[krew]: https://github.com/kubernetes-sigs/krew

## Available kubectl plugins

[See this list](./plugins.md) or the [`./plugins` directory](./plugins)
directory. You can also install [krew][krew] and list available plugins with:

    kubectl krew search

## Submitting new plugins

To learn how to create a new plugin and submit it to krew-index, read the
[Developer Guide](https://krew.sigs.k8s.io/docs/developer-guide/)
and make a pull request to this repository.

The decision criteria for plugins accepted to the centralized repository are
evaluated on a case-by-case basis as the community arrives to a decision on
the admission criteria for this repository.

## Documentation

- [Architecture](https://github.com/kubernetes-sigs/krew/blob/master/docs/KREW_ARCHITECTURE.md)
- [Docs](https://github.com/kubernetes-sigs/krew/blob/master/docs/)
- [Contributing](./CONTRIBUTING.md)  

## Community

### Bug reports

* If you're having a problem with a particular plugin's installation or
  upgrades, file an issue in this repository.
* If you have a problem with the Krew itself, please file an
  issue in the [krew] repository.
* If you're having an issue with an installed plugin, file an issue for the
  repository the plugin's source code is hosted at.

### Communication channels

* [Slack](https://kubernetes.slack.com/messages/krew) #krew
* [Mailing List](https://groups.google.com/forum/#!forum/kubernetes-sig-cli)
* [Kubernetes Community site](http://kubernetes.io/community/)

### Code of Conduct

Participation in the Kubernetes community is governed by the [Kubernetes Code
of Conduct](https://github.com/kubernetes-sigs/kustomize/blob/master/code-of-conduct.md).

[index]:https://github.com/kubernetes-sigs/krew-index
