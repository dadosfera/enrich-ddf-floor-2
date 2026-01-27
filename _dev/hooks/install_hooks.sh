#!/bin/bash
# **Local Reference**: `_dev/hooks/install_hooks.sh`
# **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/_dev/hooks/install_hooks.sh`

# ============================================================================
# Git Hooks Installer (scripts-fera + _dev/hooks/ → .git/hooks/)
# ============================================================================
#
# PURPOSE:
#   Installs git hooks (pre-commit, pre-push) by generating wrappers that
#   execute canonical hooks from scripts-fera and local hooks from _dev/hooks/.
#   This is the CANONICAL entrypoint for hook installation.
#
# SOURCE OF TRUTH:
#   - Canonical Hooks: scripts-fera/hooks/ (Single Source of Truth for shared hooks)
#   - Local Hooks: _dev/hooks/ (repository-specific hooks)
#   - Config: .pre-commit-config.yaml, config/pre-commit-config.eol.yaml
#
# TARGETS:
#   - .git/hooks/pre-commit (generated master wrapper)
#   - .git/hooks/pre-push (auto-refresh trigger)
#   - .git/hooks/.install_hooks_signature (signature cache)
#
# DEPENDENCY:
#   - scripts-fera repository (sibling or submodule)
#   - If missing: Continues in degraded mode (canonical hooks skipped, warning logged)
#
# INTELLIGENCE:
#   - Signature-based: Computes SHA256 digest of all hook sources
#   - Auto mode: Skips regeneration if signature unchanged (fast, idempotent)
#   - Push-time refresh: Pre-push hook runs install_hooks.sh --auto
#
# USAGE:
#   bash _dev/hooks/install_hooks.sh [--auto]
#   --auto: Skip reinstall when signature matches cached digest
#
# SAFETY NOTES:
#   - Never edit .git/hooks/pre-commit or .git/hooks/pre-push directly
#   - Always edit sources in _dev/hooks/ and run installer
#   - Signature writes are atomic (no corruption on failure)
#
# DOCUMENTATION:
#   See: docs-fera@ guides/distribution/distribution_workflow_unified.md (Hooks section)
#   See: standards/hooks/hook_distribution_standard.md
#   See: _dev/hooks/README.md
#
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
REPO_NAME="$(basename "$REPO_ROOT")"
HOOK_SIGNATURE_VERSION=1

log() {
    local level="$1"
    shift
    printf '[hooks][%s] %s\n' "$level" "$*"
}

usage() {
    cat <<'EOF'
Usage: bash _dev/hooks/install_hooks.sh [--auto]

Options:
  --auto    Skip reinstall when signature matches the cached digest.
  -h|--help Show this help message.
EOF
}

AUTO_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --auto)
            AUTO_MODE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            log "ERROR" "Unknown argument: $1"
            usage
            exit 1
            ;;
    esac
done

if ! GIT_DIR=$(git -C "$REPO_ROOT" rev-parse --git-dir 2>/dev/null); then
    log "ERROR" "Not inside a git repository."
    exit 1
fi

