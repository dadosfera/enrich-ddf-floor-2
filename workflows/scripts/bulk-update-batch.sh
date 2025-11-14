#!/bin/bash
# scripts/bulk-update-batch.sh
# Update multiple repositories in batch

set -euo pipefail

BATCH=${1:-"high-priority"}
REPOS_DIR="${REPOS_DIR:-$HOME/local_repos}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

case "$BATCH" in
  high-priority)
    REPOS=(
      "map-ddf-floor-2"
      "planner-ddf-floor-2"
      "news-ddf-floor-2"
      "ai-flow-module"
      "framework-ddf"
      "monitor-ddf"
      "assistant-ddf"
      "cline-ddf"
      "meta-assistant-ddf"
      "deployer-ddf-mod-open-llms"
    )
    ;;
  medium-priority)
    REPOS=(
      "assessment-ddf"
      "budget-ddf"
      "conversor-ddf"
      "crm-ddf"
      "dataapp-data-input"
      "extractor-ddf"
      "proc-ddf"
      "proto-ddf"
    )
    ;;
  low-priority)
    REPOS=(
      "3d-ddf"
      "auto-drive-v2-try-2"
      "beast"
      "central-forecast-ddf-group"
      "enrich-ddf-group"
      "enrich-ddf-mod-ncm"
      "solver-mod-bet"
      "docs-fera"
      "prompts-fera"
      "scripts-fera"
      "workflows-fera"
    )
    ;;
  pilot)
    REPOS=(
      "agent-ddf"
      "gen-ddf-floor-2"
    )
    ;;
  *)
    echo "Unknown batch: $BATCH"
    echo "Valid batches: pilot, high-priority, medium-priority, low-priority"
    exit 1
    ;;
esac

echo "🚀 Batch update: $BATCH"
echo "Repositories: ${#REPOS[@]}"
echo ""

SUCCESS=0
FAILED=0
SKIPPED=0

for repo in "${REPOS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Processing: $repo"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [ ! -d "$REPOS_DIR/$repo" ]; then
        echo "⚠️  Repository not found: $repo (skipping)"
        ((SKIPPED++))
        echo ""
        continue
    fi

    if bash "$SCRIPT_DIR/bulk-update-repo.sh" "$REPOS_DIR/$repo" 2>&1; then
        echo "✅ Success: $repo"
        ((SUCCESS++))
    else
        echo "❌ Failed: $repo"
        ((FAILED++))
    fi

    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Batch Update Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Success: $SUCCESS"
echo "Failed: $FAILED"
echo "Skipped: $SKIPPED"
echo "Total: ${#REPOS[@]}"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "⚠️  Some repositories failed. Review logs above."
    exit 1
else
    echo "🎉 All repositories updated successfully!"
fi
