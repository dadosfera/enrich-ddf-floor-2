# /jou-journey-meta-best-track-or-mini-prompt

Run the highest impact portion of `mini_prompt/lv1/meta_journey_mini_prompt.md`, choosing between the single most valuable mini prompt and the full “best track” (Core Development Loop) based on repository readiness.

## Decision flow (must be followed before executing anything)

1. **Verify repo context**
   ```bash
   gtimeout 5 git rev-parse --show-toplevel
   ```
2. **Check meta plan freshness** – ensure `docs/plans/active/{repo_name}_meta_plan.md` exists and was touched in the last 7 days. If missing/out-of-date → run the Foundation trio (create_meta_plan → project_review_reprioritize → critical_files_review) before proceeding.
3. **Inspect active plans queue**
   ```bash
   gtimeout 5 ls docs/plans/active | head -20
   ```
   - If at least one plan is actionable → go to **Best single mini prompt**.
   - If no actionable plans or the repo is mid-loop → go to **Best track (Core Development Loop)**.

## Best single mini prompt (default choice when an active plan is ready)

1. Execute `mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md`.
   - Purpose: advance the top-priority active plan autonomously.
   - Inputs: latest meta plan, prioritized plan queue, current repo status.
2. Capture outcomes: which plan moved, blockers found, follow-up items.
3. Update plan states:
   ```bash
   gtimeout 5 git status --short docs/plans/active
   ```
   - Move completed plans to `docs/plans/finished` (keep `.completed` suffix when archiving).
4. If execution uncovered quality gates that require the broader loop, immediately switch to the **Best track** section.

## Best track (Core Development Loop from the meta journey)

Execute Template 2 from the meta journey (steps 1-11) in order. Each mini prompt must be run using its file path and instructions; pause if any gate fails.

1. `mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md`
2. `mini_prompt/lv1/application_runner_mini_prompt.md`
3. `mini_prompt/lv1/makefile_runsh_tests_integration_mini_prompt.md`
4. `mini_prompt/lv2/automated_testing_mini_prompt.md`
5. `mini_prompt/lv1/weak_assertion_checker_mini_prompt.md`
6. `mini_prompt/lv1/automated_linting_mini_prompt.md`
7. `mini_prompt/lv1/test_improvement_mini_prompt.md`
8. `mini_prompt/lv2/test_driven_commit_mini_prompt.md`
9. **Stash pre-gate**: run `mini_prompt/lv1/git_stash_management_mini_prompt.md` if stash count >10 or oldest entry >14 days.
10. `mini_prompt/lv1/git_sync_mini_prompt.md`
11. `mini_prompt/lv2/cloud_vs_local_repo_state_sync_mini_prompt.md`
12. If merge required → `mini_prompt/lv2/agent_branch_merge_mini_prompt.md`

### Track execution guardrails

- Stop and document whenever a quality gate fails; branch into `mini_prompt/lv1/post_discovery_codebase_improvement_mini_prompt.md` before resuming.
- After each mini prompt, log outcomes and pending work inside the relevant plan.
- Keep all terminal commands under 20s with `gtimeout`, no chaining, and include 1–2s sleeps where needed.

## Wrap-up

1. Summarize which path ran (single vs track) and why that was considered “best” per the readiness criteria.
2. Update the meta plan and plan indices with new status, linking back to this command’s execution notes.
3. Run the repository’s mandated git-sync workflow once all quality gates pass.
