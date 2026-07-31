---
category: planning
criticality: high
scope: all
---
# /expr_xpand_prj
<!-- COMMAND_ID: 082 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ex_xpand_project -->

Expand a Project container by discovering its project-scoped plans and expanding each one using the same standards as /expp_xpand_plan, while also refreshing the Project Meta Plan so it accurately coordinates the project work.

**Local Reference**: `commands/expr_xpand_prj.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/expr_xpand_prj.md`

Backlinks:
- commands/expp_xpand_plan.md
- commands/proj_project.md
- mini_prompt/lv1/create_project_lv1_mini_prompt.md
- guides/docs_taxonomy_plans_projects_tasks.md

## When to Use

- The project has multiple project-scoped plans that are sparse or incomplete
- After creating a project and its first set of plans
- When a project meta plan is out of sync with the project’s plans

## Purpose

Projects are long-lived containers (docs/projects/... or _dev/docs/projects/...) that often hold multiple plans. This command discovers project-scoped plan files, expands each plan using /expp_xpand_plan, and refreshes the Project Meta Plan to coordinate priorities and links.

## Reference

For detailed templates, logic, and examples, see:
