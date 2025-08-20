# MDC File Editing and Creation

## Priority

P1 (Critical): Must always be followed

## When to Use This Rule

**USE WHEN:**

- Creating or editing .mdc files (MarkDown Components)
- Working with files that contain YAML frontmatter
- Editing Nuxt Content files
- Working with MDC syntax (MarkDown Components)
- Need to preserve frontmatter structure

## Core Principle

**Use direct Unix tools with proper timeouts to edit .mdc files to properly preserve frontmatter and MDC syntax**

## Rule Statement

AI agents must use direct Unix tools (cat, echo, sed, awk, etc.) with mandatory timeouts when editing .mdc files to ensure proper handling of YAML frontmatter and MDC-specific syntax while preventing command hangs.

## MDC File Structure

### Basic .mdc File Format

````mdc
---
title: "Document Title"
description: "Document description"
date: 2025-01-03
authors:
  - name: "Author Name"
    email: "author@example.com"
tags:
  - tag1
  - tag2
---

# Main Content

Regular markdown content with MDC enhancements.

::alert{type="info"}
This is an MDC component
::

## Code Blocks

```typescript
const example = "syntax highlighted code";
````

### Inline Components

Use :component-name[content] for inline components.

### Block Components

::component-name{prop="value"}
Component content here
::

````

## Frontmatter Fields

### Essential Fields
- `title`: Document title (string, max 500 chars)
- `description`: Document description (string, max 500 chars)
- `date`: Publication date (YYYY-MM-DD format)
- `authors`: List of author objects with name, email, affiliations
- `tags`: List of strings for categorization

### Optional Fields
- `subtitle`: Subtitle (string, max 500 chars)
- `thumbnail`: Path to thumbnail image
- `banner`: Path to banner image
- `keywords`: List of keywords for SEO
- `license`: License information
- `draft`: Boolean for draft status
- `toc`: Table of contents configuration

## Direct Unix Tools Approach with Timeouts

### Reading .mdc Files (All commands must use timeouts)
```bash
# Read entire file preserving frontmatter
timeout 30s cat filename.mdc

# Read only frontmatter
timeout 15s sed -n '1,/^---$/p' filename.mdc

# Read only content (skip frontmatter)
timeout 30s bash -c 'sed "1,/^---$/d" filename.mdc | sed "1,/^---$/d"'

# Check if file has frontmatter
timeout 10s head -1 filename.mdc | timeout 5s grep -q '^---$'
````

### Creating New .mdc Files (With timeout protection)

```bash
# Create with frontmatter template
timeout 60s bash -c 'cat > new-file.mdc << "EOF"
---
title: "New Document"
description: "Document description"
date: $(date +%Y-%m-%d)
authors:
  - name: "Author Name"
---

# New Document

Content goes here.
EOF'
```

### Editing Frontmatter (With mandatory timeouts)

```bash
# Update title in frontmatter
timeout 30s sed -i 's/^title: .*/title: "New Title"/' filename.mdc

# Add new frontmatter field
timeout 30s sed -i '/^---$/a\
draft: true' filename.mdc

# Update date
timeout 30s sed -i "s/^date: .*/date: $(date +%Y-%m-%d)/" filename.mdc
```

### Editing Content (Preserving Frontmatter)

```bash
# Append content to end of file
echo "New content" >> filename.mdc

# Replace content section (preserve frontmatter)
{
  sed -n '1,/^---$/p' filename.mdc
  sed -n '1,/^---$/p' filename.mdc | tail -1
  echo "New content here"
} > temp.mdc && mv temp.mdc filename.mdc
```

## MDC Syntax Patterns

### Inline Components

```mdc
:component-name[text content]
:component-name{prop="value"}[text content]
```

### Block Components

```mdc
::component-name
Content here
::

::component-name{prop="value"}
Content with props
::
```

### Nested Components

```mdc
::parent-component
  :::child-component
  Child content
  :::
::
```

### Slots

```mdc
::component
Default slot content

#named-slot
Named slot content
::
```

## Command Safety and Timeout Requirements

### MANDATORY: All Commands Must Use Timeouts

**CRITICAL**: Every Unix command used for .mdc file editing MUST include a timeout to prevent hanging and ensure system stability.

#### Timeout Guidelines

- **File reading operations**: 30s max
- **Simple editing (sed, awk)**: 30s max
- **File creation**: 60s max
- **Complex operations**: 120s max
- **Validation commands**: 15s max

#### Pre-Execution Checklist

Before running ANY command on .mdc files:

1. ✅ Command includes appropriate timeout
2. ✅ File exists and is accessible
3. ✅ Backup created if modifying
4. ✅ Command syntax validated
5. ✅ Expected output/behavior confirmed

### Timeout Command Patterns

