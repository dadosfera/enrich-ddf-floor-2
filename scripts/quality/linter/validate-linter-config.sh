#!/bin/bash
# Validate linter configuration in a repository

set -e

REPO_PATH="${1:-.}"

echo "🔍 Validating linter configuration: $(basename "$REPO_PATH")"

errors=0
warnings=0

cd "$REPO_PATH" || exit 1

# Check Python config
if [ -f "pyproject.toml" ]; then
    echo "🐍 Checking Python configuration..."

    if ! grep -q "\[tool.ruff" pyproject.toml; then
        echo "   ⚠️  Warning: No ruff configuration found"
        warnings=$((warnings + 1))
    else
        echo "   ✅ Ruff configuration found"
    fi

    # Check for cosmetic rules ignored
    if grep -q "TRY300\|SIM108\|PLR0915" pyproject.toml; then
        echo "   ✅ Cosmetic rules properly ignored"
    else
        echo "   ⚠️  Warning: Cosmetic rules may not be ignored"
        warnings=$((warnings + 1))
    fi
fi

# Check pre-commit config
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔧 Checking pre-commit configuration..."
    echo "   ✅ Pre-commit config found"

    if command -v pre-commit &> /dev/null; then
        echo "   Running pre-commit validation..."
        if pre-commit run --all-files 2>&1 | grep -q "All checks passed\|Passed"; then
            echo "   ✅ All pre-commit hooks passing"
        else
            echo "   ❌ Some pre-commit hooks failing"
            errors=$((errors + 1))
        fi
    else
        echo "   ⚠️  pre-commit not installed, skipping validation"
        warnings=$((warnings + 1))
    fi
else
    echo "   ⚠️  Warning: No pre-commit configuration found"
    warnings=$((warnings + 1))
fi

# Check ruff if available
if command -v ruff &> /dev/null && [ -f "pyproject.toml" ]; then
    echo "🔨 Checking ruff..."
    if ruff check . 2>&1 | grep -q "All checks passed"; then
        echo "   ✅ All ruff checks passing"
    else
        error_count=$(ruff check . 2>&1 | grep -c "error" || echo 0)
        if [ "$error_count" -gt 0 ]; then
            echo "   ❌ Found $error_count ruff errors"
            errors=$((errors + 1))
        fi
    fi
fi

# Summary
echo ""
echo "📊 Validation Summary:"
echo "   Errors: $errors"
echo "   Warnings: $warnings"

if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
    echo "   ✅ All checks passed!"
    exit 0
elif [ "$errors" -eq 0 ]; then
    echo "   ⚠️  Validation passed with warnings"
    exit 0
else
    echo "   ❌ Validation failed"
    exit 1
fi
