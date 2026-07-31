---
# Dadosfera Metadata
category: documentation
criticality: high
scope: all
commandId: "083"
version: "1.0.0"
type: "ca_canonical_topic_alignment"
canonical: "docs-fera@/commands/cana_canonical_topic_alignment.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/cana_canonical_topic_alignment.md"
backlinks:
  - "guides/diagrams.md"
  - "guides/distribution/distribution_workflow_unified.md"
  - "standards/hooks/hook_distribution_standard.md"
  - "mini_prompt/lv0/mermaid_best_practices_alignment_lv0_mini_prompt.md"
  - "mini_prompt/lv1/mermaid_best_practices_alignment_lv1_mini_prompt.md"
  - "mini_prompt/lv2/mermaid_best_practices_alignment_lv2_mini_prompt.md"
  - "mini_prompt/lv3/mermaid_best_practices_alignment_lv3_mini_prompt.md"
  - "mini_prompt/lv4/mermaid_best_practices_alignment_lv4_mini_prompt.md"
  - "mini_prompt/lv5/mermaid_best_practices_alignment_lv5_mini_prompt.md"

# Claude Code Metadata
name: "Canonical Topic Alignment"
description: "Align topics to canonical references and resolve naming conflicts"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 083 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ca_canonical_topic_alignment -->
# /cana_canonical_topic_alignment

**Command**: `/cana_canonical_topic_alignment`

## Purpose

Audit and align the current repository with **canonized practices from `docs-fera`** for a chosen **topic** (default: `mermaid`), using:

- `docs-fera@ guides/` (how-to and recommended workflows)
- `docs-fera@ standards/` (best practices / enforceable conventions)
- `docs-fera@ patterns/` (reusable patterns and examples)
- `docs-fera@ decisions/` (rationales and non-obvious constraints)

This command keeps the existing **mermaid-specific** checks when `TOPIC=mermaid`, but is **not limited to mermaid**.

## Default topic

- **Default**: `TOPIC=mermaid`
- Override by exporting `TOPIC` before running the steps (examples below).

## When to Use

- New repository setup requiring canonized standards/patterns
- Existing repository audit for topic best practices compliance
- After identifying unsync evolutions from canonical Dadosfera repositories
- When topic-specific docs, practices, or patterns need validation and improvement
- When documentation or tooling gaps are identified

## When NOT to Use

- For simple documentation authoring (use `/docu_document` instead)
- For general documentation structure audit (use `/dcon_docs_structure_audit` instead)
- For cross-repo standardization program management (use `/crcv_cross_repo_convergence` instead)

## Command Sequence (run in order)

### 1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

### 2. Identify canonical source repositories + set topic

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
CANONICAL_REPOS="deployer-ddf docs-fera scripts-fera"
LOCAL_REPOS_ROOT="${LOCAL_REPOS_ROOT:-$HOME/local_repos}"

# Topic to align (default: mermaid). Examples:
# TOPIC="mermaid"
# TOPIC="git hooks"
# TOPIC="distribution workflow"
# TOPIC="index yaml"
TOPIC="${TOPIC:-mermaid}"
```

### 3. Check canonical repos exist locally

```bash
for repo in $CANONICAL_REPOS; do
  if [[ -d "$LOCAL_REPOS_ROOT/$repo" ]]; then
    echo "✅ Found canonical repo: $repo"
  else
    echo "⚠️  Canonical repo not found locally: $repo"
  fi
done

DOCS_FERA_DIR="$LOCAL_REPOS_ROOT/docs-fera"
SCRIPTS_FERA_DIR="$LOCAL_REPOS_ROOT/scripts-fera"
echo "🔎 Topic: $TOPIC"
```

### 4. Extract topic canon from `docs-fera` (guides + standards + patterns + decisions)

```bash
if [[ ! -d "$DOCS_FERA_DIR" ]]; then
  echo "⚠️  docs-fera not found at: $DOCS_FERA_DIR"
  echo "    Set LOCAL_REPOS_ROOT to where your repos live (default: $HOME/local_repos)."
