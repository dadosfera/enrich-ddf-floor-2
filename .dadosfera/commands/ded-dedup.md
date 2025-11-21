# /ded-dedup

Run a safe, dry‑run deduplication sweep over repository files using the canonical file‑level deduplication workflow from `dadosfera/workflows-fera`. This command only detects and reports likely duplicates; it does **not** delete, move, or rename any files.

Backlinks:

- `mini_prompt/lv1/deduplication_check_mini_prompt.md`
- `mini_prompt/lv1/duplicate_tests_checker_mini_prompt.md`
- `mini_prompt/lv1/safe_file_organization_and_movement_mini_prompt.md`
- `mini_prompt/lv1/plans_consolidation_merging_deduplication_mini_prompt.md`
- `guides/project_taxonomy.md`
- `guides/project_structure_ontology.md`
- `templates/run_main_entry_point.md`
- `templates/meta_plan_template.md`

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
sleep 1
```

2. (Optional but recommended) Verify taxonomy compliance in the current repo

```bash
if [ -x "./scripts/prevent_wrong_taxonomy.sh" ]; then
  gtimeout 10 ./scripts/prevent_wrong_taxonomy.sh || true
  sleep 1
fi
```

3. (Optional) Run repo‑local dedupe helper (from `scripts-fera`) if available

```bash
if [ -x "./scripts/dedupe.sh" ]; then
  echo "Running repo-local dedupe helper: scripts/dedupe.sh"
  gtimeout 30 bash ./scripts/dedupe.sh
  sleep 1
else
  echo "Repo-local dedupe helper (scripts/dedupe.sh) not found; skipping."
fi
```

4. Locate the dedup workflow entrypoint from `workflows-fera`

```bash
DEDUP_WRFLW="4_workflows/workflow_management/common_complex_wrkflws/file_management/deduplication/deduplicate_files_wrflw.sh"

if [ -x "$DEDUP_WRFLW" ]; then
  echo "Found dedup workflow: $DEDUP_WRFLW"
else
  echo "Dedup workflow not found locally. Ensure workflows-fera is available or mounted. Skipping execution."
fi
sleep 1
```

5. Choose scope, whitelist, and outputs

- **ROOT_DIR** (optional): directory to scan for duplicates (default: `.`)
- **WHITELIST_JSON** (optional): JSON file with ignore patterns/directories
  - Keys: `patterns` (array of globs), `directories` (array of paths)
- **OUTPUT_DIR / OUTPUT_FILE**: where the dedup report will be written

```bash
ROOT_DIR="${ROOT_DIR:-.}"
OUTPUT_DIR="analysis"
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/dedup_report.json"
WHITELIST_JSON="${WHITELIST_JSON:-}"  # optional path
```

6. Run dedup in dry‑run mode (no file changes)

```bash
if [ -x "$DEDUP_WRFLW" ]; then
  CMD=(bash "$DEDUP_WRFLW" --auto-depth --auto-depth-threshold 100 \
       --dry-run --directory "$ROOT_DIR" --output "$OUTPUT_FILE")
  if [ -n "$WHITELIST_JSON" ] && [ -f "$WHITELIST_JSON" ]; then
    CMD+=(--whitelist "$WHITELIST_JSON")
  fi

  echo "Running: ${CMD[*]}"
  gtimeout 30 "${CMD[@]}"
  sleep 1
else
  echo "Skipping dedup execution (workflow not present)."
fi
```

7. Inspect report (read‑only)

```bash
if [ -f "$OUTPUT_FILE" ]; then
  echo "Deduplication report written to $OUTPUT_FILE"
else
  echo "No deduplication report generated"
