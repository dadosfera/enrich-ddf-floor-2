#!/bin/bash
# scripts/add-makefile-timeouts.sh
# Add timeout wrappers to Makefile targets

set -euo pipefail

MAKEFILE=${1:-Makefile}

if [ ! -f "$MAKEFILE" ]; then
    echo "Makefile not found: $MAKEFILE"
    exit 0
fi

# Detect timeout command
TIMEOUT_CMD="timeout"
if command -v gtimeout &> /dev/null; then
    TIMEOUT_CMD="gtimeout"
elif ! command -v timeout &> /dev/null; then
    echo "⚠️  Neither timeout nor gtimeout found. Install coreutils."
    exit 1
fi

# Create backup
cp "$MAKEFILE" "$MAKEFILE.bak.$(date +%Y%m%d_%H%M%S)"

# Patterns to add timeouts to (long-running operations)
PATTERNS=(
    "npm test"
    "npm run test"
    "pytest"
    "python.*test"
    "jest"
    "npm run build"
    "npm run dev"
    "vite"
    "docker compose"
    "docker-compose"
    "npm install"
    "pip install"
    "npm ci"
)

# Timeout values by operation type
declare -A TIMEOUTS
TIMEOUTS["test"]=300
TIMEOUTS["build"]=120
TIMEOUTS["dev"]=0  # No timeout for dev servers
TIMEOUTS["install"]=600
TIMEOUTS["docker"]=60
TIMEOUTS["default"]=120

get_timeout() {
    local cmd="$1"
    if [[ "$cmd" =~ test ]]; then
        echo "${TIMEOUTS[test]}"
    elif [[ "$cmd" =~ build ]]; then
        echo "${TIMEOUTS[build]}"
    elif [[ "$cmd" =~ install|ci ]]; then
        echo "${TIMEOUTS[install]}"
    elif [[ "$cmd" =~ docker ]]; then
        echo "${TIMEOUTS[docker]}"
    elif [[ "$cmd" =~ dev ]]; then
        echo "0"  # No timeout for dev
    else
        echo "${TIMEOUTS[default]}"
    fi
}

# Process Makefile
TEMP_FILE=$(mktemp)
IN_TARGET=false
CURRENT_TARGET=""

while IFS= read -r line; do
    # Detect target line
    if [[ "$line" =~ ^[a-zA-Z0-9_-]+:.*## ]]; then
        IN_TARGET=true
        CURRENT_TARGET=$(echo "$line" | cut -d: -f1)
        echo "$line" >> "$TEMP_FILE"
    elif [[ "$line" =~ ^[a-zA-Z0-9_-]+: ]]; then
        IN_TARGET=true
        CURRENT_TARGET=$(echo "$line" | cut -d: -f1)
        echo "$line" >> "$TEMP_FILE"
    elif [[ "$line" =~ ^[[:space:]]*@ ]] || [[ "$line" =~ ^[[:space:]]*\t ]]; then
        # Command line - check if it needs timeout
        CMD=$(echo "$line" | sed 's/^[[:space:]]*@//' | sed 's/^[[:space:]]*\t//')

        NEEDS_TIMEOUT=false
        for pattern in "${PATTERNS[@]}"; do
            if echo "$CMD" | grep -qi "$pattern"; then
                NEEDS_TIMEOUT=true
                break
            fi
        done

        if [ "$NEEDS_TIMEOUT" = true ] && ! echo "$CMD" | grep -q "$TIMEOUT_CMD"; then
            TIMEOUT_VAL=$(get_timeout "$CMD")
            if [ "$TIMEOUT_VAL" != "0" ]; then
                # Add timeout wrapper
                INDENT=$(echo "$line" | sed 's/\(.*\)\S.*/\1/')
                NEW_CMD="$INDENT$TIMEOUT_CMD $TIMEOUT_VAL $CMD"
                echo "$NEW_CMD" >> "$TEMP_FILE"
                continue
            fi
        fi

        echo "$line" >> "$TEMP_FILE"
    else
        # Other line (empty, comment, etc.)
        echo "$line" >> "$TEMP_FILE"
        if [ -z "$(echo "$line" | tr -d '[:space:]')" ]; then
            IN_TARGET=false
        fi
    fi
done < "$MAKEFILE"

mv "$TEMP_FILE" "$MAKEFILE"
echo "✅ Makefile timeouts added (backup: $MAKEFILE.bak.*)"
