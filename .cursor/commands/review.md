# /review

Review the entire conversation to extract: (1) pending tasks, (2) proposed tasks not yet initiated, and (3) next tasks directly related to the problem. Do not branch into new topics or start plans; focus strictly on the current problem.

Backlinks:
- mini_prompt/lv1/mini_prompt_meta_plan_mini_prompt.md
- mini_prompt/lv2/agent_branch_merge_mini_prompt.md
- mini_prompt/lv1/post_discovery_codebase_improvement_mini_prompt.md

## Execution checklist (run in order)

1) Confirm repository context (for references only)
```bash
gtimeout 5 git rev-parse --show-toplevel
```

2) Conversation synthesis (no code changes yet)
- Summarize the objective(s) and constraints explicitly stated
- List key decisions and fixes/improvements attempted or completed
- Note any blockers, risks, or assumptions that impact scope

3) Task extraction
- Pending tasks: Items discussed but not completed in the conversation
- Proposed-not-initiated: Suggestions raised but never started
- Next tasks (directly related): Immediate, scoped actions that advance the same objective

4) Output format (produce this in your message)
- Pending tasks
- Proposed but not initiated
- Next tasks directly related (no new topics)
- Short rationale tying each item back to the conversation

5) Optional local references (for validation; do not create new plans)
```bash
gtimeout 5 git status --short
```
```bash
gtimeout 5 ls -1 docs/plans/backlog 2>/dev/null | head -50
```

## Notes
- Do not create or move plan files from this command
- Keep scope tight to the conversation’s problem; avoid unrelated initiatives
- Be concise, actionable, and prioritize by impact and effort
- If something requires a plan, list it under “Next tasks” but do not create the plan here
