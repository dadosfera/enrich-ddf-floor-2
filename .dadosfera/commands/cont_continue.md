---
category: planning
criticality: medium
scope: all
---
# /cont_continue
<!-- COMMAND_ID: 071 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: co_continue -->

Resume work from where the conversation left off. Inspect what was last in flight (active plan, open todo, failing test, pending PR) and execute the smallest concrete next step without waiting for further instructions.

**Critical rule**: 'Continue' is NOT a license to invent new work. Only resume what is already in flight - do NOT start a new initiative.

**Critical rule**: If multiple plausible next steps exist and the cost of the wrong one is non-trivial, STOP and ask the user instead of guessing.

**Local Reference**: `commands/cont_continue.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/cont_continue.md`

Backlinks:
- commands/nxcm_pick_command.md
- commands/reva_review_active_conversation.md
- commands/pfac_plan_from_active_tasks_conversation.md
- commands/xect_execute_plan.md
- commands/next_next_plan_cycle.md
- standards/agents/autonomous_execution.md

## When to Use

- The user says 'continue', 'go on', 'proceed', 'keep going', or similar.
- The agent finished a step and should advance the work without waiting for more instructions.
- Resuming work based on conversation context from the previous session.

## When NOT to Use

- When there is nothing in flight - say so and ask the user what to do.
- When the in-flight work was paused for explicit user approval - wait for it.
- When the next step requires authorization (force push, ignored-file edit, restricted folder) - ask first.

## Command sequence (run in order)

### 1. Inventory what is in flight

Read these in order; stop at the first concrete next step you find.

```bash
# 1. TodoWrite list (in-progress > pending)
# 2. Active plan files (look for ~/.cursor/plans/*.plan.md or .cursor/plans/)
# 3. Last failing test or lint error in the conversation
# 4. Open PR with unresolved review comments
# 5. Last command output that showed a pending action
```

### 2. Pick the smallest concrete next step

Prefer one specific, verifiable action over a long autonomous run.

```bash
# Examples of 'smallest next step':
# - Mark the in-progress todo as done and start the next pending one
# - Re-run the failing test after the most recent edit
# - Address a single open PR comment
# - Run the next phase of the active plan
```

### 3. Verify the prerequisites still hold

```bash
# - Working tree state (git status) matches what the previous step expected
# - Required files / branches still exist
# - No new user messages have changed the goal
```

### 4. Execute and report

Run the step. Report what was done and what is next, so the user can interject before the next iteration.

```bash
# After executing, summarize:
# - What ran (or what was edited)
# - The verification result (test, lint, diff)
# - The next concrete step you would take if asked to /cont_continue again
```

## Decision tree (which router to call instead)

If Step 1 finds:

- An active `.plan.md` -> use `/xect_execute_plan` instead of guessing.
- A long-running task chain -> use `/aulo_autonomous_loop`.
- An ambiguous backlog -> use `/nxcm_pick_command` to choose.
- A finished conversation that needs archiving -> use `/arch_archive`.

`/cont_continue` is the fallback when none of the above clearly applies.

## Stop conditions

Stop and ask the user when ANY of these is true:

- The next step requires destructive or authorized action.
- Multiple plausible next steps exist with different outcomes.
- The previous step failed and the failure mode is unclear.
- The user has been silent for many iterations and progress is no longer obvious.

## Related Commands

- `/nxcm_pick_command`
- `/xect_execute_plan`
- `/aulo_autonomous_loop`
- `/arch_archive`
- `/reva_review_active_conversation`
