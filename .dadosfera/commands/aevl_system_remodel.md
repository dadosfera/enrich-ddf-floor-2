# /aevl_system_remodel
<!-- COMMAND_ID: 013 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ae_system_remodel -->

Use the Architecture Evolution & Deprecation Review mini prompt to decide when to stop chasing micro-fixes and instead make a system/architecture-level change (simpler or more structured) that reduces long-term cost, then feed the result into `/dlog_decision_log` (ADR) and the planning commands.

Backlinks:

- **Local Reference**: `mini_prompt/lv2/architecture_simplification_review_mini_prompt.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv2/architecture_simplification_review_mini_prompt.md
- **Local Reference**: commands/reva_review_active_conversation.md
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/commands/reva_review_active_conversation.md
- **Local Reference**: commands/dlog_decision_log.md
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/commands/dlog_decision_log.md

## Command sequence (run in order)

1. **Confirm repository context and gather current work signals**

   bash
   gtimeout 5 git rev-parse --show-toplevel
   gtimeout 5 git status --short
   ```

   - Briefly summarize:
     - The main objective of the current conversation.
     - Which subsystems or files have been touched repeatedly by small fixes.
     - Any signs that “this would be easier if we remodeled the system/architecture instead” (even if that means adding structure or components).

2. **Review conversation and plan context**

   - If not done recently, run `/reva_review_active_conversation` to:
     - Extract all tasks from the current conversation.
     - See where micro-fix work is concentrated (same module/boundary/feature).
   - Use the output to identify **clusters of small tasks** that might be replaced or greatly simplified by a system/architecture evolution (new boundary, new service, abstraction, or simplification).

3. **Invoke the Architecture Evolution & Deprecation mini prompt**

   - Treat `mini_prompt/lv2/architecture_simplification_review_mini_prompt.md` as the **primary reasoning scaffold**:
     - Summarize current architecture pain points.
     - Enumerate at least two evolution options:
       - Keep current architecture + micro-fixes.
       - Targeted evolution (simplification or additional structure) that obsoletes or shrinks a large chunk of code.
       - (Optional) Larger re-architecture if clearly justified.
     - Identify which tasks/plans become obsolete under each option.
   - Stay in **analysis mode only** here: do not modify code or plans yet.

4. **Decide whether an architecture ADR is needed**

   - If the mini prompt analysis shows that:
     - A single architecture decision could delete or simplify a lot of current/future work, **or**
     - A more structured architecture would significantly reduce long-term maintenance cost, **or**
     - Continuing micro-fixes would keep fighting the same complexity,
    then **escalate to `/dlog_decision_log`**.
   - Otherwise:
     - Document briefly why current architecture is adequate for now.
     - Return to `/reva_review_active_conversation` and normal planning/implementation.

5. **Run `/dlog_decision_log` using the mini prompt output as options**

   - When escalating:
    - Use the evolution options (and their impact on deletions/simplification/added structure/tests) from step 3 as the explicit options in `/dlog_decision_log`.
     - Make sure the decision matrix includes:
       - Future maintenance cost.
       - Amount of code/tasks that become obsolete or easier to change.
       - Risk and migration complexity.
    - Complete the ADR and store it under `_dev/docs/decisions/` or `docs/decisions/` as per `/dlog_decision_log`.

6. **Propagate the decision into plans and tasks**

   - After the ADR is written:
     - Use `/reva_review_active_conversation` and planning commands to:
       - Mark micro-fix tasks that are now obsolete as **superseded** or move them to backlog for reference.
       - Create new **prioritized** plans for implementing the chosen system/architecture evolution or remodel.
    - Ensure no active plan remains that only exists to fix code that will be deleted or made irrelevant by the new architecture.

## Notes

- Use this command when you notice **repeated small fixes** in the same area or when tests keep breaking due to brittle architecture, not just isolated bugs.
- Evolution might **simplify** the system or make it **more sophisticated** (e.g., new service, pipeline, or abstraction); the key is reducing long-term cost and risk, not always minimizing components.
- Always keep `/reva_review_active_conversation` and `/dlog_decision_log` in the loop so that:
  - The **decision** is recorded (ADR), and
  - The **task list** reflects the new architecture reality (no zombie micro-fix plans).
