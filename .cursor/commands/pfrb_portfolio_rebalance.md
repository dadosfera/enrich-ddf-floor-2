# /pfrb_portfolio_rebalance

<!-- COMMAND_ID: 045 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pf_portfolio_rebalance -->

**PURPOSE**: Run a portfolio-wide plans review and **rebalance** priorities across `active/`, `prioritized/`, `backlog/`, `blocked/`, `canceled/`, and `finished/` using the lv1 mini prompt, without colliding with existing priority/review prefixes.

## Usage

```bash
# In the agent interface
@mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md
```

## Description

This command is the high-level entry point for **portfolio-wide rebalancing** when the code base or business context has changed and you need to realign work:

- Scan all plan and project folders under `plans/`, `docs/plans/`, and `projects/` (top-level and project-scoped).
- Include **all statuses**: `active/`, `prioritized/`, `backlog/`, `blocked/`, `canceled/`, and `finished/` (for historical context).
- Apply the enhanced effort–impact matrix from the mini prompt to rebalance work and surface:
  - Immediate priorities: `QW_` quick wins, `CB_` critical blockers, `SEC_` security/safety.
  - High-value follow-ups: `HI_`, technical debt, and dependency-resolution plans.
- Propose concrete updates such as:
  - Which backlog items should move to `prioritized/`.
  - Which prioritized plans should be prepared for `active/`.
  - Which large plans should be split into smaller, executable chunks.
- Output a **clear shortlist of next 5–10 plans** to execute, plus consolidation opportunities; do **not** move or edit plan files directly—produce a change proposal that can be applied via normal plan lifecycle commands.

## Scope Boundaries

**Portfolio-wide scope**: This command operates across **all repositories and projects** in the portfolio (multi-repository scope). For single-repository operations, use:

| Scope                       | Command                      | Description                                                                                  |
| --------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------- |
| **Plan-only**               | `/plrr_plan_reorder`         | Plan reordering within a single repository's plan structure (narrower scope, plan-focused)   |
| **Portfolio with projects** | `/revp_prj_portfolio_review` | Portfolio review with detailed project-level analysis (single repository, includes projects) |

**Note**: This is the broadest scope command for reprioritization. Use this when you need to rebalance work across multiple repositories in the portfolio.

## Related

- **Local Reference**: `mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md
- /plrr_plan_reorder (ID 048) - Plan reordering within single repository (narrower scope, plan-focused)
- /revp_prj_portfolio_review (ID 042) - Portfolio review with project analysis (single repository, includes projects)
- `/mpov_meta_plan_overview` - Overview of master meta plan
- `/next_next_plan_cycle` - Execute next plan in lifecycle
- `/prio_investigate_codebase_priorities` - Investigate codebase priorities
