---
# Dadosfera Metadata
category: infrastructure
criticality: medium
scope: all
commandId: "086"
version: "1.0.0"
type: "df_dotfiles_ignore_audit"
canonical: "docs-fera@/commands/digr_dotfiles_ignore_audit.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/digr_dotfiles_ignore_audit.md"
backlinks:
  - "guides/development/ignore-files-git-cursor-dadosfera.md"
  - "guides/distribution/distribution_workflow_unified.md"
  - "_dev/workflows/distribution/dotfiles/README.md"
  - "docs/plans/active/dotfile_distribution_agent_instructions.md"

# Claude Code Metadata
name: "Dotfiles Ignore Audit"
description: "Audit dotfile ignore rules for consistency across .gitignore, .cursorignore, etc."
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 086 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: df_dotfiles_ignore_audit -->
# /digr_dotfiles_ignore_audit

**Command**: `/digr_dotfiles_ignore_audit`

Audit dotfiles ignore configuration (Git vs Cursor vs Dadosfera) with special focus on the distinction between **indexing-only ignores** (`.{cursor,dadosfera}indexingignore` / `.dadosferaindexignore`) and **strong ignores** (`.{cursor,dadosfera}ignore`) that can block agent access. Ensures changes are applied via the **dotfiles distribution workflow** (templates + installer + pending review gate), not via ad-hoc edits.

## Purpose

- **Stop accidental blocking**: avoid patterns in `.cursorignore` / `.dadosferaignore` that block AI reads/writes for files we still need.
- **Keep indexing fast without breaking access**: move "performance-only" patterns into `.cursorindexingignore` / `.dadosferaindexingignore`.
- **Enforce distribution discipline**: dotfiles should be updated via templates + installer (`install_dotfiles.sh`) using the pending review gate.

## When to Use

- Someone adds a broad pattern to `.cursorignore` / `.dadosferaignore` and the agent starts seeing "filtered out by ignore".
- `.vscode/**`, `.idea/**`, or `.cursor/settings.json` are being blocked (these usually belong to indexing-only ignores).
- A repo's ignore files drifted from canonical templates and need reconciliation.
- Before cross-repo dotfiles distribution (to avoid spreading a bad pattern everywhere).

## When NOT to Use

- You are changing dotfile templates themselves (use the dotfiles distribution workflow directly and include human review).

## Command Sequence

**Constraint**: This is an **audit command**. Do not directly edit dotfiles as part of the audit. If changes are needed, route them through the dotfiles distribution workflow.

### 1) Identify repo type (fera vs non-fera) and gather current dotfiles

Determine whether the repository is `-fera` and gather current dotfiles if they exist:
- `.gitignore`
- `.cursorignore`
- `.cursorindexingignore`
- `.dadosferaignore`
- `.dadosferaindexingignore` (or alias `.dadosferaindexignore`)

### 2) Apply the canonical decision table (indexing-only vs strong ignore)

Use the rules from `guides/development/ignore-files-git-cursor-dadosfera.md`:

- `.cursorignore` / `.dadosferaignore`:
  - blocks indexing **and** can block agent access
  - reserve for **heavy/generated/binary/secrets**
  - avoid for IDE/editor config that we may need to read/edit

- `.cursorindexingignore` / `.dadosferaindexingignore`:
  - indexing-only (keeps files accessible when explicitly referenced)
  - use for IDE/editor config and local noise

**Red flags (must be called out):**
- Broad wildcards (example: `*_auto.*`) placed in `.cursorignore` (can block legitimate docs/commands; see guide)
- IDE/editor config patterns in `.cursorignore` instead of indexing-only ignore
- Missing navigation allowlists in `.cursorignore` / `.dadosferaignore` (README/AGENTS/docs/project index)

### 3) Verify "navigation allowlist" safety invariants

Confirm `.cursorignore` / `.dadosferaignore` maintain navigation allowlists so agents can still traverse documentation:
- allow access to `project_index.yaml` (or equivalent index)
- allow access to `**/README.md` and `**/AGENTS.md`
- allow access to documentation trees (commonly `docs/**` in repos that have it)

If those allowlists are missing, treat it as a **critical** issue because it breaks repo navigation.

### 4) Compare against canonical templates (don't patch instances directly)

If running inside `docs-fera`, compare repo dotfiles to the templates:
- -fera templates: `templates/fera/*.template`
- non-fera templates: `templates/non_fera/*.template`

If running in a target repo (not docs-fera), use the **dotfiles distribution workflow**:
- Use installer to generate pending candidates, then review:

```bash
# Preview changes safely
bash _dev/workflows/distribution/dotfiles/installers/install_dotfiles.sh --dry-run

# Generate *.pending.template candidates (review gate)
bash _dev/workflows/distribution/dotfiles/installers/install_dotfiles.sh
```

**Promotion rule (human review gate)**:
- Only after review, promote:

```bash
bash _dev/workflows/distribution/dotfiles/installers/install_dotfiles.sh --promote
```

### 5) Produce a concrete audit report + migration guidance

Summarize:
- which patterns are in the wrong file (should move from `.cursorignore` → `.cursorindexingignore`, or `.dadosferaignore` → `.dadosferaindexingignore`)
- which patterns are too broad/risky and need tightening + explicit allowlists
- how to apply the fix via **template + installer + pending review gate** (per `guides/distribution/distribution_workflow_unified.md`)

## Output Format

```markdown
## Dotfiles Ignore Audit

### Files Present
- `.gitignore`: ✅/⚠️ missing
- `.cursorignore`: ✅/⚠️ missing
- `.cursorindexingignore`: ✅/⚠️ missing
- `.dadosferaignore`: ✅/⚠️ missing
- `.dadosferaindexingignore` / `.dadosferaindexignore`: ✅/⚠️ missing

### Key Distinctions (must restate)
- `.cursorignore` / `.dadosferaignore` = strong ignore (indexing + may block agent access)
- `.cursorindexingignore` / `.dadosferaindexingignore` = indexing-only ignore

### Findings
- **Blocking-risk patterns in strong ignore**: …
- **IDE/editor config incorrectly blocked**: …
- **Broad wildcard risks (e.g., `*_auto.*`)**: …
- **Navigation allowlist status**: ✅ present / ❌ missing

### Recommended Fix Path (distribution workflow)
- **Do not edit instances directly**.
- Update templates (`templates/{fera,non_fera}/`) and run installer:
  - `install_dotfiles.sh --dry-run`
  - `install_dotfiles.sh` (creates `*.pending.template`)
  - human review
  - `install_dotfiles.sh --promote`
```

## Notes

- This command is explicitly aligned with:
  - the ignore-files guide (`guides/development/ignore-files-git-cursor-dadosfera.md`)
  - the dotfiles distribution workflow (template + installer + pending review gate) in `guides/distribution/distribution_workflow_unified.md`
- The goal is to keep repos fast **without** breaking AI navigation and without spreading risky patterns via distribution.

---

**Local Reference**: `commands/digr_dotfiles_ignore_audit.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/digr_dotfiles_ignore_audit.md`

End Command ---
