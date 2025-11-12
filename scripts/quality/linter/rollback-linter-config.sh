#!/bin/bash
# Rollback linter configuration from backup

set -e

REPO_PATH="$1"
BACKUP_DIR="$2"

if [ -z "$REPO_PATH" ] || [ -z "$BACKUP_DIR" ]; then
    echo "Usage: $0 <repo_path> <backup_directory>"
    echo ""
    echo "Example:"
    echo "  $0 ~/local_repos/my-repo .linter-config-backup-20251112_123456"
    exit 1
fi

if [ ! -d "$REPO_PATH/$BACKUP_DIR" ]; then
    echo "❌ Error: Backup directory not found: $REPO_PATH/$BACKUP_DIR"
    exit 1
fi

echo "⏪ Rolling back linter configuration for: $(basename "$REPO_PATH")"
echo "   Backup: $BACKUP_DIR"

# Restore files
if [ -f "$REPO_PATH/$BACKUP_DIR/pyproject.toml" ]; then
    cp "$REPO_PATH/$BACKUP_DIR/pyproject.toml" "$REPO_PATH/pyproject.toml"
    echo "   ✅ Restored pyproject.toml"
fi

if [ -f "$REPO_PATH/$BACKUP_DIR/.pre-commit-config.yaml" ]; then
    cp "$REPO_PATH/$BACKUP_DIR/.pre-commit-config.yaml" "$REPO_PATH/.pre-commit-config.yaml"
    echo "   ✅ Restored .pre-commit-config.yaml"
fi

if [ -f "$REPO_PATH/$BACKUP_DIR/.eslintrc.json" ]; then
    cp "$REPO_PATH/$BACKUP_DIR/.eslintrc.json" "$REPO_PATH/.eslintrc.json"
    echo "   ✅ Restored .eslintrc.json"
fi

echo ""
echo "✅ Rollback complete!"
echo "📋 Next steps:"
echo "   1. Review changes: git diff"
echo "   2. Test: pre-commit run --all-files"
echo "   3. Commit if satisfied: git add -A && git commit -m 'chore: rollback linter configuration'"
