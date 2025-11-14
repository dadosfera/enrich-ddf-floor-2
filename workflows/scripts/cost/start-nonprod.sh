#!/bin/bash
# scripts/cost/start-nonprod.sh
# Start non-production instances in the morning

set -euo pipefail

ENVIRONMENTS=("dev" "staging" "alpha")

# Log directory
LOG_DIR="${LOG_DIR:-logs}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/cost-control.log"

log_action() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

log_action "=== Cloud Cost Control: Start Non-Production Instances ==="

# Check if OCI CLI is available
if ! command -v oci &> /dev/null; then
    log_action "⚠️  OCI CLI not found. Skipping cloud operations."
    exit 0
fi

# Check if OCI is configured
if [ -z "${OCI_ACTIVE_TENANCY:-}" ] && [ -z "${OCI_CONFIG_FILE:-}" ]; then
    log_action "⚠️  OCI not configured. Set OCI_ACTIVE_TENANCY or OCI_CONFIG_FILE."
    exit 0
fi

FAILED=0

for env in "${ENVIRONMENTS[@]}"; do
    log_action "Processing environment: $env"

    # Get instance IDs for this environment
    INSTANCE_IDS=$(oci compute instance list \
        --compartment-id "${OCI_COMPARTMENT_ID:-}" \
        --lifecycle-state STOPPED \
        --query "data[?contains(\"display-name\", \"$env\")].id" \
        --raw-output 2>/dev/null || echo "")

    if [ -z "$INSTANCE_IDS" ] || [ "$INSTANCE_IDS" = "[]" ]; then
        log_action "  No stopped instances found for $env"
        continue
    fi

    for instance_id in $(echo "$INSTANCE_IDS" | tr -d '[],"'); do
        if [ -z "$instance_id" ] || [ "$instance_id" = "null" ]; then
            continue
        fi

        instance_name=$(oci compute instance get --instance-id "$instance_id" \
            --query "data.\"display-name\"" --raw-output 2>/dev/null || echo "unknown")

        log_action "  Starting instance: $instance_name ($instance_id)"
        if oci compute instance action --instance-id "$instance_id" --action START --wait-for-state RUNNING 2>&1 | tee -a "$LOG_FILE"; then
            log_action "  ✅ Successfully started: $instance_name"
        else
            log_action "  ❌ Failed to start: $instance_name"
            ((FAILED++))
        fi
    done
done

if [ $FAILED -gt 0 ]; then
    log_action "⚠️  $FAILED instances failed to start"
    exit 1
else
    log_action "✅ Start operation completed successfully"
    exit 0
fi
