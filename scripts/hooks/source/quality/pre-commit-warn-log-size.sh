#!/bin/bash
trap 'exit 0' SIGINT SIGTERM
# Pre-commit Hook: Warn about Large Log Files
# Location: scripts-fera/hooks/source/quality/pre-commit-warn-log-size.sh
# Purpose: Warns when log files exceed size threshold (non-blocking)
# Distribution: Canonical hook for all repositories

# ==============================================================================
# ALLOWLISTS / EXCEPTIONS — WITH JUSTIFICATIONS
# ==============================================================================
# This hook is intentionally **warning-only** (never blocks commits) but it still
# supports a small set of controlled "exceptions" (mostly via configuration).
#
# **Current Allowlist / Exception Surface**
#
# 1) **LOG_DIRS** (default: `_dev/logs`, `logs`, `.logs`)
#    - **Reason**: These are the canonical log locations across repos.
#    - **Scope**: Only these directories are scanned by default.
#    - **Removal plan**: N/A (this is the core behavior).
#
# 2) **LOG_DIRS_OVERRIDE** (colon-separated override)
#    - **Reason**: Some repos place logs in non-standard locations.
#    - **Scope**: Affects only *which directories* are scanned; size thresholds
#      still apply to any discovered log files.
#    - **Removal plan**: Prefer converging repos back to canonical log dirs; keep
#      override support for portability until convergence is complete.
#
# 3) **DIRS_TO_CHECK / `.tmp`** (default: warn if `.tmp` exceeds 250MB)
#    - **Reason**: `.tmp` often accumulates build/test artifacts and can grow
#      unexpectedly, causing developer friction or CI slowness.
#    - **Scope**: Directory-size check applies only to directories listed in
#      `DIRS_TO_CHECK` (default: `.tmp`).
#    - **Removal plan**: N/A (this is a core early-warning signal).
#
# 4) **DIRS_TO_CHECK_OVERRIDE** (colon-separated override)
#    - **Reason**: Some repos use different temp directories (or multiple).
#    - **Scope**: Affects only which directories are checked for aggregate size.
#    - **Removal plan**: Prefer convergence; keep override support for now.
#
# 5) **TMP_WARNING_SIZE_MB=0** (disable temp dir warnings)
#    - **Reason**: Some repos legitimately keep large cached artifacts in `.tmp`
#      (e.g., large local test corpora) and warnings would be pure noise.
#    - **Scope**: Disables only the *directory-size* warning; log-file warnings
#      remain active.
#    - **Removal plan**: If consistently disabled, fix root cause (move caches to
#      a dedicated cache dir, add pruning/rotation, or adjust repo workflows).
#
# **Policy**
# - Exceptions must stay **bounded** and **explainable**.
# - Prefer fixing the underlying issue (rotation/pruning) over "turning it off".
# ==============================================================================

set -euo pipefail

# Color codes for output (use ANSI escape bytes, not literal "\033")
# If stdout isn't a TTY (e.g., captured logs), disable colors to avoid raw escape sequences.
if [[ -t 1 ]]; then
    RED=$'\033[0;31m'
    YELLOW=$'\033[1;33m'
    GREEN=$'\033[0;32m'
    BLUE=$'\033[0;34m'
    NC=$'\033[0m' # No Color
else
    RED=""
    YELLOW=""
    GREEN=""
    BLUE=""
    NC=""
fi

# Configuration
WARNING_SIZE_MB=${LOG_WARNING_SIZE_MB:-5}  # Default: 5MB
WARNING_SIZE_BYTES=$((WARNING_SIZE_MB * 1024 * 1024))
LOG_DIRS=("_dev/logs" "logs" ".logs")

# Optional override for testing / custom repos (colon-separated)
# Example: LOG_DIRS_OVERRIDE=".tmp/logs_test:logs"
if [[ -n "${LOG_DIRS_OVERRIDE:-}" ]]; then
    IFS=':' read -r -a LOG_DIRS <<< "${LOG_DIRS_OVERRIDE}"
fi

# Directory size warnings (non-blocking)
# Default: warn if repo-local .tmp grows beyond ~250MB (adjust via TMP_WARNING_SIZE_MB)
TMP_WARNING_SIZE_MB=${TMP_WARNING_SIZE_MB:-250}
TMP_WARNING_SIZE_BYTES=$((TMP_WARNING_SIZE_MB * 1024 * 1024))
DIRS_TO_CHECK=(".tmp")

# Optional override for testing / custom repos (colon-separated)
# Example: DIRS_TO_CHECK_OVERRIDE=".tmp/test_artifacts"
if [[ -n "${DIRS_TO_CHECK_OVERRIDE:-}" ]]; then
    IFS=':' read -r -a DIRS_TO_CHECK <<< "${DIRS_TO_CHECK_OVERRIDE}"
