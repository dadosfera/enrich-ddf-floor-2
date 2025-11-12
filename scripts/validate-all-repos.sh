#!/bin/bash
# scripts/validate-all-repos.sh
# Validate resource management compliance across all repos

set -euo pipefail

REPOS_DIR="${REPOS_DIR:-$HOME/local_repos}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔍 Validating resource management compliance across all repos..."
echo ""

TOTAL=0
COMPLIANT=0
NON_COMPLIANT=0
ISSUES=0

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

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Validating: $repo_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    REPO_COMPLIANT=true
    REPO_ISSUES=0

    # Check 1: Resource detection script
    if [ -f "$repo/scripts/detect_resources.sh" ]; then
        echo "  ✅ Resource detection script present"
    else
        echo "  ❌ Resource detection script missing"
        REPO_COMPLIANT=false
        ((REPO_ISSUES++))
    fi

    # Check 2: Makefile targets
    if [ -f "$repo/Makefile" ]; then
        if grep -q "detect-resources:" "$repo/Makefile" 2>/dev/null; then
            echo "  ✅ Standardized Makefile targets present"
        else
            echo "  ⚠️  Standardized Makefile targets missing"
            ((REPO_ISSUES++))
        fi
    fi

    # Check 3: Docker Compose resource limits
    COMPOSE_FILE=""
    [ -f "$repo/compose.yml" ] && COMPOSE_FILE="$repo/compose.yml"
    [ -z "$COMPOSE_FILE" ] && [ -f "$repo/docker-compose.yml" ] && COMPOSE_FILE="$repo/docker-compose.yml"

    if [ -n "$COMPOSE_FILE" ]; then
        if grep -q "mem_limit:" "$COMPOSE_FILE" 2>/dev/null && grep -q "cpus:" "$COMPOSE_FILE" 2>/dev/null; then
            echo "  ✅ Docker Compose resource limits present"
        else
            echo "  ⚠️  Docker Compose resource limits missing"
            ((REPO_ISSUES++))
        fi

        if grep -q "max-size:" "$COMPOSE_FILE" 2>/dev/null; then
            echo "  ✅ Log rotation configured"
        else
            echo "  ⚠️  Log rotation missing"
            ((REPO_ISSUES++))
        fi
    fi

    # Check 4: Makefile timeouts
    if [ -f "$repo/Makefile" ]; then
        if grep -q "timeout\|gtimeout" "$repo/Makefile" 2>/dev/null; then
            echo "  ✅ Makefile timeouts present"
        else
            echo "  ⚠️  Makefile timeouts missing (manual update needed)"
            ((REPO_ISSUES++))
        fi
    fi

    # Check 5: NODE_OPTIONS (if Node.js repo)
    if [ -f "$repo/package.json" ]; then
        if grep -q "NODE_OPTIONS" "$repo/package.json" 2>/dev/null; then
            echo "  ✅ NODE_OPTIONS present"
        else
            echo "  ⚠️  NODE_OPTIONS missing (manual update needed)"
            ((REPO_ISSUES++))
        fi
    fi

    # Check 6: README documentation
    if [ -f "$repo/README.md" ]; then
        if grep -q "Resource Management" "$repo/README.md" 2>/dev/null; then
            echo "  ✅ README documentation present"
        else
            echo "  ⚠️  README documentation missing"
            ((REPO_ISSUES++))
        fi
    fi

    if [ "$REPO_COMPLIANT" = true ] && [ $REPO_ISSUES -eq 0 ]; then
        echo "  ${GREEN}✅ Fully compliant${NC}"
        ((COMPLIANT++))
    else
        echo "  ${YELLOW}⚠️  $REPO_ISSUES issue(s) found${NC}"
        ((NON_COMPLIANT++))
        ISSUES=$((ISSUES + REPO_ISSUES))
    fi

    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Validation Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total repos: $TOTAL"
echo "${GREEN}Fully compliant: $COMPLIANT${NC}"
echo "${YELLOW}Needs attention: $NON_COMPLIANT${NC}"
echo "Total issues: $ISSUES"
echo ""

if [ $ISSUES -eq 0 ]; then
    echo "${GREEN}✅ All repos are compliant!${NC}"
    exit 0
else
    echo "${YELLOW}⚠️  Some repos need manual updates${NC}"
    echo "See issues above for details"
    exit 0  # Don't fail - just report
fi
