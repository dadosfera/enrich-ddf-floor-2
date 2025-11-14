#!/bin/bash
# scripts/access_ignored_file.sh
# AI helper script for accessing specific ignored files

FILE_PATH="$1"
ACTION="${2:-read}"
SEARCH_TERM="$3"

if [ -z "$FILE_PATH" ]; then
    echo "Usage: $0 <file_path> [read|edit|search] [search_term]"
    echo ""
    echo "Examples:"
    echo "  $0 logs/error.log read"
    echo "  $0 model_cache/config.json edit"
    echo "  $0 logs/app.log search 'ERROR'"
    echo ""
    echo "Actions:"
    echo "  read   - Display file contents"
    echo "  edit   - Prepare for editing (shows path for AI tools)"
    echo "  search - Search for term in file"
    exit 1
fi

# Security check - prevent access to sensitive files
SENSITIVE_PATTERNS=(".env" "secrets/" "credentials/" "*.key" "*.pem" "*.crt")
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "🚨 SECURITY WARNING: Attempting to access sensitive file: $FILE_PATH"
        echo "❌ Access denied for security reasons"
        exit 1
    fi
done

case "$ACTION" in
    "read")
        echo "📖 Reading ignored file: $FILE_PATH"
        if [ -f "$FILE_PATH" ]; then
            echo "--- File Contents ---"
            cat "$FILE_PATH"
            echo "--- End of File ---"
        else
            echo "❌ File not found: $FILE_PATH"
            echo "💡 Check if the file exists and path is correct"
        fi
        ;;
    "edit")
        echo "✏️  Opening ignored file for editing: $FILE_PATH"
        if [ -f "$FILE_PATH" ]; then
            echo "✅ File exists and is accessible"
            echo "🔧 Use AI edit_file tool with path: '$FILE_PATH'"
            echo "💡 Example: edit_file '$FILE_PATH'"
        else
            echo "❌ File not found: $FILE_PATH"
            echo "💡 Check if the file exists and path is correct"
        fi
        ;;
    "search")
        if [ -z "$SEARCH_TERM" ]; then
            echo "❌ Search term required for 'search' action"
            echo "💡 Usage: $0 <file_path> search <search_term>"
            exit 1
        fi
        echo "🔍 Searching for '$SEARCH_TERM' in: $FILE_PATH"
        if [ -f "$FILE_PATH" ]; then
            grep -n "$SEARCH_TERM" "$FILE_PATH" 2>/dev/null || echo "❌ No matches found"
        else
            echo "❌ File not found: $FILE_PATH"
        fi
        ;;
    *)
        echo "❌ Unknown action: $ACTION"
        echo "💡 Valid actions: read, edit, search"
        exit 1
        ;;
esac
