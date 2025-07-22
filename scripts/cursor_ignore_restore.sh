#!/bin/bash
# scripts/cursor_ignore_restore.sh
# Restore original .cursorignore exclusions

IGNORE_FILE=".cursorignore"
BACKUP_FILE=".cursorignore.backup"

if [ -f "$BACKUP_FILE" ]; then
    mv "$BACKUP_FILE" "$IGNORE_FILE"
    echo "✅ Restored original .cursorignore from backup"
    echo "📋 Backup file removed"
else
    echo "❌ No backup file found: $BACKUP_FILE"
    echo "💡 This means no override was performed or backup was already restored"
    exit 1
fi
