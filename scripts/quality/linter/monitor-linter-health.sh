#!/bin/bash
# Monitor linter health across all repos

REPO_BASE="$HOME/local_repos"
REPORT_FILE="active/linter-health-report-$(date +%Y%m%d_%H%M%S).txt"

echo "📊 Monitoring linter health across all repos..."
echo "Report: $REPORT_FILE"

{
    echo "Linter Health Report - $(date)"
    echo "=================================="
    echo ""

    total_repos=0
    healthy_repos=0
    unhealthy_repos=0
    no_config_repos=0

    for repo in "$REPO_BASE"/*/; do
        if [ ! -d "$repo" ] || [ ! -d "$repo/.git" ]; then
            continue
        fi

        repo_name=$(basename "$repo")
        total_repos=$((total_repos + 1))

        echo "📁 $repo_name"

        # Check for Python config
        if [ -f "$repo/pyproject.toml" ]; then
            if command -v ruff &> /dev/null; then
                cd "$repo" || continue
                error_count=$(ruff check . 2>&1 | grep -c "error" || echo 0)
                if [ "$error_count" -eq 0 ]; then
                    echo "   ✅ Python: Healthy (0 errors)"
                    healthy_repos=$((healthy_repos + 1))
                else
                    echo "   ❌ Python: $error_count errors"
                    unhealthy_repos=$((unhealthy_repos + 1))
                fi
                cd - > /dev/null || true
            else
                echo "   ⚠️  Python: ruff not available"
            fi
        else
            echo "   ℹ️  No Python config"
        fi

        # Check pre-commit
        if [ -f "$repo/.pre-commit-config.yaml" ]; then
            echo "   ✅ Pre-commit: Configured"
        else
            echo "   ⚠️  Pre-commit: Not configured"
            no_config_repos=$((no_config_repos + 1))
        fi

        echo ""
    done

    echo "=================================="
    echo "Summary:"
    echo "  Total repos: $total_repos"
    echo "  Healthy: $healthy_repos"
    echo "  Unhealthy: $unhealthy_repos"
    echo "  No config: $no_config_repos"
} | tee "$REPORT_FILE"

echo ""
echo "✅ Report saved to: $REPORT_FILE"
