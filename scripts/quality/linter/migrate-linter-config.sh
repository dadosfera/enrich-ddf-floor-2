#!/bin/bash
# Migrate a repository to standardized linter configuration

set -e

REPO_PATH="$1"
TEMPLATE_BASE="$(cd "$(dirname "$0")/../../.." && pwd)"
BACKUP_DIR=".linter-config-backup-$(date +%Y%m%d_%H%M%S)"

# Safety checks
if [ -z "$REPO_PATH" ]; then
    echo "Usage: $0 <repo_path>"
    exit 1
fi

if [ ! -d "$REPO_PATH" ]; then
    echo "❌ Error: Repository path does not exist: $REPO_PATH"
    exit 1
fi

if [ ! -d "$REPO_PATH/.git" ]; then
    echo "⚠️  Warning: Not a git repository: $REPO_PATH"
    read -p "Continue anyway? (y/N): " confirm
    if [ "$confirm" != "y" ]; then
        exit 1
    fi
fi

echo "🔄 Migrating linter configuration for: $(basename "$REPO_PATH")"
echo "   Path: $REPO_PATH"

# Backup existing configs
echo "📦 Creating backup..."
mkdir -p "$REPO_PATH/$BACKUP_DIR"
[ -f "$REPO_PATH/pyproject.toml" ] && cp "$REPO_PATH/pyproject.toml" "$REPO_PATH/$BACKUP_DIR/" || true
[ -f "$REPO_PATH/.pre-commit-config.yaml" ] && cp "$REPO_PATH/.pre-commit-config.yaml" "$REPO_PATH/$BACKUP_DIR/" || true
[ -f "$REPO_PATH/.eslintrc.json" ] && cp "$REPO_PATH/.eslintrc.json" "$REPO_PATH/$BACKUP_DIR/" || true

# Check if repo has Python files
has_python=false
if find "$REPO_PATH" -maxdepth 2 -name "*.py" -type f | head -1 | grep -q .; then
    has_python=true
fi

# Check if repo has JavaScript/TypeScript files
has_js=false
if find "$REPO_PATH" -maxdepth 2 \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.jsx" \) -type f | head -1 | grep -q .; then
    has_js=true
fi

# Apply Python template if needed
if [ "$has_python" = true ]; then
    echo "🐍 Applying Python/Ruff configuration..."
    cp "$TEMPLATE_BASE/templates/pyproject.toml.template" "$REPO_PATH/pyproject.toml"
    echo "   ✅ pyproject.toml updated"
fi

# Apply pre-commit template
echo "🔧 Applying pre-commit configuration..."
cp "$TEMPLATE_BASE/templates/.pre-commit-config.yaml.template" "$REPO_PATH/.pre-commit-config.yaml"
echo "   ✅ .pre-commit-config.yaml updated"

# Run auto-fixes if Python
if [ "$has_python" = true ]; then
    echo "🔨 Running auto-fixes..."
    cd "$REPO_PATH" || exit 1

    # Install pre-commit if not available
    if ! command -v pre-commit &> /dev/null; then
        echo "   ⚠️  pre-commit not found, skipping hooks"
    else
        # Run ruff auto-fixes
        if command -v ruff &> /dev/null; then
            echo "   Running ruff --fix..."
            ruff check . --fix --unsafe-fixes 2>&1 | tail -5 || true
        fi

        # Install pre-commit hooks
        echo "   Installing pre-commit hooks..."
        pre-commit install 2>&1 | grep -v "already installed" || true
    fi
fi

# Report
echo ""
echo "✅ Migration complete for $(basename "$REPO_PATH")"
echo "📦 Backup saved to: $BACKUP_DIR"
echo ""
echo "📋 Next steps:"
echo "   1. Review changes: git diff"
echo "   2. Test: pre-commit run --all-files"
echo "   3. Commit if satisfied: git add -A && git commit -m 'chore: standardize linter configuration'"
