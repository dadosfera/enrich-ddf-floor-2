#!/bin/bash
# Auto-generated rollback script for linting auto-fix operations

set -e

BASELINE_TAG="${1:-auto-fix-baseline-$(date +%Y%m%d)*}"

echo "🔄 Rolling back to baseline: $BASELINE_TAG"

# Find the most recent baseline tag if not specified
if [[ "$BASELINE_TAG" == *"*"* ]]; then
    BASELINE_TAG=$(git tag -l "auto-fix-baseline-*" | sort -V | tail -1)
    echo "📍 Using most recent baseline: $BASELINE_TAG"
fi

# Verify tag exists
if ! git tag -l | grep -q "^$BASELINE_TAG$"; then
    echo "❌ Baseline tag not found: $BASELINE_TAG"
    git tag -l "auto-fix-baseline-*" | tail -5
    exit 1
fi

# Reset to baseline
git reset --hard "$BASELINE_TAG"
echo "✅ Repository rolled back to: $BASELINE_TAG"

# Clean any auto-fix artifacts
rm -f .eslintcache .prettierignore.bak lint_report.md rollback_auto_fix.sh
echo "✅ Cleaned auto-fix artifacts"

echo "🎯 Rollback completed successfully"