# /invp_investigate_priorities

<!-- COMMAND_ID: 049 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pr_investigate_codebase_priorities -->

This command triggers the **Investigate Top Priorities & Suggest Plans/Projects** mini-prompt.

## Usage

```bash
# In the Agent interface
@mini_prompt/lv0/investigate_top_priorities.md
```

## Description

Analyzes the codebase to identify top 10 priorities and suggests creating top 5 plans and top 5 projects.

> Renamed from `/inve_investigate_codebase_priorities` to avoid prefix collisions; behavior is unchanged.

## Related

- [fresh_codebase_top10_improvements](../mini_prompt/lv0/fresh_codebase_top10_improvements.md)
