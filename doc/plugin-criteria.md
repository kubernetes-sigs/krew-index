Krew plugin criteria
===

Rationale
---

Krew is a `kubectl` plugin manager.

A plugin provides a technical solution to at least one _task_ concerning a problem around kubernetes.
As plugins are invoked via `kubectl <plugin-name>`, they should feel like natural extensions of the `kubectl` command in a way that some kubectl task is extended.
Stated reversely: without the plugin, users would typically try to solve the plugin task mainly with kubectl.

A plugin should be classified in the following categories:

- Purpose
- Category
- Usability

Purpose
---

This task should be classified in one of the categories:

1. The task is already solved by kubectl.
2. The task provides a different solution to a problem which is also solved by kubectl. However, the task would be impossible or very hard to reproduce with kubectl alone. Examples: `access-matrix`, `get-all`, `mtail`, `tail`
3. The task addresses a completely different problem than any of the kubectl subcommands, but is clearly focused on k8s.
4. The task is very dissimilar to common kubectl tasks and is not primarily focused on k8s. However, it can be useful in the k8s ecosystem.
5. The task is very dissimilar to common kubectl tasks and is not focused on k8s. Its general usefulness in the k8s ecosystem is questionable.


#### Guideline

- 1: Mere command wrappers are not acceptable, as those are better covered by shell aliases.
  However, convenience and productivity improvements are welcome (examples: `konfig`, `change-ns`, `view-secret`)
- 2: In general welcome unless it overlaps significantly with other plugins or has a bad usability.
- 3: Gray area. If the task fits well into `kubectl`, it may be accepted (for example `kubectl debug`).
- 4: Not acceptable.
- 5: Not acceptable.

Category
---

In order of decreasing frequency:

1. Recurring task on the same cluster. For example: `mtail`
2. Recurring task on different cluster instances, but one-time task on the same cluster instance. For example: `init-tiller`
3. One-time task per machine.

#### Guideline

- 1: Favors acceptance as plugin.
- 2: Gray area. Usually this is not acceptable.
- 3: In general not acceptable as plugin.


Usability
---

1. Standard look & feel: Adheres to standard kubectl best practices and in particular uses consistent (abbreviated) flag names. For example: bad `--ns`, good `--namespace` + `-n`.
2. A plugin needs to be documented in such a way, that a proficient `kubectl` user immediately understands its purpose and how to use it.
3. Plugins may not depend on additional non-standard third-party tools which are not part of the plugin installation. Acceptable: jq, standard unix CLI tools (awk, sed, grep).
<!-- 4. Ready to use: Unless absolutely required, a plugin should not need extra configuration. -->


#### Guideline

- 1,2,3: Required for acceptance.