if [[ "$GIT_DIR" != /* ]]; then
    GIT_DIR="$REPO_ROOT/$GIT_DIR"
fi

if [[ ! -d "$GIT_DIR" ]]; then
    log "ERROR" "Git directory not found at: $GIT_DIR"
    exit 1
fi

HOOKS_DIR="$GIT_DIR/hooks"
SIGNATURE_FILE="$HOOKS_DIR/.install_hooks_signature"

mkdir -p "$HOOKS_DIR"

resolve_scripts_fera() {
    local repo_parent
    repo_parent="$(cd "$REPO_ROOT/.." && pwd -P)"
    local candidates=(
        "$REPO_ROOT/scripts-fera/hooks"
        "$repo_parent/scripts-fera/hooks"
    )

    for path in "${candidates[@]}"; do
        if [[ -d "$path" ]]; then
            printf '%s\n' "$path"
            return 0
        fi
    done

    printf ''
}

SCRIPTS_FERA_HOOKS_DIR="$(resolve_scripts_fera)"

if [[ -z "$SCRIPTS_FERA_HOOKS_DIR" ]]; then
    log "WARN" "scripts-fera/hooks not detected; continuing in degraded mode."
fi

read_previous_signature() {
    if [[ -f "$SIGNATURE_FILE" ]]; then
        awk -F'=' '/^digest=/{print $2}' "$SIGNATURE_FILE" | tail -n1
    fi
}

generate_signature() {
    HOOK_REPO_ROOT="$REPO_ROOT" \
    HOOK_SCRIPTS_FERA="$SCRIPTS_FERA_HOOKS_DIR" \
    python3 <<'PY'
import hashlib
import os
from pathlib import Path

repo_root = Path(os.environ["HOOK_REPO_ROOT"]).resolve()
scripts_fera = Path(os.environ.get("HOOK_SCRIPTS_FERA", "")).resolve() if os.environ.get("HOOK_SCRIPTS_FERA") else None

include_dirs = [
    repo_root / "_dev" / "hooks",
    repo_root / "_dev" / "hooks" / "core",
    repo_root / "_dev" / "hooks" / "python",
]
if scripts_fera and scripts_fera.exists():
    include_dirs.append(scripts_fera)

include_files = [
    repo_root / ".pre-commit-config.yaml",
    repo_root / "config" / "pre-commit-config.eol.yaml",
]

patterns = {".sh", ".py", ".yaml"}

def iter_candidate_files():
    seen = set()
    for directory in include_dirs:
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in patterns:
                continue
            if ".git" in path.parts or ".tmp" in path.parts:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield resolved
    for file_path in include_files:
        resolved = file_path.resolve()
        if resolved.is_file() and resolved not in seen:
            seen.add(resolved)
            yield resolved

hasher = hashlib.sha256()
count = 0

if not (scripts_fera and scripts_fera.exists()):
    hasher.update(b"scripts-fera-missing")

for candidate in iter_candidate_files():
    try:
        relative = candidate.relative_to(repo_root)
        hasher.update(str(relative).encode())
    except ValueError:
        hasher.update(str(candidate).encode())
    hasher.update(b"\0")
    with candidate.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    count += 1

if count == 0:
    hasher.update(b"no-inputs")

print(hasher.hexdigest())
PY
}

persist_signature() {
    local digest="$1"
    local tmp_file="${SIGNATURE_FILE}.tmp.$$"
    {
        printf 'signature_version=%s\n' "$HOOK_SIGNATURE_VERSION"
        printf 'repo_name=%s\n' "$REPO_NAME"
        printf 'digest=%s\n' "$digest"
        printf 'generated_at=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    } > "$tmp_file"
    mv "$tmp_file" "$SIGNATURE_FILE"
}

install_pre_commit_hook() {
    cat > "$HOOKS_DIR/pre-commit" <<'EOF'
#!/bin/bash
# Master Pre-commit Hook
# Delegates to canonical and local hooks

set -e

# 0. Ensure Git Guard is installed (self-healing)
#    If the guard is missing, install it and block the commit so the user can
#    restart/source their shell and actually activate the runtime protection.
SCRIPTS_FERA_DIR_FOR_GUARD=""
if [[ -d "scripts-fera" ]]; then
  SCRIPTS_FERA_DIR_FOR_GUARD="scripts-fera"
elif [[ -d "../scripts-fera" ]]; then
  SCRIPTS_FERA_DIR_FOR_GUARD="../scripts-fera"
fi

if [[ -n "$SCRIPTS_FERA_DIR_FOR_GUARD" && -f "$SCRIPTS_FERA_DIR_FOR_GUARD/hooks/pre-commit-ensure-git-guard-installed.sh" ]]; then
  bash "$SCRIPTS_FERA_DIR_FOR_GUARD/hooks/pre-commit-ensure-git-guard-installed.sh"
elif [[ -f "_dev/hooks/core/ensure_git_guard_installed.sh" ]]; then
  bash _dev/hooks/core/ensure_git_guard_installed.sh
fi

# 1. Submodule Check (Critical Safety)
if [[ ! -f ".gitmodules" ]]; then
  # Exclude the installer itself from the scan to avoid false positives (the hook
  # necessarily contains submodule-related text).
  SUBMODULE_SCAN_FILES="$(git diff --cached --name-only | grep -v '^_dev/hooks/install_hooks\.sh$' || true)"
  if [[ -n "$SUBMODULE_SCAN_FILES" ]] && echo "$SUBMODULE_SCAN_FILES" | xargs -I{} sh -c 'grep -HnE "gi""t submodule|submodule update|submodule foreach" "{}" 2>/dev/null' | grep -q .; then
    echo "❌ Submodule commands detected in staged changes but .gitmodules is absent."
    echo "   Remove submodule-related commands or add a proper .gitmodules before committing."
    exit 1
  fi
fi

# 2. Canonical Hooks (scripts-fera)
echo "🔍 Running canonical hooks..."

# Attempt to locate scripts-fera
SCRIPTS_FERA_DIR=""
if [[ -d "scripts-fera" ]]; then
    SCRIPTS_FERA_DIR="scripts-fera"
elif [[ -d "../scripts-fera" ]]; then
    SCRIPTS_FERA_DIR="../scripts-fera"
fi

if [[ -n "$SCRIPTS_FERA_DIR" ]]; then
    if [[ -f "$SCRIPTS_FERA_DIR/hooks/pre-commit-check-no-git-automation.sh" ]]; then
        bash "$SCRIPTS_FERA_DIR/hooks/pre-commit-check-no-git-automation.sh"
    fi

    if [[ -f "$SCRIPTS_FERA_DIR/hooks/pre-commit-check-deprecated-commands.sh" ]]; then
        bash "$SCRIPTS_FERA_DIR/hooks/pre-commit-check-deprecated-commands.sh"
    fi

    # Prefer installed hook instances (via scripts-fera official installers) over
    # executing scripts directly out of scripts-fera.
    # For -fera repos, check _dev/scripts/hooks/ first; for other repos, check scripts/hooks/
    DID_WARN_LOG_SIZE_CANONICAL="no"
    REPO_NAME="$(basename "$(pwd)")"
    if [[ "$REPO_NAME" == *"-fera" ]]; then
        # -fera repo: check _dev/scripts/hooks/ first
        if [[ -x "_dev/scripts/hooks/pre-commit-warn-log-size.sh" ]]; then
            bash _dev/scripts/hooks/pre-commit-warn-log-size.sh
            DID_WARN_LOG_SIZE_CANONICAL="yes"
        elif [[ -x "scripts/hooks/pre-commit-warn-log-size.sh" ]]; then
            bash scripts/hooks/pre-commit-warn-log-size.sh
            DID_WARN_LOG_SIZE_CANONICAL="yes"
        fi
    else
        # Non-fera repo: check scripts/hooks/ (installed by scripts-fera installers)
        if [[ -x "scripts/hooks/pre-commit-warn-log-size.sh" ]]; then
            bash scripts/hooks/pre-commit-warn-log-size.sh
            DID_WARN_LOG_SIZE_CANONICAL="yes"
        else
            # Best-effort self-heal: install the hook into this repo (non-blocking).
            TARGET_REPO_ABS="$(pwd -P)"
            INSTALL_WARN_LOG_SIZE="$SCRIPTS_FERA_DIR/_dev/workflows/distribution/hooks_distribution/installers/install_warn_log_size.sh"
            if [[ -f "$INSTALL_WARN_LOG_SIZE" ]]; then
                bash "$INSTALL_WARN_LOG_SIZE" "$TARGET_REPO_ABS" >/dev/null 2>&1 || true
            fi

            if [[ -x "scripts/hooks/pre-commit-warn-log-size.sh" ]]; then
                bash scripts/hooks/pre-commit-warn-log-size.sh
                DID_WARN_LOG_SIZE_CANONICAL="yes"
            fi
        fi
    fi
    if [[ "$DID_WARN_LOG_SIZE_CANONICAL" == "no" ]] && [[ -f "$SCRIPTS_FERA_DIR/hooks/pre-commit-warn-log-size.sh" ]]; then
        # Legacy fallback (should disappear once all repos rely on installers).
        bash "$SCRIPTS_FERA_DIR/hooks/pre-commit-warn-log-size.sh"
        DID_WARN_LOG_SIZE_CANONICAL="yes"
    fi

    # Filename validation (shared) - if present
    DID_VALIDATE_FILENAME_CANONICAL="no"
    if [[ -f "$SCRIPTS_FERA_DIR/hooks/pre-commit-validate-filename.sh" ]]; then
        bash "$SCRIPTS_FERA_DIR/hooks/pre-commit-validate-filename.sh"
        DID_VALIDATE_FILENAME_CANONICAL="yes"
    fi
else
    echo "⚠️  scripts-fera not found. Canonical hooks skipped."
    echo "   Expected at ../scripts-fera or ./scripts-fera"
    DID_VALIDATE_FILENAME_CANONICAL="no"
fi

# 3. Local Hooks (docs-fera specific)
echo "🔍 Running local hooks..."

if [[ -f "_dev/hooks/pre-commit-rule-validation.sh" ]]; then
    bash _dev/hooks/pre-commit-rule-validation.sh
fi

if [[ -f "_dev/hooks/pre-commit-validate-command-workflow.sh" ]]; then
    bash _dev/hooks/pre-commit-validate-command-workflow.sh
fi

if [[ -f "_dev/hooks/pre-commit-validate-commands.py" ]]; then
    python3 _dev/hooks/pre-commit-validate-commands.py
fi

if [[ -f "_dev/hooks/pre-commit-validate-command-references.py" ]]; then
    python3 _dev/hooks/pre-commit-validate-command-references.py
fi

if [[ -f "_dev/hooks/pre-commit-command-tests.sh" ]]; then
    bash _dev/hooks/pre-commit-command-tests.sh
fi

# Avoid running warn-log-size twice: use local hook only as fallback when canonical did not run.
if [[ "${DID_WARN_LOG_SIZE_CANONICAL:-no}" != "yes" && -f "_dev/hooks/pre-commit-warn-log-size.sh" ]]; then
    bash _dev/hooks/pre-commit-warn-log-size.sh
fi

# 4. Taxonomy Validation
if [[ -f "_dev/hooks/core/validate_taxonomy.py" ]]; then
    echo "🔍 Validating taxonomy..."
    python3 _dev/hooks/core/validate_taxonomy.py
fi

# 5. Index Validation
if [[ -f "_dev/hooks/core/validate_indexes.py" ]]; then
    echo "🔍 Validating indexes..."
    python3 _dev/hooks/core/validate_indexes.py
fi

# 6. Folder Structure Validation
if [[ -f "_dev/hooks/core/validate_folder_structure.py" ]]; then
    echo "🔍 Validating folder structure..."
    python3 _dev/hooks/core/validate_folder_structure.py
fi

# 7. Filename Validation (added/renamed files) - fallback when scripts-fera hook not available
if [[ "${DID_VALIDATE_FILENAME_CANONICAL:-no}" != "yes" ]]; then
    if [[ -f "_dev/hooks/core/validate_filename.py" ]]; then
        echo "🔍 Validating filenames..."
        python3 _dev/hooks/core/validate_filename.py
    fi
fi

echo "✅ All pre-commit checks passed"
EOF
    chmod +x "$HOOKS_DIR/pre-commit"
    log "INFO" "Pre-commit hook refreshed at $HOOKS_DIR/pre-commit"
}

install_pre_push_hook() {
    cat > "$HOOKS_DIR/pre-push" <<'EOF'
#!/bin/bash
# Pre-push trigger that keeps hooks current via install_hooks.sh --auto.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"
INSTALLER="_dev/hooks/install_hooks.sh"

if [[ -z "$REPO_ROOT" ]]; then
    echo "⚠️ pre-push hook: unable to locate repository root; skipping auto-refresh."
    exit 0
fi

INSTALLER_PATH="$REPO_ROOT/$INSTALLER"

if [[ ! -f "$INSTALLER_PATH" ]]; then
    echo "⚠️ pre-push hook: installer missing at $INSTALLER_PATH; continuing push."
    exit 0
fi

if command -v gtimeout >/dev/null 2>&1; then
    if gtimeout 5 bash "$INSTALLER_PATH" --auto; then
        echo "✅ pre-push hook intelligence: hooks already current."
    else
        echo "⚠️ pre-push hook: automatic refresh failed (non-blocking)."
    fi
    sleep 1
else
    echo "⚠️ pre-push hook: gtimeout not available; skipping automatic refresh."
fi

exit 0
EOF
    chmod +x "$HOOKS_DIR/pre-push"
    log "INFO" "Pre-push hook refreshed at $HOOKS_DIR/pre-push"
}

previous_signature="$(read_previous_signature || true)"
current_signature="$(generate_signature)"

if [[ "$AUTO_MODE" == "true" && -n "$previous_signature" && "$previous_signature" == "$current_signature" ]]; then
    log "INFO" "Signature unchanged – skipping hook reinstall."
    exit 0
fi

log "INFO" "Signature difference detected (or manual run) – installing hooks."
install_pre_commit_hook
install_pre_push_hook
persist_signature "$current_signature"
log "INFO" "Hook intelligence ready (signature: $current_signature)"
