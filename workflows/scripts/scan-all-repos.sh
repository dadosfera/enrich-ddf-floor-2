#!/bin/bash

# Comprehensive Repository Scanner
# Scans all local repos for resource management compliance
# Version: 1.0.0

set -euo pipefail

REPOS_DIR="${REPOS_DIR:-$HOME/local_repos}"
REPORT_FILE="${1:-active/repo-baseline-$(date +%Y-%m-%d).md}"

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔍 Scanning all repositories in: $REPOS_DIR"
echo "📊 Report will be saved to: $REPORT_FILE"
echo ""

# Initialize counters
TOTAL=0
HAS_COMPOSE=0
HAS_TIMEOUTS=0
HAS_CAPS=0
HAS_PORTS=0
HAS_COSTS=0
HAS_HEALTH=0
HAS_LOGS=0
HAS_TESTS=0

{
    echo "# Repository Resource Management Baseline Scan"
    echo "Generated: $(date)"
    echo ""
    echo "## Summary"
    echo ""
    echo "| Metric | Count | Percentage |"
    echo "|--------|-------|------------|"

    # Scan all repos
    for repo in "$REPOS_DIR"/*/; do
        if [ ! -d "$repo" ]; then
            continue
        fi

        repo_name=$(basename "$repo")
        ((TOTAL++))

        # Skip hidden directories
        if [[ "$repo_name" =~ ^\. ]]; then
            continue
        fi

        # Initialize flags
        has_compose="❌"
        has_timeouts="❌"
        has_caps="❌"
        has_ports="❌"
        has_costs="❌"
        has_health="❌"
        has_logs="❌"
        has_tests="❌"
        score=0

        # Check Docker Compose
        if [ -f "$repo/compose.yml" ] || [ -f "$repo/docker-compose.yml" ] || [ -d "$repo/docker" ]; then
            has_compose="✅"
            ((HAS_COMPOSE++))
            ((score++))
        fi

        # Check Makefile timeouts
        if [ -f "$repo/Makefile" ]; then
            if grep -q "timeout\|gtimeout" "$repo/Makefile" 2>/dev/null; then
                has_timeouts="✅"
                ((HAS_TIMEOUTS++))
                ((score++))
            fi
        fi

        # Check resource caps
        if grep -q "mem_limit\|cpus" "$repo"/*.yml 2>/dev/null || \
           grep -q "mem_limit\|cpus" "$repo"/docker/*.yml 2>/dev/null || \
           grep -q "mem_limit\|cpus" "$repo"/config/docker/*.yml 2>/dev/null; then
            has_caps="✅"
            ((HAS_CAPS++))
            ((score++))
        fi

        # Check port management
        if [ -f "$repo/config/ports.js" ] || grep -q "PORT_REGISTRY\|port.*check" "$repo"/*.sh 2>/dev/null; then
            has_ports="✅"
            ((HAS_PORTS++))
            ((score++))
        fi

        # Check cost controls
        if [ -d "$repo/scripts/cost" ] || grep -q "cloud-stop\|cloud-cost" "$repo/Makefile" 2>/dev/null; then
            has_costs="✅"
            ((HAS_COSTS++))
            ((score++))
        fi

        # Check health checks
        if grep -q "healthcheck:" "$repo"/*.yml 2>/dev/null || \
           grep -q "healthcheck:" "$repo"/docker/*.yml 2>/dev/null || \
           grep -q "healthcheck:" "$repo"/config/docker/*.yml 2>/dev/null; then
            has_health="✅"
            ((HAS_HEALTH++))
            ((score++))
        fi

        # Check log rotation
        if grep -q "max-size\|max-file" "$repo"/*.yml 2>/dev/null || \
           grep -q "max-size\|max-file" "$repo"/docker/*.yml 2>/dev/null || \
           grep -q "max-size\|max-file" "$repo"/config/docker/*.yml 2>/dev/null; then
            has_logs="✅"
            ((HAS_LOGS++))
            ((score++))
        fi

        # Check adaptive testing
        if [ -f "$repo/scripts/detect_resources.sh" ] || grep -q "test-auto\|detect-resources" "$repo/Makefile" 2>/dev/null; then
            has_tests="✅"
            ((HAS_TESTS++))
            ((score++))
        fi

        # Calculate percentage
        percentage=$((score * 100 / 8))

        # Store for detailed table
        echo "| $repo_name | $has_compose | $has_timeouts | $has_caps | $has_ports | $has_costs | $has_health | $has_logs | $has_tests | $score/8 |"
    done

    echo ""
    echo "## Statistics"
    echo ""
    echo "Total Repositories: $TOTAL"
    echo ""
    echo "| Feature | Count | Percentage |"
    echo "|---------|-------|------------|"
    echo "| Docker Compose | $HAS_COMPOSE | $((HAS_COMPOSE * 100 / TOTAL))% |"
    echo "| Makefile Timeouts | $HAS_TIMEOUTS | $((HAS_TIMEOUTS * 100 / TOTAL))% |"
    echo "| Resource Caps | $HAS_CAPS | $((HAS_CAPS * 100 / TOTAL))% |"
    echo "| Port Management | $HAS_PORTS | $((HAS_PORTS * 100 / TOTAL))% |"
    echo "| Cost Controls | $HAS_COSTS | $((HAS_COSTS * 100 / TOTAL))% |"
    echo "| Health Checks | $HAS_HEALTH | $((HAS_HEALTH * 100 / TOTAL))% |"
    echo "| Log Rotation | $HAS_LOGS | $((HAS_LOGS * 100 / TOTAL))% |"
    echo "| Adaptive Testing | $HAS_TESTS | $((HAS_TESTS * 100 / TOTAL))% |"
    echo ""
    echo "## Detailed Compliance Matrix"
    echo ""
    echo "| Repository | Compose | Timeouts | Caps | Ports | Costs | Health | Logs | Tests | Score |"
    echo "|------------|---------|----------|------|-------|-------|--------|------|-------|-------|"

    # Detailed scan
    for repo in "$REPOS_DIR"/*/; do
        if [ ! -d "$repo" ]; then
            continue
        fi

        repo_name=$(basename "$repo")

        # Skip hidden directories
        if [[ "$repo_name" =~ ^\. ]]; then
            continue
        fi

        has_compose="❌"
        has_timeouts="❌"
        has_caps="❌"
        has_ports="❌"
        has_costs="❌"
        has_health="❌"
        has_logs="❌"
        has_tests="❌"
        score=0

        # Check Docker Compose
        if [ -f "$repo/compose.yml" ] || [ -f "$repo/docker-compose.yml" ] || [ -d "$repo/docker" ]; then
            has_compose="✅"
            ((score++))
        fi

        # Check Makefile timeouts
        if [ -f "$repo/Makefile" ]; then
            if grep -q "timeout\|gtimeout" "$repo/Makefile" 2>/dev/null; then
                has_timeouts="✅"
                ((score++))
            fi
        fi

        # Check resource caps
        if grep -q "mem_limit\|cpus" "$repo"/*.yml 2>/dev/null || \
           grep -q "mem_limit\|cpus" "$repo"/docker/*.yml 2>/dev/null || \
           grep -q "mem_limit\|cpus" "$repo"/config/docker/*.yml 2>/dev/null; then
            has_caps="✅"
            ((score++))
        fi

        # Check port management
        if [ -f "$repo/config/ports.js" ] || grep -q "PORT_REGISTRY\|port.*check" "$repo"/*.sh 2>/dev/null; then
            has_ports="✅"
            ((score++))
        fi

        # Check cost controls
        if [ -d "$repo/scripts/cost" ] || grep -q "cloud-stop\|cloud-cost" "$repo/Makefile" 2>/dev/null; then
            has_costs="✅"
            ((score++))
        fi

        # Check health checks
        if grep -q "healthcheck:" "$repo"/*.yml 2>/dev/null || \
           grep -q "healthcheck:" "$repo"/docker/*.yml 2>/dev/null || \
           grep -q "healthcheck:" "$repo"/config/docker/*.yml 2>/dev/null; then
            has_health="✅"
            ((score++))
        fi

        # Check log rotation
        if grep -q "max-size\|max-file" "$repo"/*.yml 2>/dev/null || \
           grep -q "max-size\|max-file" "$repo"/docker/*.yml 2>/dev/null || \
           grep -q "max-size\|max-file" "$repo"/config/docker/*.yml 2>/dev/null; then
            has_logs="✅"
            ((score++))
        fi

        # Check adaptive testing
        if [ -f "$repo/scripts/detect_resources.sh" ] || grep -q "test-auto\|detect-resources" "$repo/Makefile" 2>/dev/null; then
            has_tests="✅"
            ((score++))
        fi

        echo "| $repo_name | $has_compose | $has_timeouts | $has_caps | $has_ports | $has_costs | $has_health | $has_logs | $has_tests | $score/8 |"
    done

    echo ""
    echo "## Next Steps"
    echo ""
    echo "1. Review compliance matrix above"
    echo "2. Prioritize repos by score (lowest first)"
    echo "3. Run bulk updater: \`bash scripts/bulk-update-batch.sh high-priority\`"
    echo "4. Validate changes: \`bash scripts/validate-all-repos.sh\`"
    echo ""

} > "$REPORT_FILE"

echo "✅ Scan complete!"
echo "📊 Report saved: $REPORT_FILE"
echo ""
echo "Summary:"
echo "  Total repos: $TOTAL"
echo "  With Compose: $HAS_COMPOSE"
echo "  With Timeouts: $HAS_TIMEOUTS"
echo "  With Resource Caps: $HAS_CAPS"
echo "  Average compliance: $(( (HAS_COMPOSE + HAS_TIMEOUTS + HAS_CAPS + HAS_PORTS + HAS_COSTS + HAS_HEALTH + HAS_LOGS + HAS_TESTS) * 100 / (TOTAL * 8) ))%"
