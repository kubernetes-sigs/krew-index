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
             <li>`konfig` is a convencience script to aid with merging of kubeconfig files, similar to `kubectl config view`.</li>
             <li>`change-ns` is a utility easily switch between namespaces, similar to `kubectl config set-context --curent -n`</li>
             <li>`view-secret` retrieves and decodes secrets, similar to `kubectl get secret -o jsonpath=... | base64 -d`</li>
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
            <li>`get-all` plugin is a replacement for `kubectl get all` command which actually fetches only a subset of API resource types.</li>
            <li>`access-matrix` gives an overview of authorities, whereas `kubectl auth can-i` only applies to single resource/verb pairs</li>
            <li>`tail` plugin allows tailing logs from pods from a label selector, a namespace or all namespaces at once, whereas `kubectl logs` command has more limited functionality.</li>
            <li>`mtail` plugin allows tailing logs from pods from a label selector, similar to `kubectl logs -l` but labels log lines.</li>
          </ul>
        </td>
    </tr>
    <tr>
        <td>3.</td>
        <td>The task addresses a completely different problem than any of the kubectl subcommands, but is clearly focused on k8s.</td>
        <td>Gray area. If the task fits well into `kubectl`, it may be accepted (for example `kubectl debug-pod`).</td>
    </tr>
    <tr>
        <td>4.</td>
        <td>
          The task is very dissimilar to common kubectl tasks and is not primarily focused on k8s.
          However, it can be useful in the k8s ecosystem.
        </td>
        <td>Not acceptable.</td>
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
        <td>Recurring task on the same cluster. For example: `mtail`</td>
        <td>Favors acceptance as plugin.</td>
    </tr>
    <tr>
        <td>2.</td>
        <td>
          Recurring task on different cluster instances, but one-time task on the same cluster instance.
          For example: `init-tiller`
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
Further required acceptance criteria:

1. Standard look & feel: Adheres to standard kubectl best practices and in particular uses consistent (abbreviated) flag names. For example: bad `--ns`, good `--namespace` + `-n`.
2. A plugin needs to be documented in such a way, that a proficient `kubectl` user immediately understands its purpose and how to use it.
3. Plugins may not depend on additional non-standard third-party tools which are not part of the plugin installation. Acceptable: jq, standard unix CLI tools (awk, sed, grep).
<!-- 4. Ready to use: Unless absolutely required, a plugin should not need extra configuration. -->
