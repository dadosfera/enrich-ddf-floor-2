---
# Dadosfera Metadata
category: documentation
criticality: medium
scope: all
commandId: "096"
version: "1.0.0"
type: "re_distill_conversation_to_docs_fera"
canonical: "docs-fera@/commands/dstl_distill_conversation_to_docs_fera.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/dstl_distill_conversation_to_docs_fera.md"
backlinks:
  - "commands/reva_review_active_conversation.md"
  - "commands/docu_document.md"
  - "commands/pfac_plan_from_active_tasks_conversation.md"
  - "commands/cana_canonical_topic_alignment.md"
  - "commands/crcv_cross_repo_convergence.md"
  - "commands/ctra_capability_transplant_transfer.md"
  - "commands/dlog_decision_log.md"
  - "commands/arch_archive.md"
  - "guides/commands/command_authoring_best_practices.md"
  - "guides/commands/cursor_commands_sync.md"
  - "standards/documentation/planning_docs_ci_standards.md"

# Claude Code Metadata
name: "Distill Conversation to docs-fera"
description: "Reflect on the current conversation, separate project-specific work from generalizable insights, and propose a docs-fera plan to update shared commands/skills/guides/standards for reuse by other agents and repos"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 096 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: re_distill_conversation_to_docs_fera -->
<!-- UPDATED: 2026-07-31 - Step 8 now requires committing/pushing/PRing the plan file; an untracked plan is lost work. Added concurrent-session worktree route. -->
<!-- TEMPLATE_VERSION: 1.0.0 -->
# /dstl_distill_conversation_to_docs_fera

**Command**: `/dstl_distill_conversation_to_docs_fera`

## Purpose

Run this at any point in (or at the end of) a conversation — in **any** repository, not just `docs-fera` — to reflect on what just happened and answer one question: *"Of everything that came up here, what is worth teaching every other agent and every other repo, not just fixing here?"*

This command does **not** fix the current repo. It:

