---
# Dadosfera Metadata
category: planning
criticality: critical
scope: all
commandId: "078"
version: "1.0.0"
type: "re_review"
canonical: "docs-fera@/commands/revt_review_top_ten_plans.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/revt_review_top_ten_plans.md"

# Claude Code Metadata
name: "Review Top Ten Plans"
description: "Generate comprehensive top 10 plans list with priority justification and paths"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 078 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: re_review -->
# /revt_review_top_ten_plans

**Command**: `/revt_review_top_ten_plans`

**Analysis only - no files modified.** Orchestrates multiple review commands to generate a comprehensive top 10 list of existing plans with priority justification, absolute paths, descriptions, and names. Outputs in two sections of 5 plans each.

## Usage

```bash
# In the Agent interface
@mini_prompt/lv1/top10_plans_list_generation_lv1_mini_prompt.md
```

## Description

This command orchestrates a comprehensive review workflow that combines insights from multiple review commands without overlapping tasks:

1. **Inventory existing plans** across all statuses (active, prioritized, backlog, blocked, canceled, finished)
2. **Collect priority data** from codebase analysis and plan reviews
3. **Rank and select top 10 plans** based on priority, effort-impact, and dependencies
4. **Generate formatted output** with two sections of 5 plans each, including:
   - Plan name
   - Absolute path
   - Description
   - Priority justification

## Command Orchestration (No Task Overlap)

This command coordinates multiple review operations without duplicating work:

### Phase 1: Plan Discovery
- Scans all plan directories (`_dev/docs/plans/`, `docs/plans/`, `plans/`)
- Collects existing plans from all statuses
- Extracts metadata (name, path, status, effort, impact)

### Phase 2: Priority Analysis
- Uses insights from `/revc_review_codebase_priorities` (codebase priorities)
- Uses insights from `/revl_review_all_plans` (meta plan context)
- Applies effort-impact matrix from `/plrr_plan_reorder` logic (single-repo prioritization patterns)
- Applies portfolio-level prioritization patterns from `/pfrb_portfolio_rebalance` (multi-repo context awareness, cross-repository dependency understanding, portfolio-wide effort-impact balancing)
- **Does NOT execute** these commands directly to avoid overlap

### Phase 3: Ranking & Selection
- Ranks plans by priority prefix (QW_ > CB_ > SEC_ > HI_ > MI_ > others)
- Considers effort (shorter effort preferred within same prefix)
- Evaluates impact (HIGH/CRITICAL prioritized)
- Accounts for dependencies and blockers

### Phase 4: Output Generation
- Formats top 10 plans in two sections (5 plans each)
- Includes all required fields: name, absolute path, description, priority justification

## Output Format

The command outputs a structured top 10 list in two sections:

### Section 1: Top 5 Highest Priority Plans (1-5)

1. **Plan Name**: `{PREFIX}_{EFFORT}_{IMPACT}_{slug}`
   - **Absolute Path**: `/full/absolute/path/to/plan.md`
   - **Description**: One-line description of what this plan accomplishes
   - **Priority Justification**: Why this plan is ranked in the top 5 (e.g., "Quick win with 2h effort and HIGH impact on developer experience")

2. **Plan Name**: ...
   - **Absolute Path**: ...
   - **Description**: ...
   - **Priority Justification**: ...

[... continues for plans 3-5 ...]

### Section 2: Next 5 Priority Plans (6-10)

6. **Plan Name**: ...
   - **Absolute Path**: ...
   - **Description**: ...
   - **Priority Justification**: ...

[... continues for plans 7-10 ...]

## When to Use

- When you need a quick overview of the most important plans to work on
- Before starting a new work cycle to understand priorities
- When coordinating work across multiple agents or team members
- To get a prioritized list without executing full review commands

## Constraints

### Must Do
- Scan all plan statuses (active, prioritized, backlog, blocked, canceled, finished)
- Include both top-level and project-scoped plans
- Use absolute paths for all plan references
- Rank by priority prefix and effort-impact matrix
- Output exactly 10 plans in two sections of 5

### Must Not Do
- Do NOT execute `/revc`, `/plrr`, `/pfrb`, or `/revl` commands directly (only use their logic)
- Do NOT modify or move plan files
- Do NOT create new plans
- Do NOT duplicate work already done by other review commands

## Related Commands

- `/revc_review_codebase_priorities` (ID: 028) - Identifies codebase priorities (logic used, not executed)
- `/revl_review_all_plans` (ID: 035) - Reviews all plans including meta plans (logic used, not executed)
- `/plrr_plan_reorder` (ID: 047) - Plan reordering within single repository (effort-impact matrix logic used, not executed)
- `/pfrb_portfolio_rebalance` (ID: 045) - Portfolio-wide rebalancing across multiple repositories (portfolio prioritization patterns used, not executed)
  - **Portfolio logic explained**: This command operates at the **portfolio level** (multiple repositories), not just a single repository. It considers:
    - Cross-repository dependencies and blockers
    - Portfolio-wide effort-impact balancing (ensuring work is distributed appropriately across repos)
    - Multi-repository context awareness (understanding how plans in one repo affect others)
    - Portfolio-level prioritization patterns (not just single-repo prioritization)
  - **Note**: While `/revt_review_top_ten_plans` operates on a single repository, it uses portfolio-level prioritization patterns to ensure the ranking considers broader organizational context and cross-repo implications.
- `/next_next_plan_cycle` - Execute next plan in lifecycle

## Related Mini Prompt

- Local: `mini_prompt/lv1/top10_plans_list_generation_lv1_mini_prompt.md`
- Git URL: `https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv1/top10_plans_list_generation_lv1_mini_prompt.md`

---

**Local Reference**: `commands/revt_review_top_ten_plans.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/revt_review_top_ten_plans.md`

End Command ---
