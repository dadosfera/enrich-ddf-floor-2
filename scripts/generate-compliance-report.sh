#!/bin/bash
# scripts/generate-compliance-report.sh
# Generate comprehensive compliance report

set -euo pipefail

REPOS_DIR="${REPOS_DIR:-$HOME/local_repos}"
REPORT_FILE="${1:-active/compliance-report-$(date +%Y-%m-%d).md}"

echo "📊 Generating compliance report..."
echo ""

{
    echo "# Resource Management Compliance Report"
    echo "Generated: $(date)"
    echo ""
    echo "## Executive Summary"
    echo ""

    TOTAL=0
    HAS_DETECT=0
    HAS_MAKEFILE=0
    HAS_COMPOSE=0
    HAS_LIMITS=0
    HAS_TIMEOUTS=0
    HAS_NODE=0
    HAS_DOCS=0

    echo "| Repository | Detect | Makefile | Compose | Limits | Timeouts | NODE | Docs | Score |"
    echo "|------------|--------|----------|---------|--------|----------|------|------|-------|"

    for repo in "$REPOS_DIR"/*/; do
        if [ ! -d "$repo" ]; then
            continue
        fi

        repo_name=$(basename "$repo")

        # Skip hidden directories
        if [[ "$repo_name" =~ ^\. ]]; then
            continue
        fi

        ((TOTAL++))

        detect="❌"
        makefile="❌"
        compose="❌"
        limits="❌"
        timeouts="❌"
        node="❌"
        docs="❌"
        score=0

        # Check resource detection
        if [ -f "$repo/scripts/detect_resources.sh" ]; then
            detect="✅"
            ((HAS_DETECT++))
            ((score++))
        fi

        # Check Makefile targets
        if [ -f "$repo/Makefile" ] && grep -q "detect-resources:" "$repo/Makefile" 2>/dev/null; then
            makefile="✅"
            ((HAS_MAKEFILE++))
            ((score++))
        fi

        # Check Docker Compose
        COMPOSE_FILE=""
        [ -f "$repo/compose.yml" ] && COMPOSE_FILE="$repo/compose.yml"
        [ -z "$COMPOSE_FILE" ] && [ -f "$repo/docker-compose.yml" ] && COMPOSE_FILE="$repo/docker-compose.yml"

        if [ -n "$COMPOSE_FILE" ]; then
            compose="✅"
            ((HAS_COMPOSE++))
            ((score++))

            # Check resource limits
            if grep -q "mem_limit:" "$COMPOSE_FILE" 2>/dev/null && grep -q "cpus:" "$COMPOSE_FILE" 2>/dev/null; then
                limits="✅"
                ((HAS_LIMITS++))
                ((score++))
            fi
        fi

        # Check timeouts
        if [ -f "$repo/Makefile" ] && grep -q "timeout\|gtimeout" "$repo/Makefile" 2>/dev/null; then
            timeouts="✅"
            ((HAS_TIMEOUTS++))
            ((score++))
        fi

        # Check NODE_OPTIONS
        if [ -f "$repo/package.json" ] && grep -q "NODE_OPTIONS" "$repo/package.json" 2>/dev/null; then
            node="✅"
            ((HAS_NODE++))
            ((score++))
        fi

        # Check docs
        if [ -f "$repo/README.md" ] && grep -q "Resource Management" "$repo/README.md" 2>/dev/null; then
            docs="✅"
            ((HAS_DOCS++))
            ((score++))
        fi

        echo "| $repo_name | $detect | $makefile | $compose | $limits | $timeouts | $node | $docs | $score/7 |"
    done

    echo ""
    echo "## Statistics"
    echo ""
    echo "Total Repositories: $TOTAL"
    echo ""
    echo "| Feature | Count | Percentage |"
    echo "|---------|-------|------------|"
    echo "| Resource Detection | $HAS_DETECT | $((HAS_DETECT * 100 / TOTAL))% |"
    echo "| Makefile Targets | $HAS_MAKEFILE | $((HAS_MAKEFILE * 100 / TOTAL))% |"
    echo "| Docker Compose | $HAS_COMPOSE | $((HAS_COMPOSE * 100 / TOTAL))% |"
    echo "| Resource Limits | $HAS_LIMITS | $((HAS_LIMITS * 100 / TOTAL))% |"
    echo "| Makefile Timeouts | $HAS_TIMEOUTS | $((HAS_TIMEOUTS * 100 / TOTAL))% |"
    echo "| NODE_OPTIONS | $HAS_NODE | $((HAS_NODE * 100 / TOTAL))% |"
    echo "| Documentation | $HAS_DOCS | $((HAS_DOCS * 100 / TOTAL))% |"
    echo ""

    AVG_SCORE=$(( (HAS_DETECT + HAS_MAKEFILE + HAS_COMPOSE + HAS_LIMITS + HAS_TIMEOUTS + HAS_NODE + HAS_DOCS) * 100 / (TOTAL * 7) ))
    echo "**Average Compliance Score: $AVG_SCORE%**"
    echo ""
    echo "## Next Steps"
    echo ""
    echo "1. Review repos with low scores"
    echo "2. Add missing Makefile timeouts"
    echo "3. Add NODE_OPTIONS to package.json scripts"
    echo "4. Review Docker Compose resource limits"
    echo "5. Run validation: \`bash scripts/validate-all-repos.sh\`"
    echo ""

} > "$REPORT_FILE"

echo "✅ Compliance report generated: $REPORT_FILE"
