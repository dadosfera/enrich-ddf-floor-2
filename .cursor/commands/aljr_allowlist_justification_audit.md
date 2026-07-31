---
# Dadosfera Metadata
category: general
criticality: medium
scope: all
commandId: "085"
version: "1.0.0"
type: "qa_allowlist_justification_audit"
canonical: "docs-fera@/commands/aljr_allowlist_justification_audit.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/aljr_allowlist_justification_audit.md"
backlinks:
  - "_dev/hooks/README.md"
  - "guides/distribution/distribution_workflow_unified.md"
  - "standards/hooks/hook_distribution_standard.md"

# Claude Code Metadata
name: "Allowlist Justification Audit"
description: "Audit allowlist entries and ensure each has documented justification"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 085 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: qa_allowlist_justification_audit -->
# /aljr_allowlist_justification_audit

**Command**: `/aljr_allowlist_justification_audit`

Audit and challenge accumulated allowlists/exceptions (especially in hooks and validators). **Exceptions are a last resort**: if you added an allowlist entry, you must justify why you did not fix the underlying issue.

## Purpose

- **Prevent allowlist creep**: allowlists tend to grow forever and silently weaken enforcement.
- **Enforce "fix-first" discipline**: the default must be "fix the problem", not "skip the check".
- **Require justification per entry**: every allowlist/exception must have a concrete reason, bounded scope, and a removal plan.

## When to Use

- A hook/validator got "unblocked" by adding allowlists/excludes/skips.
- CI/pre-commit started accumulating `exclude`, `ignore`, `skip`, or "allowlist" entries over time.
- A new repository rule is being introduced and there is pressure to "just add an exception".

## When NOT to Use

- You already have a concrete reproduction and you are actively fixing the underlying bug (use a debug/fix command instead).
- This is a pure documentation-only change with no enforcement surface.

## Command Sequence

**Constraint**: This is a **read-only audit**. Do not edit or apply changes while running this command. Output a report with findings + recommended next actions.

### 1) Build an "exceptions inventory" (search + collect)

Search the repo for common allowlist/exception patterns and collect them into an inventory list (file → line → entry → nearby comment).

**Search targets (minimum):**
- Hooks: `_dev/hooks/`
- Hook cores: `_dev/hooks/core/`
- Pre-commit config: `.pre-commit-config.yaml` (and any `config/pre-commit-*.yaml` if present)
- Shared hooks (if present): `scripts-fera/hooks/`
- Validation scripts likely to carry allowlists: `_dev/scripts/`, `scripts/`

**Search patterns (start broad, then refine):**

```bash
gtimeout 10 rg -n --hidden -S "(^|\\b)(ALLOWLIST|ALLOW_LIST|EXCEPTION|EXCEPTIONS|SKIP|SKIPS|IGNORE(D)?_DIRS|EXCLUDE(D)?|exclude_patterns|exclude:|ignore:|--exclude|--ignore|pass_filenames:\\s*false)(\\b|$)" .
```

**Inventory rule**:
- For each hit, capture **3–10 lines of context** above/below to see whether there is a justification comment.

### 2) For each allowlist/exception entry, run the "No Lazy Exceptions" interrogation

For every allowlist entry found, answer the questions below.

**Hard rule**: If you cannot answer these clearly, the exception is not acceptable.

**Interrogation questions (required):**
- **What broke?** What is the exact failure you were trying to avoid (error message, failing rule/hook, and a minimal reproduction)?
- **Why not fix it?** Why was the underlying issue not fixed instead of adding an exception?
- **Why is an exception justified?** What hard constraint prevents a real fix right now (upstream bug, missing dependency, known false-positive, performance wall)?
- **How is it bounded?** Is the exception as narrow as possible (single path, exact file, exact pattern) rather than a broad wildcard?
- **What is the risk?** What enforcement is being weakened (security, governance, quality, taxonomy), and what could slip through?
- **What is the removal plan?** Link to a plan/task/issue and define a **sunset condition** (and ideally a date).
- **What evidence exists?** Show logs/tests that demonstrate the exception is needed and that the bounded scope is correct.

**Reasoning checkpoint (must be stated in the report):**
- "Why did you add exceptions instead of fixing them?"
- "Exceptions are only a last resort — don't be lazy."

### 3) Cross-check for redundancy, overlap, and hidden weakening

Review the full inventory and detect:
- **Duplicate entries** (same path/pattern repeated across scripts/configs)
- **Overlapping entries** where a broad pattern makes smaller ones meaningless
- **Contradictory intent** (e.g., a validator enforces a rule but another allowlist bypasses it broadly)
- **Unbounded scope** (glob patterns like `**/*` style, directory-wide skips, or "ignore everything under X" without strong reason)

### 4) Produce a "keep / tighten / remove / replace-with-fix" verdict per entry

For each entry, classify one of:
- **KEEP (justified)**: bounded + justified + removal plan exists
- **TIGHTEN**: justified but too broad → propose a narrower pattern
- **REMOVE**: no longer needed or unjustified
- **REPLACE WITH FIX**: exception exists but the underlying issue should be fixed now

## Output Format

```markdown
## Allowlist / Exceptions Audit

### Summary
- **Total allowlist/exception hits**: N
- **With explicit justification**: A
- **Missing justification**: B
- **High-risk exceptions (security/governance)**: C

### Inventory (by file)

#### `<file_path>`
- **Entry**: `<exact allowlist / exclude / skip item>`
  - **Context**: `<rule/hook it affects>`
  - **Justification present**: ✅/⚠️ (quote the justification line if present)
  - **Interrogation answers**:
    - What broke: …
    - Why not fix: …
    - Why exception is justified: …
    - How bounded: …
    - Risk: …
    - Removal plan + sunset: …
    - Evidence: …
  - **Verdict**: KEEP / TIGHTEN / REMOVE / REPLACE WITH FIX

### Findings
- …

### Non-Negotiable Principles (restate)
- "Why did you add exceptions instead of fixing them?"
- "Exceptions are only a last resort — don't be lazy."
```

## Notes

- This command is intentionally judgmental: allowlists degrade standards unless aggressively justified.
- Prefer durable fixes over exceptions: improve detection logic, reduce false positives, scope checks by file type, or update the underlying rule.
- If a temporary exception is unavoidable, it must be **bounded**, **documented**, and **tracked to removal**.

---

**Local Reference**: `commands/aljr_allowlist_justification_audit.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/aljr_allowlist_justification_audit.md`

End Command ---