```bash
# CORRECT - With timeout
timeout 30s sed -i 's/old/new/' filename.mdc

# INCORRECT - Without timeout (FORBIDDEN)
sed -i 's/old/new/' filename.mdc

# CORRECT - Complex operations with timeout
timeout 60s bash -c 'complex_operation_here'

# CORRECT - Chained commands with individual timeouts
timeout 15s head -1 file.mdc | timeout 10s grep pattern
```

## Safe Editing Patterns

### Always Backup First (With timeout)

```bash
timeout 30s cp filename.mdc filename.mdc.backup
```

### Validate Frontmatter (With timeout)

```bash
# Check YAML validity
timeout 30s python3 -c "
import yaml
with open('filename.mdc', 'r') as f:
    content = f.read()
    if content.startswith('---'):
        frontmatter = content.split('---')[1]
        yaml.safe_load(frontmatter)
        print('Valid YAML frontmatter')
"
```

### Preserve Line Endings (With timeout)

```bash
# Use -i flag with sed for in-place editing
timeout 30s sed -i 's/old/new/' filename.mdc

# Or use temporary file approach
timeout 30s sed 's/old/new/' filename.mdc > temp.mdc && timeout 10s mv temp.mdc filename.mdc
```

## Common Editing Tasks

### Add New Author (With timeout)

```bash
# Add author to existing authors list
timeout 30s sed -i '/^authors:$/a\
  - name: "New Author"\
    email: "new@example.com"' filename.mdc
```

### Update Tags (With timeout)

```bash
# Replace entire tags section
timeout 30s sed -i '/^tags:$/,/^[^ ]/ { /^tags:$/!d; }' filename.mdc
timeout 30s sed -i '/^tags:$/a\
  - new-tag\
  - another-tag' filename.mdc
```

### Add MDC Component (With timeout)

```bash
# Append MDC component to content
timeout 30s bash -c 'cat >> filename.mdc << "EOF"

::alert{type="warning"}
This is a warning message
::
EOF'
```

## Error Prevention

### Validate Before Editing

1. Check file exists and is readable
2. Verify frontmatter syntax
3. Backup original file
4. Test changes on copy first

### Common Pitfalls to Avoid

- Don't break YAML frontmatter delimiters (---)
- Preserve indentation in YAML
- Don't mix tabs and spaces
- Maintain proper MDC component syntax
- Keep frontmatter at file beginning

## Integration with Build Tools

### Nuxt Content Compatibility

- Ensure frontmatter follows Nuxt Content schema
- Use proper date formats (ISO 8601)
- Follow naming conventions for components

### Validation Commands (With timeout)

```bash
# Check file structure
timeout 15s grep -n "^---$" filename.mdc | timeout 10s head -2

# Validate MDC syntax
timeout 15s grep -n "::" filename.mdc
```

## Examples

### Complete File Creation (With timeout protection)

```bash
#!/bin/bash
create_mdc_file() {
    local filename="$1"
    local title="$2"
    local description="$3"

    timeout 60s bash -c "cat > \"$filename\" << EOF
---
title: \"$title\"
description: \"$description\"
date: \$(date +%Y-%m-%d)
authors:
  - name: \"\$(timeout 10s git config user.name)\"
    email: \"\$(timeout 10s git config user.email)\"
tags: []
---

# $title

$description

## Content

Write your content here.

::alert{type=\"info\"}
This is an example MDC component
::
EOF"
}
```

### Bulk Update Script (With timeout protection)

```bash
#!/bin/bash
update_author_info() {
    local dir="$1"
    local old_name="$2"
    local new_name="$3"

    timeout 300s find "$dir" -name "*.mdc" -exec timeout 30s sed -i "s/name: \"$old_name\"/name: \"$new_name\"/" {} \;
}
```

## Benefits

- Preserves frontmatter integrity
- Maintains proper YAML structure
- Handles MDC syntax correctly
- Prevents encoding issues
- Enables batch operations
- Provides reliable file manipulation
- **Prevents command hangs with mandatory timeouts**
- **Ensures system stability and responsiveness**

## Enforcement

**CRITICAL**: Any command executed without a timeout when working with .mdc files is a **VIOLATION** of this rule and must be immediately corrected.

### Timeout Violation Examples

```bash
# ❌ FORBIDDEN - No timeout
sed -i 's/old/new/' file.mdc

# ❌ FORBIDDEN - No timeout
cat > file.mdc << EOF
content
EOF

# ❌ FORBIDDEN - No timeout
python3 -c "process_file()"

# ✅ CORRECT - With timeout
timeout 30s sed -i 's/old/new/' file.mdc

# ✅ CORRECT - With timeout
timeout 60s bash -c 'cat > file.mdc << "EOF"
content
EOF'

# ✅ CORRECT - With timeout
timeout 30s python3 -c "process_file()"
```

This rule ensures proper handling of .mdc files while preserving their special structure and syntax requirements, with mandatory timeout protection to prevent system hangs.