else
  echo "✅ Found docs-fera at: $DOCS_FERA_DIR"

  # NOTE: People sometimes refer to a \"best_practices\" folder; in docs-fera the canon is usually:
  # - standards/ (best practices / enforceable conventions)
  # - patterns/  (examples and reusable patterns)
  SEARCH_DIRS=(
    "$DOCS_FERA_DIR/guides"
    "$DOCS_FERA_DIR/standards"
    "$DOCS_FERA_DIR/patterns"
    "$DOCS_FERA_DIR/decisions"
  )

  echo "🔍 Searching docs-fera canon for topic matches..."
  for d in "${SEARCH_DIRS[@]}"; do
    if [[ -d "$d" ]]; then
      COUNT=$(grep -Ril -- "$TOPIC" "$d" 2>/dev/null | wc -l | tr -d ' ')
      echo "📚 $(basename "$d")/: $COUNT file(s) mention '$TOPIC'"
    fi
  done

  echo ""
  echo "🔗 Top matching files (first 30):"
  for d in "${SEARCH_DIRS[@]}"; do
    if [[ -d "$d" ]]; then
      grep -Ril -- "$TOPIC" "$d" 2>/dev/null | head -n 30
    fi
  done

  # Mermaid shortcut: surface the canonical mermaid guide (if present).
  if [[ "$TOPIC" == "mermaid" ]] && [[ -f "$DOCS_FERA_DIR/guides/diagrams.md" ]]; then
    echo ""
    echo "✅ Mermaid guide (canonical): $DOCS_FERA_DIR/guides/diagrams.md"
  fi
fi
```

### 5. Audit current repository for the chosen topic

```bash
TOPIC_FILES=$(find "$REPO_ROOT" -type f \( -name "*.md" -o -name "*.mdc" \) -exec grep -li -- "$TOPIC" {} \; 2>/dev/null)
TOPIC_COUNT=$(echo "$TOPIC_FILES" | grep -v "^$" | wc -l | tr -d ' ')
echo "📊 Current repository: Found $TOPIC_COUNT file(s) mentioning topic '$TOPIC'"

# Mermaid-only deep checks (keeps mermaid behavior as the default topic)
if [[ "$TOPIC" == "mermaid" ]]; then
  MERMAID_FILES=$(find "$REPO_ROOT" -type f \( -name "*.md" -o -name "*.mdc" \) -exec grep -l "```mermaid" {} \; 2>/dev/null)
  MERMAID_COUNT=$(echo "$MERMAID_FILES" | grep -v "^$" | wc -l | tr -d ' ')
  echo "📊 Current repository: Found $MERMAID_COUNT file(s) with mermaid diagrams"

  ASCII_COUNT=0
  for file in $MERMAID_FILES; do
    if grep -q "ASCII Alternative\|ASCII alternative\|ascii alternative" "$file" 2>/dev/null; then
      ((ASCII_COUNT++)) || true
    fi
  done
  echo "📊 Mermaid files with ASCII alternatives: $ASCII_COUNT / $MERMAID_COUNT"
fi
```

### 6. Check for topic validation hooks / tooling (scripts-fera)

```bash
if [[ ! -d "$SCRIPTS_FERA_DIR" ]]; then
  echo "⚠️  scripts-fera not found at: $SCRIPTS_FERA_DIR"
else
  echo "✅ Found scripts-fera at: $SCRIPTS_FERA_DIR"

  if [[ "$TOPIC" == "mermaid" ]]; then
    if [[ -f "$SCRIPTS_FERA_DIR/templates/hooks/pre-commit-validate-mermaid.sh" ]]; then
      echo "✅ Mermaid validation hook template found in scripts-fera"
    elif [[ -f "$SCRIPTS_FERA_DIR/_dev/workflows/distribution/hooks_distribution/installers/install_validate_mermaid.sh" ]]; then
      echo "✅ Mermaid validation hook installer found in scripts-fera"
    else
      echo "⚠️  Mermaid validation hook not found in scripts-fera"
    fi

    if [[ -f "$REPO_ROOT/.git/hooks/pre-commit" ]] && grep -q "validate.*mermaid\|mermaid.*validate" "$REPO_ROOT/.git/hooks/pre-commit" 2>/dev/null; then
      echo "✅ Mermaid validation hook installed in current repo"
    else
      echo "⚠️  Mermaid validation hook not installed in current repo"
    fi
  else
    echo "🔍 Searching scripts-fera for tooling related to: $TOPIC"
    TOOLING_MATCHES=$(grep -Ril -- "$TOPIC" "$SCRIPTS_FERA_DIR" 2>/dev/null | head -n 50)
    if [[ -n "${TOOLING_MATCHES:-}" ]]; then
      echo "✅ Found possible tooling references (first 50):"
      echo "$TOOLING_MATCHES"
    else
      echo "⚠️  No obvious scripts-fera tooling found for topic '$TOPIC' (by keyword search)."
      echo "    If this topic should be enforced, implement it in scripts-fera and distribute via its installers."
    fi
  fi
fi
```

### 7. Verify docs-fera documentation organization for the topic

```bash
if [[ -d "$DOCS_FERA_DIR" ]]; then
  if [[ -f "$DOCS_FERA_DIR/guides/index_guides.yaml" ]]; then
    if grep -qi -- "$TOPIC" "$DOCS_FERA_DIR/guides/index_guides.yaml"; then
      echo "✅ Topic appears in docs-fera guides index"
    else
      echo "⚠️  Topic not found in docs-fera guides index (may still be documented elsewhere)"
    fi
  fi
