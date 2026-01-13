# /revp_prj_portfolio_review

<!-- COMMAND_ID: 040 -->
<!-- COMMAND_VERSION: 1.0.2 -->
<!-- COMMAND_TYPE: rv_prj_portfolio_review -->

**PURPOSE**: Run a repository-wide portfolio review and **realign priorities** across `active/`, `prioritized/`, `backlog/`, `blocked/`, `canceled/`, and `finished/` using the lv1 mini prompt.

## Usage

```bash
# In the agent interface
@mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md
```

## Description

This command is the high-level entry point for **portfolio-wide reprioritization** when the code base or business context has changed and you need to realign work:

- Scan all plan and project folders under `plans/`, `docs/plans/`, and `projects/` (top-level and project-scoped).
- Include **all statuses**: `active/`, `prioritized/`, `backlog/`, `blocked/`, `canceled/`, and `finished/` (for historical context).
- Apply the enhanced effort–impact matrix from the mini prompt to reprioritize work and surface:
  - Immediate priorities: `QW_` quick wins, `CB_` critical blockers, `SEC_` security/safety.
  - High-value follow-ups: `HI_`, technical debt, and dependency-resolution plans.
- Propose concrete updates such as:
  - Which backlog items should move to `prioritized/`.
  - Which prioritized plans should be prepared for `active/`.
  - Which large plans should be split into smaller, executable chunks.
- Output a **clear shortlist of next 5–10 plans** to execute, plus consolidation opportunities; do **not** move or edit plan files directly—produce a change proposal that can be applied via normal plan lifecycle commands.

## Scope Boundaries

**Portfolio review with project analysis**: This command provides portfolio-wide review with detailed project-level analysis across all plans and projects in a single repository. For other scopes, use:

| Scope              | Command                     | Description                                                                                     |
| ------------------ | --------------------------- | ----------------------------------------------------------------------------------------------- |
| **Plan-only**      | `/plrr_plan_reorder`        | Plan reordering within a single repository's plan structure (excludes project-scoped plans)     |
| **Portfolio-wide** | `/pfrb_portfolio_rebalance` | Portfolio-wide rebalancing across all repositories in the portfolio (broader operational scope) |

**Note**: For project-only reprioritization (single project's plans), use project-specific planning commands or manually review the project's plan structure.

## Related

- **Local Reference**: `mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md
- /plrr_plan_reorder (ID 048) - Plan reordering within single repository (narrower scope, plan-focused)
- /pfrb_portfolio_rebalance (ID 046) - Portfolio-wide rebalancing across all repositories (broader scope, multi-repo)
- **Local Reference**: `commands/mpov_meta_plan_overview.md`
  **Git URL Reference**: `