fi

# Function to get file size in bytes (cross-platform)
get_file_size() {
    local file="$1"
    if [[ -f "$file" ]]; then
        # Try Linux stat first, then macOS stat
        stat -c%s "$file" 2>/dev/null || \
        stat -f%z "$file" 2>/dev/null || \
        echo "0"
    else
        echo "0"
    fi
}

# Function to get directory size in bytes (cross-platform best-effort)
get_dir_size_bytes() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "0"
        return 0
    fi

    # `du -sk` is portable across Linux/macOS; outputs KiB.
    local kb
    kb="$(du -sk "$dir" 2>/dev/null | awk '{print $1}' || true)"
    if [[ -z "${kb:-}" ]]; then
        echo "0"
        return 0
    fi
    echo $((kb * 1024))
}

# Function to format bytes to human-readable
format_size() {
    local bytes=$1
    if [[ $bytes -ge 1048576 ]]; then
        echo "$((bytes / 1048576))MB"
    elif [[ $bytes -ge 1024 ]]; then
        echo "$((bytes / 1024))KB"
    else
        echo "${bytes}B"
    fi
}

echo "📊 Checking log file sizes..."

# Track if any warnings were found
WARNINGS_FOUND=0

# Check each log directory
for log_dir in "${LOG_DIRS[@]}"; do
    if [[ ! -d "$log_dir" ]]; then
        continue
    fi

    # Find all log files (common extensions)
    while IFS= read -r -d '' log_file; do
        file_size=$(get_file_size "$log_file")

        if [[ $file_size -gt $WARNING_SIZE_BYTES ]]; then
            if [[ $WARNINGS_FOUND -eq 0 ]]; then
                echo ""
                echo "${YELLOW}⚠️  Large log files detected:${NC}"
            fi

            size_formatted=$(format_size "$file_size")
            echo "  ${YELLOW}⚠️${NC}  ${log_file}: ${size_formatted} (threshold: ${WARNING_SIZE_MB}MB)"
            WARNINGS_FOUND=1
        fi
    done < <(find "$log_dir" -type f \( -name "*.log" -o -name "*.log.*" \) -print0 2>/dev/null || true)
done

# Check selected directories sizes (e.g., .tmp/)
if [[ "${TMP_WARNING_SIZE_MB}" -gt 0 ]]; then
    for dir in "${DIRS_TO_CHECK[@]}"; do
        if [[ ! -d "$dir" ]]; then
            continue
        fi

        dir_size=$(get_dir_size_bytes "$dir")
        if [[ $dir_size -gt $TMP_WARNING_SIZE_BYTES ]]; then
            if [[ $WARNINGS_FOUND -eq 0 ]]; then
                echo ""
                echo "${YELLOW}⚠️  Large directories detected:${NC}"
            fi

            size_formatted=$(format_size "$dir_size")
            echo "  ${YELLOW}⚠️${NC}  ${dir}: ${size_formatted} (threshold: ${TMP_WARNING_SIZE_MB}MB)"
            echo "     ${YELLOW}Consider:${NC} Cleaning or pruning generated artifacts under ${dir}/"
            WARNINGS_FOUND=1
        fi
    done
fi

# Also check staged log files specifically
STAGED_LOG_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null | grep -E '\.(log|log\..*)$' || true)

if [[ -n "$STAGED_LOG_FILES" ]]; then
    echo ""
    echo "${BLUE}ℹ️  Checking staged log files...${NC}"

    while IFS= read -r log_file; do
        if [[ -f "$log_file" ]]; then
            file_size=$(get_file_size "$log_file")

            if [[ $file_size -gt $WARNING_SIZE_BYTES ]]; then
                if [[ $WARNINGS_FOUND -eq 0 ]]; then
                    echo ""
                    echo "${YELLOW}⚠️  Large log files detected:${NC}"
                fi

                size_formatted=$(format_size "$file_size")
                echo "  ${YELLOW}⚠️${NC}  ${log_file} (staged): ${size_formatted} (threshold: ${WARNING_SIZE_MB}MB)"
                echo "     ${YELLOW}Consider:${NC} Rotate or exclude large log files from commits"
                WARNINGS_FOUND=1
            fi
        fi
    done <<< "$STAGED_LOG_FILES"
fi

if [[ $WARNINGS_FOUND -eq 0 ]]; then
    echo "${GREEN}✅ All log files are within size limits${NC}"
else
    echo ""
    echo "${YELLOW}💡 Tip:${NC} Consider adding large log files to .gitignore or rotating them"
    echo "   Set LOG_WARNING_SIZE_MB to adjust the threshold (current: ${WARNING_SIZE_MB}MB)"
    echo ""
    # Non-blocking: exit 0 to allow commit
fi

exit 0
