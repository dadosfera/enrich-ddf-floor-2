# /cprs_commits_prs_rules_analysis
<!-- COMMAND_ID: 061 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: qr_rules_review -->

Analyze the last 1000 commits (in 10 chunks of 100) and the last 100 PRs, then identify recurring mistakes and propose improvements to `.cursor/rules/` (or the repo’s rules source-of-truth, if `.cursor/rules/` is generated).

Backlinks:

- **Local Reference**: `rules/cursor/4_23_rule_distribution_discipline.mdc`

  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/rules/cursor/4_23_rule_distribution_discipline.mdc`
- **Local Reference**: `guides/rule_distribution_workflow.md`

  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/guides/rule_distribution_workflow.md`
- **Local Reference**: `guides/distribution_workflow_unified.md`

  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/guides/distribution_workflow_unified.md`
- **Local Reference**: `commands/lint_lint.md`

  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/lint_lint.md`

## Notes (read this before running anything)

- This is an **analysis-first** command. Default outcome is a report + recommended rule changes (not edits).
- If `.cursor/rules/` is **generated**, do **not** edit it directly. Update the source-of-truth (in `docs-fera`, that’s `rules/json/core/*.json`) and run the repo’s rule distribution workflow (in `docs-fera`, `bash workflows/rule_distribution/build_all_from_json.sh`).
- If you detect a mistake pattern that is “rules-appropriate” but **not enforceable** via rules, capture it as a process/guide improvement instead.

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Create an output workspace (ephemeral)

```bash
RUN_TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR=".tmp/cprs_rules_analysis_${RUN_TS}"
gtimeout 5 mkdir -p "$OUT_DIR"
echo "OUT_DIR=$OUT_DIR"
```

3. Snapshot current rules state (what exists today)

```bash
gtimeout 5 test -d ".cursor/rules" && echo "OK: .cursor/rules exists" || echo "WARN: .cursor/rules missing"
gtimeout 10 find ".cursor/rules" -type f 2>/dev/null | sort > "$OUT_DIR/cursor_rules_files.txt" || true
gtimeout 10 find "rules/json/core" -type f 2>/dev/null | sort > "$OUT_DIR/rules_json_core_files.txt" || true
gtimeout 10 find "rules/cursor" -type f 2>/dev/null | sort > "$OUT_DIR/rules_cursor_files.txt" || true
```

4. Collect last 1000 commits (10 chunks of 100)

```bash
# Chunk 1 is most recent; chunk 10 is oldest in the last 1000.
for i in $(seq 0 9); do
  SKIP=$((i*100))
  CHUNK_NUM=$((i+1))
  OUT_FILE="$OUT_DIR/git_commits_chunk_${CHUNK_NUM}_skip_${SKIP}.txt"
  echo "Writing $OUT_FILE"
  gtimeout 60 git log --max-count 100 --skip "$SKIP" --date=iso-strict --pretty=format:'%H|%ad|%an|%s' --name-status > "$OUT_FILE"
  sleep 0.2
done
```

5. Collect last 100 PRs (requires GitHub CLI)

```bash
gtimeout 5 gh --version
gtimeout 10 gh auth status

# Save PR list JSON (last 100 PRs, any state)
gtimeout 60 gh pr list --limit 100 --state all --json number,title,url,author,createdAt,mergedAt,closedAt,labels > "$OUT_DIR/prs_last_100.json"
```

Optional deep fetch (slower; use when PR titles/bodies are insufficient evidence):

```bash
gtimeout 5 jq --version

PR_NUMS=$(jq -r '.[].number' "$OUT_DIR/prs_last_100.json" | head -100)
for n in $PR_NUMS; do
  OUT_FILE="$OUT_DIR/pr_${n}.json"
  echo "Writing $OUT_FILE"
  gtimeout 90 gh pr view "$n" --json number,title,url,author,body,createdAt,mergedAt,closedAt,labels,reviews,comments,files > "$OUT_FILE" || true
  sleep 0.2
done
```

6. Extract “common mistakes” evidence (fast heuristic search)

```bash
# Optional, but strongly recommended to speed up analysis.
gtimeout 5 rg --version

gtimeout 20 rg -n \
  "pre-commit|hook|distribution|rule_distribution|cursor rule|\\.cursor/rules|rules/json/core|index_commands\\.yaml|project_index\\.yaml|AGENTS\\.md|README\\.md|template|\\.template|taxonomy|lint|ruff|shellcheck" \
  "$OUT_DIR" \
  > "$OUT_DIR/keyword_hits.txt" || true

gtimeout 5 wc -l "$OUT_DIR/keyword_hits.txt" 2>/dev/null || true
```

7. Analyze and propose `.cursor/rules/` improvements (manual reasoning; document with evidence)

- For each recurring mistake, capture:
  - **Symptom**: what people did wrong
  - **Evidence**: commit hashes and/or PR numbers where it happened
  - **Impact**: what broke (pre-commit, CI, distribution drift, confusing docs, wrong paths)
  - **Current rule coverage**: where (if anywhere) the rule already exists today (file path)
  - **Proposed rule improvement**: what to change/add (rule title + concrete additions/examples)
  - **Enforcement leverage**: can a rule prevent it, or do we need a guide/hook/test?

8. Write the report (recommended location: `analysis/`)

```bash
DATE="$(date +%Y-%m-%d)"
REPORT_PATH="analysis/CURSOR_RULES_COMMON_MISTAKES_${DATE}.md"
echo "$REPORT_PATH"
```

Use this minimal template:

```markdown
### Summary
- Scanned: last 1000 commits (10×100) + last 100 PRs
- Output dir: <paste OUT_DIR>

### Top recurring mistakes (ranked)
1. <mistake>
   - Evidence: <commit hash(es)>; PRs: <#123, #456>
   - Current rule coverage: <path or "missing">
   - Proposed rule improvement: <specific change>

### Proposed changes (rules source-of-truth)
- <rule file / JSON source>:
  - <change>

### Follow-ups
- <optional: plan to implement rule updates and run distribution>
```

---

**Last updated**: 2025-12-27






