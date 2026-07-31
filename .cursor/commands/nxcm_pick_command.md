---
category: planning
criticality: medium
scope: all
---
# /nxcm_pick_command
<!-- COMMAND_ID: 070 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: nx_pick_command -->

<!-- TEMPLATE_VERSION: 1.0.0 -->

**Local Reference**: `commands/nxcm_pick_command.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/nxcm_pick_command.md`

Backlinks:
- commands/index_commands.yaml
- commands/reva_review_active_conversation.md
- commands/chkp_check_pending.md
- commands/pfac_plan_from_active_tasks_conversation.md
- commands/xect_execute_plan.md
- commands/jour_journey_meta_best_track.md
- mini_prompt/index_mini_prompt.md
- standards/agents/autonomous_execution.md

## When to Use

- When the agent is unsure what to do now.
- At the start of a session, to pick the best entry command.
- After finishing a step, to decide the command that advances the objective.
- When multiple commands match the same “shape” (review vs plan vs execute vs test).
