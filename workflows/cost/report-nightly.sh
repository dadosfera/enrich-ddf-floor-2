#!/bin/bash
# scripts/cost/report-nightly.sh
# Generate nightly cost report

set -euo pipefail

REPORT_DIR="${REPORT_DIR:-logs}"
mkdir -p "$REPORT_DIR"
REPORT_FILE="$REPORT_DIR/cost-report-$(date +%Y-%m-%d).txt"

log_action() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1"
}

log_action "=== Generating Cloud Cost Report ==="

{
    echo "Cloud Cost Report - $(date)"
    echo "================================"
    echo ""

    # Check if OCI CLI is available
    if ! command -v oci &> /dev/null; then
        echo "⚠️  OCI CLI not found. Generating report without instance data."
        echo ""
        echo "Estimated Daily Cost: N/A (OCI CLI not available)"
        echo "Estimated Monthly Cost: N/A (OCI CLI not available)"
        exit 0
    fi

    # Check if OCI is configured
    if [ -z "${OCI_ACTIVE_TENANCY:-}" ] && [ -z "${OCI_CONFIG_FILE:-}" ]; then
        echo "⚠️  OCI not configured. Set OCI_ACTIVE_TENANCY or OCI_CONFIG_FILE."
        echo ""
        echo "Estimated Daily Cost: N/A (OCI not configured)"
        echo "Estimated Monthly Cost: N/A (OCI not configured)"
        exit 0
    fi

    echo "Instance Status:"
    echo "----------------"
    oci compute instance list --all --output table 2>/dev/null || echo "Failed to retrieve instance list"
    echo ""

    echo "Instance Summary:"
    echo "-----------------"
    RUNNING=$(oci compute instance list --lifecycle-state RUNNING --query "length(data)" --raw-output 2>/dev/null || echo "0")
    STOPPED=$(oci compute instance list --lifecycle-state STOPPED --query "length(data)" --raw-output 2>/dev/null || echo "0")
    echo "Running instances: $RUNNING"
    echo "Stopped instances: $STOPPED"
    echo ""

    # Estimate costs (simplified - adjust based on your instance types)
    # This is a placeholder - actual cost calculation would need instance shapes and pricing
    echo "Cost Estimation:"
    echo "----------------"
    echo "⚠️  Note: Actual costs depend on instance shapes, storage, and usage."
    echo "    Use OCI Cost Management Console for accurate billing."
    echo ""
    echo "Estimated Daily Cost: \$[Calculate based on running instances]"
    echo "Estimated Monthly Cost: \$[Calculate based on running instances * 30]"
    echo ""
    echo "Cost Optimization Tips:"
    echo "- Stop non-production instances during off-hours"
    echo "- Use smaller instance shapes for dev/staging"
    echo "- Enable auto-scaling for production workloads"
    echo "- Review and terminate unused resources"

} > "$REPORT_FILE"

log_action "Report saved: $REPORT_FILE"
cat "$REPORT_FILE"
