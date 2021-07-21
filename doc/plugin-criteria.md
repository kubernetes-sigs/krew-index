Krew plugin criteria
===

Rationale
---

Krew is a `kubectl` plugin manager.

The centralized Krew plugin index (`sigs.k8s.io/krew-index` repository) holds plugins that are applicable to a broad set of kubectl users.

A plugin in the Krew plugin index must add new functionality or enhance the existing functionality in `kubectl`, or encapsulate a common operator/developer workflow for higher productivity.

A plugin should be classified in the following categories:

- Purpose
- Category
- Usability

Purpose
---

This task should be classified in one of the categories:

<table>
    <thead>
    <tr>
        <th>#</th>
        <th>Classification</th>
        <th>Recommendation</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>1.</td>
        <td>The task is already solved by kubectl.</td>
        <td>
          Mere command wrappers are not acceptable, as those are better coveredby shell aliases.
          However, convenience and productivity improvements are welcome. Examples:
           <ul>
             <li><code>konfig</code> is a convencience script to aid with merging of kubeconfig files, similar to <code>kubectl config view</code>.</li>
             <li><code>change-ns</code> is a utility easily switch between namespaces, similar to <code>kubectl config set-context --curent -n</code></li>
             <li><code>view-secret</code> retrieves and decodes secrets, similar to <code>kubectl get secret -o jsonpath=... | base64 -d</code></li>
           </ul>
        </td>
    </tr>
    <tr>
        <td>2.</td>
        <td>
          The task provides a different solution to a problem which is also solved by kubectl.
          However, the task would be impossible or very hard to reproduce with kubectl alone.
        </td>
        <td>
          In general welcome unless it overlaps significantly with other plugins or has a bad usability.
          Examples:
          <ul>
            <li><code>get-all</code> plugin is a replacement for <code>kubectl get all</code> command which actually fetches only a subset of API resource types.</li>
            <li><code>access-matrix</code> gives an overview of authorities, whereas <code>kubectl auth can-i</code> only applies to single resource/verb pairs</li>
            <li><code>tail</code> plugin allows tailing logs from pods from a label selector, a namespace or all namespaces at once, whereas <code>kubectl logs</code> command has more limited functionality.</li>
            <li><code>mtail</code> plugin allows tailing logs from pods from a label selector, similar to <code>kubectl logs -l</code> but labels log lines.</li>
          </ul>
        </td>
    </tr>
    <tr>
        <td>3.</td>
        <td>The task addresses a completely different problem than any of the kubectl subcommands, but is clearly focused on k8s.</td>
        <td>
          Gray area. If most users would use tool as a <code>kubectl</code> plugin, it may be accepted.
          For example, <code>kubectl debug-pod</code> would be acceptable.
          On the other hand, <code>helm</code> as <code>kubectl helm</code> would not be acceptable, because it is independent.
        </td>
    </tr>
    <tr>
        <td>4.</td>
        <td>
          The task is very dissimilar to common kubectl tasks and is not primarily focused on k8s.
          However, it can be useful in the k8s ecosystem.
        </td>
        <td>Not acceptable. Consider distributing as a separate tool instead of making it a kubectl plugin.</td>
    </tr>
    <tr>
        <td>5.</td>
        <td>
          The task is very dissimilar to common kubectl tasks and is not focused on k8s.
          Its general usefulness in the k8s ecosystem is questionable.
        </td>
        <td>Not acceptable.</td>
    </tr>
    </tbody>
</table>

Category
---

In order of decreasing usage frequency:

<table>
    <thead>
    <tr>
        <th>#</th>
        <th>Classification</th>
        <th>Recommendation</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>1.</td>
        <td>Recurring task on the same cluster. For example: <code>mtail</code></td>
        <td>Favors acceptance as plugin.</td>
    </tr>
    <tr>
        <td>2.</td>
        <td>
          Recurring task on different cluster instances, but one-time task on the same cluster instance.
          For example: <code>init-tiller</code>
        </td>
        <td>Gray area. Usually this is not acceptable.</td>
    </tr>
    <tr>
        <td>3.</td>
        <td>One-time task per machine.</td>
        <td>In general not acceptable as plugin.</td>
    </tr>
    </tbody>
</table>

Usability
---
Plugins should be as user-friendly as possible.
Please follow the following guidelines:

1. Standard look & feel: The plugin should adhere to standard kubectl best practices and have consistent (abbreviated) flag names. For example: bad `--ns`, good `--namespace` + `-n`.
    - when writing a plugin in go, consider using the official `k8s.io/cli-runtime/pkg/genericclioptions`
2. A plugin should be documented in such a way, that a proficient `kubectl` user immediately understands its purpose and how to use it.
3. If the plugin has dependencies, try to limit those to fundamental UNIX tools (like bash, sed, grep, awk) or popular tools (like jq, yq) as this makes it easier to get started.
4. Make sure the plugin fails with a user-friendly error when a required dependency is missing.