fi
```

## Notes

- **Read‑only**: `/dedup` is strictly a detection/reporting flow. It must not delete, move, or rename any files.
- Use whitelist patterns to avoid flagging intentional copies (fixtures, vendored code, build artifacts, generated docs).
- For **tests‑only** sweeps, prefer the dedicated duplicate tests checker mini prompt (`mini_prompt/lv1/duplicate_tests_checker_mini_prompt.md`), which writes `analysis/tests_dedup/tests_dedup_report.{json,csv}`.
- When acting on duplicates (merging/removal), use the safe file movement/taxonomy mini prompt (`mini_prompt/lv1/safe_file_organization_and_movement_mini_prompt.md`) and follow taxonomy checks before and after changes.
- In repos that vendor helpers from `scripts-fera`, `scripts/dedupe.sh` is the preferred quick health-check wrapper (see `scripts-fera/scripts/utilities/deduplication/dedupe.sh`); this command treats it as an optional first pass before calling the lower-level `workflows-fera` pipeline.
- Treat the JSON report as a **repo-wide input**: when you later open a conversation about dedupe results, use that conversation with `/review` and `/archive` as usual if you want to turn chosen actions into plans, but `/dedup` itself is not conversation-scoped.
- For duplicate or overlapping plans/docs discovered from the report, the dedicated entrypoint is `mini_prompt/lv1/plans_consolidation_merging_deduplication_mini_prompt.md`, which operates over planning docs directly and is not tied to a single `/review` or `/archive` run.
 - Standard whitelist location/shape:
   - Template: `config/dedup_whitelist.json.template` (checked into `docs-fera`).
   - Per-repo copy: `config/dedup_whitelist.json` with `patterns` and `directories` keys as documented in `guides/deduplication_guide.md`.

## Usage examples

- **Full-repo scan (default ROOT_DIR)**

  ```bash
  # From the repo root, run /dedup in Cursor (no extra env needed)
  # ROOT_DIR defaults to the entire repository: "."
  ```

- **Scan only tests/**

  ```bash
  # Limit the sweep to tests/ (e.g., before running the duplicate tests checker)
  export ROOT_DIR="tests"
  # Then invoke /dedup from the command palette
  ```

- **Scan only guides/**

  ```bash
  # Focus on documentation duplication under guides/
  export ROOT_DIR="guides"
  # Then invoke /dedup from the command palette
  ```

- **Use a whitelist JSON to ignore known duplicates**

  ```bash
  # Example whitelist file managed in your repo
  export WHITELIST_JSON="config/dedup_whitelist.json"
  # Optional: also scope to a subdirectory
  export ROOT_DIR="."
  # Then invoke /dedup from the command palette
  ```

  Example `config/dedup_whitelist.json` structure:

  ```json
  {
    "patterns": [
      "docs/**/generated/**",
      "tests/**/fixtures/**"
    ],
    "directories": [
      "node_modules",
      "dist"
    ]
  }
  ```

In all cases, `/dedup` writes its primary JSON output to `analysis/dedup_report.json`, which you can inspect or feed into later planning conversations.

## Relationship to other commands and workflows

- **`/dedup` (this command)**: Repo/path-scoped deduplication detector. It can run at any time, independent of a particular conversation, and only ever reports duplicates (no moves/deletes).
- **`scripts/dedupe.sh` (from `scripts-fera`)**: Optional, repo-local helper that runs as a quick health-check wrapper, often used by `workflows/run.sh`. `/dedup` uses it when present, then calls the lower-level `deduplicate_files_wrflw.sh` pipeline.
- **`workflows-fera` dedup pipeline (`deduplicate_files_wrflw.sh`)**: Canonical engine that performs the actual file-level dedup analysis; `/dedup` is a thin, repo-aware front-end for this pipeline.
- **`/review`**: Conversation-scoped analysis that turns what happened in a single conversation (including any decisions about acting on dedup results) into a structured task list. It does not run dedup itself and does not read `analysis/dedup_report.json` automatically.
- **`/archive`**: Another conversation-scoped command that consumes `/review` tasks routed to backlog/prioritized plans when you are closing out a journey. It also does not run dedup directly.
- **`mini_prompt/lv1/plans_consolidation_merging_deduplication_mini_prompt.md`**: Dedicated workflow for consolidating and deduplicating planning docs themselves (e.g., overlapping plans), operating over `docs/plans/**` rather than the raw repo tree.

`/dedup` is therefore **repo/path-scoped and not conversation-scoped**: it produces artifacts (like `analysis/dedup_report.json`) that later conversations can reference, but it does not depend on or modify any particular conversation workflow.
