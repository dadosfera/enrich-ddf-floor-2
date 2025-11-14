#!/bin/bash

# IDE Configuration Helper for enrich-ddf-floor-2
# Helps configure IDEs to properly handle .env files

set -euo pipefail

echo "🔧 Configuring IDE settings for enrich-ddf-floor-2..."

# Create VSCode settings if VSCode is detected
if command -v code >/dev/null 2>&1; then
    echo "📝 Configuring VSCode settings..."

    mkdir -p .vscode

    cat > .vscode/settings.json << 'EOF'
{
  "files.associations": {
    ".env*": "properties",
    "*.env": "properties"
  },
  "shellcheck.ignorePatterns": {
    "**/.env*": true,
    "**/*.env": true
  },
  "[properties]": {
    "shellcheck.enable": false
  }
}
EOF

    echo "✅ VSCode settings configured"
fi

# Create Cursor settings if Cursor is detected
if command -v cursor >/dev/null 2>&1 || [ -d "/Applications/Cursor.app" ]; then
    echo "📝 Configuring Cursor settings..."

    mkdir -p .cursor

    cat > .cursor/settings.json << 'EOF'
{
  "files.associations": {
    ".env*": "properties",
    "*.env": "properties"
  },
  "shellcheck.ignorePatterns": {
    "**/.env*": true,
    "**/*.env": true
  },
  "[properties]": {
    "shellcheck.enable": false
  }
}
EOF

    echo "✅ Cursor settings configured"
fi

echo ""
echo "🎉 IDE configuration complete!"
echo ""
echo "📋 Manual configuration for other IDEs:"
echo "   1. Set file association for .env* files to 'properties' or 'dotenv'"
echo "   2. Disable shellcheck for .env files"
echo "   3. Add .env* to shellcheck ignore patterns"
echo ""
echo "🔍 If you still see shellcheck errors on .env files:"
echo "   1. Restart your IDE"
echo "   2. Check IDE-specific shellcheck settings"
echo "   3. Ensure .env files are recognized as 'properties' not 'shell'"
echo ""
