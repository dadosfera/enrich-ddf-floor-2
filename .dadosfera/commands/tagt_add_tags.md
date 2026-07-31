---
category: quality
criticality: high
scope: all
---
# /tagt_add_tags
<!-- COMMAND_ID: 074 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ta_add_tags -->

Interactive command to add or update tags (category, criticality, scope) to artifacts (commands, rules, hooks, mini prompts) following the Extended Tagging Standard.

**Local Reference**: `commands/tagt_add_tags.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/tagt_add_tags.md`

Backlinks:
- standards/tagging/testing_tagging_standard_extended.md
- _dev/scripts/quality_governance/validate_tags.py
- _dev/hooks/pre-commit-validate-tags.py
- mini_prompt/lv1/tagging_artifacts_lv1_mini_prompt.md

## When to Use

- When adding tags to new artifacts
- When updating tags on existing artifacts
- When batch tagging multiple files
- When unsure about appropriate tag values (command provides suggestions)

## Command sequence (run in order)

### 2. Detect file type and validate

```bash
# Determine file type
if [[ "$file" == *.md ]] || [[ "$file" == *.mdc ]]; then
  FILE_TYPE="markdown"
elif [[ "$file" == *.yaml ]] || [[ "$file" == *.yml ]]; then
  FILE_TYPE="yaml"
elif [[ "$file" == *.sh ]]; then
  FILE_TYPE="shell"
else
  echo "❌ Unsupported file type: $file"
  exit 1
fi

# Verify file exists
if [[ ! -f "$file" ]]; then
  echo "❌ File not found: $file"
  exit 1
fi
```

### 3. Extract existing tags (if any)

Use `validate_tags.py` functions to extract existing tags:
- For Markdown: `get_markdown_tags(path)`
- For YAML: `get_yaml_tags(path)`
- For Shell: `get_shell_tags(path)`

Display existing tags to user:

```bash
if existing_tags; then
  echo "Current tags:"
  echo "  Category: ${existing_category:-none}"
  echo "  Criticality: ${existing_criticality:-none}"
  echo "  Scope: ${existing_scope:-none}"
fi
```

### 5. Interactive tag selection

For each tag (category, criticality, scope):

```bash
# Category (required)
echo "Select category (required):"
echo "Allowed values: testing, distribution, validation, safety, automation, git, infrastructure, documentation, quality, planning, architecture"
echo "Suggested: $suggested_category"
read -p "Category: " selected_category

# Validate category
if ! validate_category "$selected_category"; then
  echo "❌ Invalid category. Please choose from allowed values."
  # Re-prompt
fi

# Criticality (optional)
echo "Select criticality (optional, press Enter to skip):"
echo "Allowed values: critical, high, medium, low"
echo "Suggested: $suggested_criticality"
read -p "Criticality: " selected_criticality

# Scope (optional)
echo "Select scope (optional, press Enter to skip):"
echo "Allowed values: infra, integration, docs, local, ci-cd, all"
echo "Suggested: $suggested_scope"
read -p "Scope: " selected_scope
```

### 6. Validate tags

Run validation using `validate_tags.py`:

```bash
python3 _dev/scripts/quality_governance/validate_tags.py "$file"
```

### 7. Add/update tags in file

**For Markdown files:**
- Add or update YAML frontmatter at the top of file
- Preserve existing frontmatter if present
- Format:

```yaml
---
category: <value>
criticality: <value>  # optional
scope: <value>        # optional
---
```

### 8. Report success/failure

```bash
if validation_passed; then
  echo "✅ Tags added successfully to $file"
  echo "   Category: $selected_category"
  echo "   Criticality: ${selected_criticality:-not set}"
  echo "   Scope: ${selected_scope:-not set}"
else
  echo "❌ Failed to add tags. Validation errors:"
  echo "$validation_errors"
  exit 1
fi
```

### 9. Batch operation summary (if multiple files)

If processing multiple files:

```bash
echo ""
echo "Summary:"
echo "  Total files: $total_files"
echo "  Successfully tagged: $success_count"
echo "  Failed: $failure_count"
```
