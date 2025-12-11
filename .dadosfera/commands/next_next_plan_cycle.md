# /next_next_plan_cycle
<!-- COMMAND_ID: 014 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ne_next_plan_cycle -->

**PURPOSE**: Pick and EXECUTE the **next** plan in the queue (Active → Prioritized → Backlog) without getting stuck on already finished plans.

This command is for **one-step advancement** in the plan lifecycle, not for executing every plan in the repo. Use `/xpal_execute_plan_all` or `/plca_complete_all_active` if you want to sweep all active plans.

---

## CRITICAL BEHAVIOR RULES

- **Your job is to move work forward, not to say “re-run this command.”**
- If the last plan is already in `finished/`, **do NOT** tell the user to call `/next_next_plan_cycle` again.
- Instead, **re-scan the filesystem** (Active → Prioritized → Backlog) and pick the next plan according to the algorithm below.
- If **no candidate plans exist**, only then it is valid to suggest creating new plans (e.g. via `/prio_investigate_codebase_priorities`).

---

## 0. Detect Repository Type and Plans Base

Use repository name to resolve the correct plans base path (no hardcoded `docs/plans` for `-fera` repos):

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
REPO_NAME=$(basename "$REPO_ROOT")
if [[ "$REPO_NAME" == *-fera ]]; then
    PLANS_BASE="_dev/docs/plans"
else
    PLANS_BASE="docs/plans"
fi
```

When you talk about paths in your answer, **always** show absolute paths using `"$REPO_ROOT/$PLANS_BASE/..."`

---

## 1. Ignore Already-Finished Plans (MANDATORY)

Before selecting the next plan, **ignore any plan that already lives under `finished/`**:

- If the conversation or user mentions a plan like
  `.../plans/finished/QW_1h_HIGH_systematic_hardcoded_constants_fix.md`:
  - Acknowledge it is complete and already in `finished/`
  - **Do NOT** route work back into that plan
  - **Do NOT** answer “Re-run `/next_next_plan_cycle` so it can select the next plan”
- Instead, immediately proceed with **Section 2–4** to find the **next** plan.

Your response MUST always move to a **new target plan** or say “no plans left” after checking the directories.

---

## 2. Find the Next Active Plan (Primary Path)

Look for candidates in `"$PLANS_BASE/active"`:

```bash
# Find active plans (exclude README.md, AGENTS.md, index files)
ACTIVE_PLANS=$(find "$PLANS_BASE/active/" -name "*.md" \
  ! -name "README.md" ! -name "AGENTS.md" ! -name "index*.md" \
  -type f 2>/dev/null | sort)
```

If `ACTIVE_PLANS` is **non-empty**:

1. Rank candidates by prefix and effort (see Priority Table below):
   - Highest prefix first: `QW_` → `CB_` → `SEC_` → `RW_` → `HI_` → `MI_` → others (alphabetical)
   - Within same prefix, prefer **shorter effort**: `_30m_` < `_1h_` < `_2h_` < `_4h_` < `_1d_` …
2. Select the **single best candidate** as `NEXT_PLAN`.
3. Respond with something like:

> **Next plan selected (Active queue)**
> Plan: `<absolute path>`
> Reason: `QW_` quick win with shortest effort among active plans.
> I will now start executing it, beginning with task 1...

Then execute tasks directly or by invoking `/xect_execute_plan` on that plan.

---

## 3. Promote from Prioritized → Active (if Active empty)

If there are **no active plans**, promote the top plan from `prioritized/` into `active/`:

```bash
# Priority order: QW_ > CB_ > SEC_ > RW_ > HI_ > MI_ > others
for prefix in QW_ CB_ SEC_ RW_ HI_ MI_; do
  PLAN=$(ls -1 "$PLANS_BASE/prioritized/"${prefix}*.md 2>/dev/null | head -1)
  if [ -n "$PLAN" ]; then
    mv "$PLAN" "$PLANS_BASE/active/"
    NEXT_PLAN="$PLANS_BASE/active/$(basename "$PLAN")"
    break
  fi
done

# Fallback: any .md file (non-README)
if [ -z "$NEXT_PLAN" ]; then
  PLAN=$(ls -1 "$PLANS_BASE/prioritized/"*.md 2>/dev/null | grep -v README | head -1)
  if [ -n "$PLAN" ]; then
    mv "$PLAN" "$PLANS_BASE/active/"
    NEXT_PLAN="$PLANS_BASE/active/$(basename "$PLAN")"
  fi
