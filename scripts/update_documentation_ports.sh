#!/bin/bash

# Script to update hardcoded port references in documentation
# Part of the Dynamic Port Configuration Plan

set -euo pipefail

# Configuration
OLD_PORT="8000"
NEW_PORT="\${APP_PORT:-8247}"
BACKUP_DIR=".tmp/port_migration_backup_$(date +%Y%m%d_%H%M%S)"

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "🔄 Starting port migration from $OLD_PORT to dynamic configuration..."
echo "📁 Backup directory: $BACKUP_DIR"

# Function to update files
update_file() {
    local file="$1"
    local description="$2"
    
    if [[ -f "$file" ]]; then
        echo "  📝 Updating $description: $file"
        # Create backup
        cp "$file" "$BACKUP_DIR/$(basename "$file").backup"
        
        # Replace hardcoded ports with environment variable syntax
        sed -i.tmp \
            -e "s|http://localhost:$OLD_PORT|http://localhost:$NEW_PORT|g" \
            -e "s|http://0\\.0\\.0\\.0:$OLD_PORT|http://0.0.0.0:$NEW_PORT|g" \
            -e "s|:$OLD_PORT/|:$NEW_PORT/|g" \
            -e "s|port $OLD_PORT|port $NEW_PORT|g" \
            -e "s|Port $OLD_PORT|Port $NEW_PORT|g" \
            "$file"
        
        # Remove temporary file
        rm -f "$file.tmp"
    else
        echo "  ⚠️  File not found: $file"
    fi
}

# List of files to update
echo "📋 Updating documentation files..."

# Active directory files
update_file "active/01_immediate_priorities.md" "Immediate Priorities"
update_file "active/02_technical_roadmap.md" "Technical Roadmap"
update_file "active/03_execution_commands.md" "Execution Commands"
update_file "active/04_current_status.md" "Current Status"
update_file "active/04_current_status_summary.md" "Current Status Summary"
update_file "active/05_execution_summary.md" "Execution Summary"
update_file "active/05_final_execution_summary.md" "Final Execution Summary"
update_file "active/06_latest_execution_summary.md" "Latest Execution Summary"
update_file "active/07_final_status_update.md" "Final Status Update"
update_file "active/08_comprehensive_execution_summary.md" "Comprehensive Execution Summary"
update_file "active/09_retry_execution_summary.md" "Retry Execution Summary"

# Update README files if they exist
update_file "README.md" "Main README"
update_file "docs/README.md" "Documentation README"

# Create migration summary
cat > "$BACKUP_DIR/migration_summary.md" << EOF
# Port Migration Summary

## Migration Details
- **Date**: $(date)
- **Old Port**: $OLD_PORT (hardcoded)
- **New Port**: \${APP_PORT:-8247} (dynamic)
- **Backup Location**: $BACKUP_DIR

## Files Updated
$(find active/ -name "*.md" -type f | wc -l) documentation files in active/ directory

## Environment Variable Usage
The new configuration uses environment variables:
\`\`\`bash
export APP_PORT=8247  # or any other port
\`\`\`

## Rollback Instructions
To rollback changes:
\`\`\`bash
# Restore from backup
for file in $BACKUP_DIR/*.backup; do
    if [[ -f "\$file" ]]; then
        original_name=\$(basename "\$file" .backup)
        cp "\$file" "active/\$original_name"
    fi
done
\`\`\`

## Testing
After migration, test with:
\`\`\`bash
# Start application
APP_PORT=8247 python main.py

# Test endpoints
curl http://localhost:\${APP_PORT:-8247}/health
curl http://localhost:\${APP_PORT:-8247}/
\`\`\`
EOF

echo "✅ Port migration completed!"
echo "📊 Summary:"
echo "   - Backup created in: $BACKUP_DIR"
echo "   - Files updated with dynamic port configuration"
echo "   - Default port changed from $OLD_PORT to 8247"
echo "   - Use APP_PORT environment variable to override"
echo ""
echo "🧪 Test the migration:"
echo "   APP_PORT=8247 python main.py"
echo ""
echo "📖 View migration details:"
echo "   cat $BACKUP_DIR/migration_summary.md" 