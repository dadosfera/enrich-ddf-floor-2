# /revc_review_codebase_priorities

<!-- COMMAND_ID: 028 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: re_review -->
<!-- REVIEW_TYPE: codebase_priorities -->

**Analysis only - no files modified.** Review priorities of the codebase that could become plans and projects. Analyzes the codebase to identify top priorities and suggests creating plans and projects.

This command triggers the **Investigate Top Priorities & Suggest Plans/Projects** mini-prompt.

## Usage

```bash
# In the Agent interface
@mini_prompt/lv0/investigate_top_priorities.md
```

## Description

Analyzes the codebase to identify top 10 priorities and suggests creating top 5 plans and top 5 projects. **All suggested plans and projects are listed with their full absolute paths** for easy reference and creation.

> Renamed from `/inve_investigate_codebase_priorities` to `/prio_investigate_codebase_priorities` to avoid prefix collisions, then to `/revc_review_codebase_priorities` to align with review command naming; behavior updated to show full absolute paths for suggested plans and projects.

## Related

- [fresh_codebase_top10_improvements](../mini_prompt/lv0/fresh_codebase_top10_improvements.md)