fi
```

If `NEXT_PLAN` is set:

- Say you **promoted** it from `prioritized/` to `active/`
- Show the **absolute path**
- Immediately proceed to execute it (directly or via `/xect_execute_plan`)

**Do not stop after promotion. This command must both promote and start execution.**

---

## 4. Promote from Backlog → Active (if Prioritized empty)

If there are no active or prioritized plans, promote from `backlog/`:

```bash
PLAN=$(find "$PLANS_BASE/backlog" -name "ready_*.md" -type f | sort | head -1)
if [ -n "$PLAN" ]; then
  mv "$PLAN" "$PLANS_BASE/active/"
  NEXT_PLAN="$PLANS_BASE/active/$(basename "$PLAN")"
fi
```

If `NEXT_PLAN` is set:

- Explain that you **promoted a ready backlog plan** into `active/`
- Show the **absolute path**
- Immediately begin execution of that plan

If `NEXT_PLAN` is still empty after this step:

- It is valid to say:

> I checked `active/`, `prioritized/`, and `backlog/ready_*` under `<absolute PLANS_BASE>`, and there are no remaining candidate plans.
> The next step is to create new plans, for example by running `/prio_investigate_codebase_priorities`.

---

## 5. Git Sync After Promotions

Whenever you actually move plans between folders (`prioritized/` → `active/`, `backlog/` → `active/`), recommend running the git sync workflow:

```bash
/gsyn_git_sync
```

You may mention `/gful_git_full_sync` when submodules or multi-repo changes are involved.

---

## Priority Prefixes (from Highest to Lowest)

| Rank | Prefix | Meaning             |
|------|--------|---------------------|
| 1    | `QW_`  | Quick Win – do FIRST |
| 2    | `CB_`  | Critical Blocker    |
| 3    | `SEC_` | Security            |
| 4    | `RW_`  | Runbook/Recovery    |
| 5    | `HI_`  | High Impact         |
| 6    | `MI_`  | Medium Impact       |
| 7    | others | Alphabetical        |

Within the same prefix, prefer shorter effort markers (e.g. `_30m_` before `_4h_`).

---

## Post-Execution Lifecycle (After Completing a Plan)

When **all tasks** in the current plan have been executed, `/next_next_plan_cycle` must follow a **double‑verification pattern** instead of moving the plan immediately:

1. **Execution cycle (first pass)**:
   - Update the plan’s `Status:` / `**Status**:` to `finished` / `completed` / `done`.
   - Optionally add a short `## Lessons Learned` section (2–3 bullet points max).
   - Mark the plan as implementation-complete by renaming it to use the `.completed` extension (for example `plan.md` → `plan.completed`) while keeping it under `${PLANS_BASE}/active/`.
   - Do **not** move the plan to `finished/` in this pass; the plan is “ready for verification” but still lives in `active/` for visibility and potential follow‑up work.

2. **Verification cycle (second pass)**:
   - On a subsequent `/next_next_plan_cycle` run, when the best candidate is this `.completed` plan, treat that run as a **verification-only cycle**:
     - Re-run assertions, documentation updates, and tests required by the plan.
     - Confirm there are no remaining unchecked tasks or regressions and that the plan content has not drifted back into an “active work” state.
   - If verification passes and no new active work is introduced, you may now move the plan from `${PLANS_BASE}/active/` to `${PLANS_BASE}/finished/` (dropping the `.completed` suffix if desired), in line with `templates/plan_management_system.md`.
   - If verification fails or new work is needed, clear the `.completed` marker and keep the plan in `active/` for further execution instead of moving it.

After a plan is successfully moved to `finished/`, `/next_next_plan_cycle` must pick a **different** plan (or report that no plans remain); it must never loop on the already‑finished one.

**Never** let “Lessons Learned” or the verification cycle block execution indefinitely; keep both pragmatic and focused on ensuring the plan is truly done before archival.

---

## Anti-Patterns (DO NOT DO THESE)

- ❌ “This plan is already finished; please re-run `/next_next_plan_cycle`.”
  - ✅ Instead: **select another plan** from `active/`, `prioritized/`, or `backlog/ready_*`.
- ❌ “First I need to analyze PDCA/PDSA in detail before choosing the next plan.”
  - ✅ Instead: apply the simple priority rules and start executing.
- ❌ Ignoring a clearly higher-priority `QW_` plan in favor of a random `MI_` plan.

**Correct behavior example**:

> Active and finished queues inspected.
> Previous plan `QW_1h_HIGH_systematic_hardcoded_constants_fix.md` is in `finished/`, so I will not reuse it.
> Next plan selected: `<absolute path to new active or promoted plan>`.
> I will now begin executing its tasks, starting with task 1...

---

## Related Commands

- `/xect_execute_plan` — Execute the content of a selected plan
- `/plca_complete_all_active` — Validate and complete **all** active plans with semantic overlap checks
- `/xqpa_xqt_plan_all` — Execute all active plans in simple priority order
- `/reva_review_active_conversation` — Review conversation and create/update plans
- `/arch_archive` — Archive completed plans and related artifacts