1. Harvests candidate insights from the conversation (reusing `/reva_review_active_conversation`'s extraction).
2. Runs each candidate through the **Generalization Filter** (below) to separate project-specific noise from durable, reusable signal.
3. Maps the survivors onto the correct `docs-fera` asset type (command, skill, mini prompt, guide, standard, pattern, rule, glossary term).
4. Searches `docs-fera` for an existing file to **extend** before proposing a new one.
5. Writes a single, sanitized **plan file inside `docs-fera`** — it proposes; it does not silently implement.

## When to Use

- You just spent real effort resolving something (a bug, a confusing command, a missing guardrail, an undocumented convention) and suspect other repos/agents would hit the same wall.
- A shared command, skill, mini prompt, guide, or standard turned out to be ambiguous, wrong, stale, or missing entirely — and you had to work around it *this time*.
- You noticed a naming collision, versioning drift, or duplicate concept in the shared command/skill palette while doing unrelated work.
- You are about to run `/arch_archive` to close out the session and want to make sure durable lessons don't get lost in a conversation-scoped archive.

## When NOT to Use

- The entire session was project-specific (business logic, one-off bug, local config) with no reusable lesson — just use `/docu_document` or `/arch_archive` for that repo, and skip this command entirely. Forcing a distillation where none exists is scope creep.
- You already know exactly which `docs-fera` file to edit and the change is trivial (typo, broken link) — edit it directly and skip the ceremony.
- You need to align the **current repo** with existing `docs-fera` canon (the opposite direction) — use `/cana_canonical_topic_alignment` instead.
- The pattern is already confirmed across two or more mature sibling repos and needs an organization-wide standard — use `/crcv_cross_repo_convergence` instead (it operates on repo pairs, not a single conversation).
- You want to move a whole working capability/feature (auth layer, payments, uploader), not a lesson-sized improvement — use `/ctra_capability_transplant_transfer` instead.

## Core Principle: The Generalization Filter

Every candidate insight from the conversation MUST be explicitly tagged **INCLUDE** or **EXCLUDE**. Never silently drop a candidate — list excluded ones too, with a one-line reason, so the filtering is auditable.

**EXCLUDE (project-specific — stays in the current repo only)** when the insight depends on:

- Business logic, domain model, or feature names unique to this product.
- Environment-specific values: ports, hostnames, table/column names, tenant IDs, credentials, API keys.
- A one-off bug caused by *this repo's* specific code with no broader pattern behind it.
- A decision that only makes sense given this repo's specific stack/vendor choice.

**INCLUDE (generalizable — belongs in `docs-fera`)** when the insight is:

- A missing, ambiguous, or wrong instruction in a **shared** command/skill/mini-prompt/rule that cost turns or produced a wrong guess — regardless of which repo surfaced it.
- A recurring mistake pattern that would recur in any repo using the same D&ADDF tooling.
- A documentation gap in `guides/`, `standards/`, or `patterns/` that any agent hitting the same workflow would also hit.
- A naming/collision/versioning issue in the shared command or skill palette itself.
- A genuinely reusable snippet, checklist, or example worth promoting to `standards/` or `patterns/`.
- A better default, guardrail, or safety check that should apply everywhere, not just here.

If a candidate is ambiguous, default to **EXCLUDE** and note it as "needs a second occurrence before promoting" — one data point is an anecdote, not a pattern. Prefer waiting for a repeat over polluting `docs-fera` with a premature generalization.

## Command Sequence (run in order)

### 1. Locate `docs-fera` locally

```bash
LOCAL_REPOS_ROOT="${LOCAL_REPOS_ROOT:-$HOME/local_repos}"
DOCS_FERA_DIR="$LOCAL_REPOS_ROOT/docs-fera"

if [[ ! -d "$DOCS_FERA_DIR" ]]; then
  echo "⚠️  docs-fera not found at: $DOCS_FERA_DIR"
  echo "    Set LOCAL_REPOS_ROOT to where your repos live, or clone docs-fera first."
  exit 1
fi
echo "✅ Found docs-fera at: $DOCS_FERA_DIR"

CURRENT_REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
echo "📍 Source conversation repo: $CURRENT_REPO_ROOT"
```

If the current repo **is** `docs-fera` itself, skip the cross-repo framing — the "propose in docs-fera" step becomes a local plan instead of a cross-repo one, but the Generalization Filter still applies (a fix made while working *in* docs-fera can still be project-specific to that one file/workflow rather than broadly reusable).

### 2. Harvest candidates from the conversation

Reuse the extraction logic from `/reva_review_active_conversation`: walk the conversation and list every fix, workaround, confusion point, and "I had to guess because the docs didn't say X" moment. Do not filter yet — over-collect at this stage.

```text
CANDIDATES (raw, unfiltered):
1. <one-line description> — <where it came from: tool call / user correction / error / confusion>
2. ...
```

### 3. Apply the Generalization Filter to every candidate

For each candidate from step 2, produce one line:

```text
[INCLUDE] <candidate> — <why it's reusable: which shared asset it affects and why other repos would hit it too>
[EXCLUDE] <candidate> — <why it's project-specific>
```

Every candidate from step 2 MUST appear exactly once in this list. No exceptions, no silent drops.

### 4. Map `INCLUDE` items to the correct `docs-fera` asset type

| Signal | Asset type | Location |
|---|---|---|
| A slash command is missing a step, has a stub body, or lacks guardrails | Command | `commands/*.md` (+ `commands/index_commands.yaml`) |
| An agent skill (`.cursor/skills/*`, `.claude/skills/*`) is ambiguous or missing a trigger case | Skill | skill's `SKILL.md` in the docs-fera skills registry |
| A maturity-stage workflow is missing a phase or ordering step | Mini prompt | `mini_prompt/lv*/*.md` |
| A how-to is missing, stale, or wrong | Guide | `guides/**/*.md` |
| A convention should be enforced, not just suggested | Standard | `standards/**/*.md` |
| A reusable snippet/example is worth promoting | Pattern | `patterns/**/*.md` |
| A guardrail belongs in `.cursor/rules` or `.claude` behavior | Rule | `rules/**/*.md` |
| A term is used inconsistently across docs/commands | Glossary | `glossaries/llm_ide_automation.md` |

For each `INCLUDE` item, write down: `<candidate> -> <asset type> -> <best-guess target path>`.

### 5. Search `docs-fera` before proposing a new file (extend over create)

For every mapped item, search first — creating a duplicate is worse than extending an existing file, and duplicates also risk 4-letter command-prefix collisions:

```bash
KEYWORD="<short keyword from the candidate>"

for d in guides standards patterns commands mini_prompt rules glossaries; do
  if [[ -d "$DOCS_FERA_DIR/$d" ]]; then
    MATCHES=$(grep -Ril -- "$KEYWORD" "$DOCS_FERA_DIR/$d" 2>/dev/null | head -n 20)
    if [[ -n "$MATCHES" ]]; then
      echo "📚 Existing candidates to extend in $d/:"
      echo "$MATCHES"
    fi
  fi
done

# If proposing a NEW command, the 4-letter prefix collision check is mandatory:
# python3 "$DOCS_FERA_DIR/_dev/scripts/commands/check_command_collisions.py"
```

Record, per item: **Extend** `<existing file>` **or** **Create new** `<proposed file>` — with a one-line justification for why extension wasn't possible if creating new.

### 6. Sanitize before anything touches `docs-fera`

Before drafting the plan, strip from every `INCLUDE` item's description:

- Project/product names, internal service names, tenant/customer identifiers.
- Ports, hostnames, URLs, table/column names, environment variable values.
- Secrets, tokens, credentials — even redacted-looking ones.
- Business terminology that only makes sense inside the source repo.

Rewrite each item in **tool/workflow-neutral language** — describe the shared asset that failed and how, not the business context that surfaced it.

### 7. Draft the plan file inside `docs-fera`

Target directory: `_dev/docs/plans/prioritized/` (docs-fera's own planning tree; fall back to `docs/plans/prioritized/` only if `_dev/docs/plans/` does not exist). Follow the naming convention in `templates/plan_management_system.md` (`{PRIORITY_PREFIX}_{EFFORT}_{IMPACT}_{SHORT_DESCRIPTION}.md`) and the mandatory dual effort estimate.

```bash
PLAN_DATE=$(date +%Y-%m-%d)
PLAN_FILE="$DOCS_FERA_DIR/_dev/docs/plans/prioritized/MI_LE_2h_MEDIUM_distill_docs_fera_improvements_${PLAN_DATE}.md"

cat > "$PLAN_FILE" << 'EOF'
# Distilled docs-fera Improvements

effort:
  ai_hours: 2
  human_hours: 1

## Source

- Originating repo/conversation: <sanitized description only — no project names/secrets>
- Command chain: /reva_review_active_conversation -> /dstl_distill_conversation_to_docs_fera

## Generalization Filter Results

### Included (reusable — proposed below)
- [ ] <item> — <why reusable>

### Excluded (project-specific — stays out of docs-fera)
- <item> — <why excluded>

## Proposed docs-fera Changes

### Commands
- Extend `commands/<file>.md`: <what changes>
  <!-- OR -->
- Create `commands/<new>.md`: <why extension wasn't possible; run collision checker>

### Skills / Mini Prompts / Guides / Standards / Patterns / Rules / Glossary
- <asset type>: Extend/Create `<path>` — <what changes>

## Search Evidence

- Searched: guides/, standards/, patterns/, commands/, mini_prompt/, rules/, glossaries/ for: <keywords>
- Result: <extend existing file X | no existing coverage found, creating new>

## Next Actions

1. Get user approval on this plan before editing docs-fera.
2. For command/skill changes: follow `guides/commands/command_authoring_best_practices.md` exactly (prefix collision check, COMMAND_ID/VERSION sync, no stub bodies).
3. For everything else: `/docu_document` (simple doc updates) or `/dlog_decision_log` (architecture-critical decisions).
4. Distribute per `guides/commands/cursor_commands_sync.md` if commands/skills changed — do NOT mass-distribute to other repos without explicit user authorization.

## Links

- Source conversation archive (if created): <link or "not archived">
- `/arch_archive` for this session's own WIP gate and closure
EOF

echo "📝 Distillation plan created: $PLAN_FILE"
```

### 8. Persist the plan — commit, push, open a PR

**"Do not implement" never meant "do not commit."** The no-implementation rule
protects the *proposed content* — commands, guides and standards that every repo
consumes. It says nothing about the plan document itself, which belongs in
`docs-fera`'s planning tree by definition.

A plan left untracked in a working tree is lost work waiting to happen: a
`git clean`, a branch switch, or simply a different session reclaiming the
checkout destroys it, and the analysis has to be redone from scratch. It is also
invisible to everyone else — which defeats the point, since the value of a
distillation is that a *future* occurrence can be matched against it.

```bash
cd "$DOCS_FERA_DIR"

# If the checkout is busy (another session's uncommitted work, or a branch that
# is not the default), do NOT switch it — work from an isolated worktree, a
# filesystem sibling of the main checkout:
#   git worktree add -b docs/distill-<date> ../docs-fera-wt-distill origin/main
# then copy the plan file into it. See guides/collaboration/multi_agent_worktree_workflow.md

git checkout -b "docs/distill-$(date +%Y-%m-%d)" origin/main   # never commit onto someone else's branch
git add "$PLAN_FILE"                                            # ONLY the plan file
git status --short                                              # confirm nothing else is staged
git commit -m "docs(plan): distilled docs-fera improvements from <date> session"
git push -u origin HEAD
gh pr create --fill --base main
```

Rules for this step:

- Stage **only** the plan file. Other untracked files in the planning tree
  usually belong to concurrent sessions — never sweep them in.
- Verify the file is actually tracked afterwards (`git ls-files <path>`): broad
  ignore patterns can exclude it silently, and `git add` will not always error.
- The PR body must state plainly that this is a **proposal**: no command, guide
  or standard was modified. Merging the plan does not implement anything.
- If a `docs-fera` branch other than the default is checked out, or the tree has
  another session's uncommitted work, use the worktree route above rather than
  switching branches under them.

### 9. Present the plan — do not auto-implement

Show the user the plan file's path, the PR link, and a summary of Included vs Excluded counts. Stop here. Implementation is a separate, explicitly-approved step (`/docu_document`, `/dlog_decision_log`, or direct command authoring), because writing into `docs-fera` affects every repo and agent that consumes it.

## Output Format

- A single markdown plan under `_dev/docs/plans/prioritized/` in `docs-fera`, using the structure in step 7, **committed on its own branch with an open PR**.
- Every candidate from step 2 accounted for under either "Included" or "Excluded" — counts must match.
- Every "Proposed docs-fera Changes" line names an exact target path and says **Extend** or **Create** (with justification for Create).

## Constraints

### Must Do

- Run the Generalization Filter explicitly on every candidate; show both Included and Excluded lists for auditability.
- Search existing `docs-fera` assets (step 5) before proposing any new file; prefer extending.
- Sanitize every item (step 6) before it is written anywhere under `docs-fera`.
- Output the result as a **plan** file only — never edit `docs-fera` commands/guides/standards directly in the same pass unless the user explicitly asks to implement immediately.
- **Commit, push and open a PR for the plan file itself** (step 8). Leaving it untracked is how the analysis gets destroyed by a branch switch or `git clean`. Committing a plan is not implementing it.
- Stage only the plan file, and confirm with `git ls-files` that it is tracked — ignore patterns can exclude it without an error.
- If a candidate proposes a new/changed command or skill, follow `guides/commands/command_authoring_best_practices.md` exactly, including the 4-letter prefix collision check.
- Default ambiguous candidates to **EXCLUDE** ("needs a second occurrence") rather than generalizing from a single data point.

### Must Not Do

- Must not copy project-specific code, config, secrets, or business terms verbatim into `docs-fera`.
- Must not create a new command/skill/guide/standard when an existing one can be reasonably extended.
- Must not silently drop a candidate — every item from step 2 must resolve to Included or Excluded.
- Must not mass-distribute the resulting change to other repositories — that requires explicit user authorization per the "No Mass Alterations" policy in `guides/commands/cursor_commands_sync.md`.
- Must not mark the resulting plan `Finished` without the WIP gate described in `/arch_archive`.

## Success Criteria

- [ ] Every conversation candidate is tagged Included or Excluded, with a one-line reason each.
- [ ] Every Included item is mapped to a concrete `docs-fera` asset type and target path.
- [ ] `docs-fera` was searched for an existing file to extend before any "Create new" proposal.
- [ ] All Included items are sanitized (no project-specific identifiers, secrets, or business terms).
- [ ] A single plan file exists under `_dev/docs/plans/prioritized/` (or `docs/plans/prioritized/`) summarizing the above.
- [ ] The plan file is **committed, pushed, and has an open PR** — not left untracked in a working tree.
- [ ] Nothing was implemented without explicit user approval.

## Related Commands

- `/reva_review_active_conversation` — upstream: extracts and classifies the raw conversation candidates this command filters.
- `/docu_document` — downstream: once the plan is approved, use it to write the actual README/AGENTS/guide updates.
- `/dlog_decision_log` — use instead of plain doc edits when an Included item is an architecture-critical decision, not a simple fix.
- `/cana_canonical_topic_alignment` — the inverse direction: pulls canon **from** `docs-fera` **into** the current repo. This command pushes learnings the other way.
- `/crcv_cross_repo_convergence` — use once a pattern is confirmed across two or more mature repos and needs an organization-wide standard, rather than a single conversation's lesson.
- `/ctra_capability_transplant_transfer` — use for transplanting a whole working capability/feature, not a lesson-sized improvement.
- `/arch_archive` — run for this session's own WIP gate and closure; link the resulting archive from the distillation plan's "Links" section.
- `guides/commands/command_authoring_best_practices.md` — required reading before any Included item proposes a new or changed command.

**Local Reference**: `commands/dstl_distill_conversation_to_docs_fera.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/dstl_distill_conversation_to_docs_fera.md`

--- End Command ---
