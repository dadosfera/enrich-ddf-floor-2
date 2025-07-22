#!/bin/bash
# scripts/cursor_ignore_override.sh
# Temporarily remove patterns from .cursorignore for AI access

IGNORE_FILE=".cursorignore"
BACKUP_FILE=".cursorignore.backup"
TARGET_PATTERN="$1"

if [ -z "$TARGET_PATTERN" ]; then
    echo "Usage: $0 <pattern_to_temporarily_allow>"
    echo "Example: $0 'logs/'"
    echo "Example: $0 '*.log'"
    echo "Example: $0 'venv/'"
    exit 1
fi

# Check if .cursorignore exists
if [ ! -f "$IGNORE_FILE" ]; then
    echo "❌ .cursorignore file not found"
    exit 1
fi

# Backup current .cursorignore
cp "$IGNORE_FILE" "$BACKUP_FILE"
echo "📋 Backed up current .cursorignore to $BACKUP_FILE"

# Remove the specified pattern (case-insensitive)
grep -v -i "$TARGET_PATTERN" "$IGNORE_FILE" > "$IGNORE_FILE.tmp"
mv "$IGNORE_FILE.tmp" "$IGNORE_FILE"

echo "✅ Temporarily allowed: $TARGET_PATTERN"
echo "💡 Run 'scripts/cursor_ignore_restore.sh' to restore original exclusions"
echo "⚠️  Remember to restore exclusions after AI work is complete" 