# /dlog_decision_log

<!-- COMMAND_ID: 012 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: dl_decision_log -->

Create (or update) an architecture-critical decision record with mandatory background research and a weighted decision matrix. The output is a timestamped ADR stored under the repository’s decisions directory (`_dev/docs/decisions/` for `*-fera`, otherwise `docs/decisions/`), plus backlinks in the inventory.

Backlinks:

- **Local Reference**: `_dev/docs/decisions/README.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/_dev/docs/decisions/README.md
- **Local Reference**: _dev/docs/decisions/decision_record.template.md
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/_dev/docs/decisions/decision_record.template.md
- **Local Reference**: _dev/docs/inventory/decisions/README.md
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/_dev/docs/inventory/decisions/README.md

## Command sequence (run in order)

1. **Confirm repository context**

   bash
   gtimeout 5 git rev-parse --show-toplevel
   ```

2. **Resolve decision log directory**

   ```bash
   cat <<'EOF' > .tmp/resolve_decision_dir.sh
   #!/usr/bin/env bash
   set -euo pipefail
   REPO_ROOT="$(git rev-parse --show-toplevel)"
   REPO_NAME="$(basename "$REPO_ROOT")"
   if [[ "$REPO_NAME" == *-fera ]]; then
     DECISION_DIR="$REPO_ROOT/_dev/docs/decisions"
   else
     DECISION_DIR="$REPO_ROOT/docs/decisions"
   fi
   printf '%s\n' "$DECISION_DIR"
   EOF
   chmod +x .tmp/resolve_decision_dir.sh
   gtimeout 5 .tmp/resolve_decision_dir.sh
   ```

   - Create the directory when it does not exist yet:
     ```bash
     DECISION_DIR_PATH="$(.tmp/resolve_decision_dir.sh)"
     gtimeout 5 mkdir -p "$DECISION_DIR_PATH"
     ```

3. **Capture current context before researching**

   ```bash
   gtimeout 5 git status --short
   ```

   - Summarize the conversation goal, blockers, and decision scope in your own words (keep this summary handy for the ADR “Problem Statement” section).

4. **Identify existing guidance + prior decisions**

   - Search related documentation to understand constraints before proposing options:
     ```bash
     gtimeout 10 rg -n "<keyword>" standards/ guides/ rules/ | head -40
     ```
   - List relevant decision history:
     ```bash
     gtimeout 5 ls -1 "$DECISION_DIR_PATH" | head -40
     ```
   - Use `project_index.yaml` or plan inventories to discover impacted components.

5. **Perform background research (at least three sources)**

   - Collect internal sources (standards, rules, incidents) and any vetted external references.
   - For each source, capture:
     1. Evidence / key finding
     2. How it influences the repository
     3. Where it lives (provide both reference formats per docs-fera rule)
   - Example transcription inside the ADR:
     ```
     - **Local Reference**: `standards/project/project_structure_standard.md`
       **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/project/project_structure_standard.md


6. **Define options**

   - Enumerate at least two realistic approaches.
   - For each option list effort, expected benefits, risks, and any prerequisites discovered during research.

7. **Build the decision matrix**

   - Choose 4–6 evaluation factors that reflect the decision drivers.
   - Assign normalized weights that sum to **1.00** (or 100% if you prefer percentages, but keep the math explicit).
   - Score each option on a consistent 1–5 (or 1–10) scale where higher is better.
   - Compute weighted scores: Σ(weight × score)` per option.
   - The winning option **must** be the one with the highest weighted score. If there is a tie, document the tie-breaker analysis.

8. **Instantiate the ADR from the template**

   - Create filename and copy template:
     ```bash
     DECISION_FILE="$(date -u +%Y-%m-%d)_<slug>.md"
     gtimeout 5 cp "$DECISION_DIR_PATH/decision_record.template.md" "$DECISION_DIR_PATH/$DECISION_FILE"
     ```
     Replace `<slug>` with a concise, kebab-case descriptor (no spaces). Edit the new file and fill every section:
     - Background Research table populated with the sources from step 5
     - Options section detailing each alternative
     - Decision Matrix table with factors, weights, scores, and weighted totals
     - Decision section explicitly referencing the highest weighted score
     - Consequences and follow-up tasks

9. **Cross-link inventories**

   - Append the new decision to `_dev/docs/decisions/README.md` (list entry) and, if applicable, log it under `_dev/docs/inventory/decisions/`.
   - Reference any related plans, commands, or rules using the dual-reference format.

10. **Surface the result**
    - Summarize the winning option, weighted score, and follow-up actions in the conversation so reviewers can quickly see the outcome.
    - Stage documentation updates when ready (`git add`) and proceed with `/docu_document` or `/gsyn_git_sync` workflows as needed.

## Notes

- The ADR is incomplete unless both the **Background Research** section and the **Decision Matrix** table are filled with evidence-driven data.
- If a decision revises a previous record, update the older ADR’s status (e.g., Superseded) and link both files.
- Keep calculations transparent—include intermediate math or a short appendix when using complex scoring.
- Do not skip inventory updates; they are how other agents discover prior decisions before proposing new changes.