fi
```

### 8. Verify scripts-fera has topic tooling and distribution workflow (when applicable)

```bash
if [[ -d "$SCRIPTS_FERA_DIR" ]]; then
  if [[ "$TOPIC" == "mermaid" ]]; then
    if [[ -f "$SCRIPTS_FERA_DIR/templates/hooks/pre-commit-validate-mermaid.sh" ]] || \
       [[ -f "$SCRIPTS_FERA_DIR/_dev/hooks/validate_mermaid.py" ]] || \
       [[ -f "$SCRIPTS_FERA_DIR/_dev/scripts/validate_mermaid.sh" ]]; then
      echo "✅ Mermaid validator found in scripts-fera"
    else
      echo "⚠️  Mermaid validator not found in scripts-fera"
    fi

    if [[ -d "$SCRIPTS_FERA_DIR/_dev/workflows/distribution/hooks_distribution/installers" ]]; then
      if ls "$SCRIPTS_FERA_DIR/_dev/workflows/distribution/hooks_distribution/installers/"*mermaid* 2>/dev/null; then
        echo "✅ Mermaid hook installer found in scripts-fera"
      else
        echo "⚠️  Mermaid hook installer not found in scripts-fera"
      fi
    fi
  else
    echo "ℹ️  Generic topics: verify (1) scripts-fera has a validator/hook and (2) an installer exists to distribute it."
    echo "    Use docs-fera@ guides/distribution/distribution_workflow_unified.md as the authority for workflow boundaries."
  fi
fi
```

### 9. Run distribution workflow (topic tooling) — mermaid path kept; generic path is discovery-only

```bash
if [[ "$TOPIC" == "mermaid" ]]; then
  if [[ -f "$SCRIPTS_FERA_DIR/_dev/workflows/distribution/hooks_distribution/installers/install_validate_mermaid.sh" ]]; then
    echo "📦 Running mermaid hook installer from scripts-fera..."
    bash "$SCRIPTS_FERA_DIR/_dev/workflows/distribution/hooks_distribution/installers/install_validate_mermaid.sh" "$REPO_ROOT"
  elif [[ -f "$SCRIPTS_FERA_DIR/_dev/workflows/distribution/entity_management_cli.sh" ]]; then
    echo "📦 Using entity management CLI to install mermaid hook..."
    bash "$SCRIPTS_FERA_DIR/_dev/workflows/distribution/entity_management_cli.sh" install hooks validate_mermaid --target "$REPO_ROOT"
  else
    echo "⚠️  No distribution workflow found for mermaid hooks"
  fi
else
  echo "ℹ️  For non-mermaid topics: identify the correct scripts-fera installer for that topic and run it."
  echo "    Never copy files directly; route changes through templates + installers."
fi
```

### 10. Create an improvement plan (topic-general)

```bash
IMPROVEMENTS_FILE="$REPO_ROOT/.tmp/topic_improvements_$(date +%Y%m%d_%H%M%S).md"

cat > "$IMPROVEMENTS_FILE" << 'EOF'
# Topic Improvements

## Issues Found
- [ ] Missing topic documentation references (guides/standards/patterns/decisions)
- [ ] Missing enforcement tooling (hook/validator) or installer workflow
- [ ] Drift from canonized conventions

## Actions Required
1. Identify the canonized references in docs-fera (guides/standards/patterns/decisions)
2. Update this repo to match those conventions (without breaking existing behavior)
3. If enforcement is required: ensure scripts-fera has the validator/hook + installer
4. Install tooling via distribution workflows (never copy)
EOF

echo "📝 Improvement plan created: $IMPROVEMENTS_FILE"
```

## Success Criteria

- [ ] docs-fera canon consulted for the chosen topic (guides/standards/patterns/decisions)
- [ ] Current repository audited against that canon
- [ ] If applicable: enforcement tooling exists in scripts-fera and is installed via distribution workflow
- [ ] Drift is documented with an actionable improvement plan
- [ ] Mermaid topic (default): diagrams follow best practices (dual approach, ASCII alternatives)
- [ ] All improvements documented and actionable

## Related Commands

- `/dcon_docs_structure_audit` - General documentation structure audit
- `/crcv_cross_repo_convergence` - Cross-repo standardization workflow
- `/docu_document` - Create new documentation
- `/lint_lint` - Run linting and validation

**Local Reference**: `commands/cana_canonical_topic_alignment.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/cana_canonical_topic_alignment.md`
