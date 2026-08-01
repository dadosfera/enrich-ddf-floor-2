#!/usr/bin/env bash
set -euo pipefail

# Thin wrapper (canonical, scripts-fera SSoT) to run the log size warning hook.

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SH_HOOK="$HOOK_DIR/source/quality/pre-commit-warn-log-size.sh"

if [[ ! -f "$SH_HOOK" ]]; then
  echo "❌ scripts-fera: missing canonical log size warning hook at $SH_HOOK" >&2
  exit 1
fi

bash "$SH_HOOK" "$@"
