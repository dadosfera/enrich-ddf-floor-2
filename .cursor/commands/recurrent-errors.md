# /recurrent-errors

Document and prevent recurring errors by creating a standardized entry, adding backlinks, updating indexes, and committing the changes. Use this when the same error appears more than once or is likely to recur.

Backlinks:

- mini_prompt/lv1/recurrent_errors_mini_prompt.md
- \_dev/docs/recurrent_errors/README.md

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Set variables (edit `ERR_SLUG`)

```bash
ERR_SLUG="brief-error-slug"   # e.g., safe-rm-path-confusion
DATE=$(date +%Y-%m-%d)

# Resolve recurrent errors directory (repo-compatible)
if [ -d "_dev/docs/recurrent_errors" ]; then
  REC_DIR="_dev/docs/recurrent_errors"
else
  REC_DIR="docs/recurrent_errors"
fi

ERR_FILE="$REC_DIR/${DATE}_${ERR_SLUG}.md"
```

3. Ensure target directory exists

```bash
gtimeout 5 mkdir -p "$REC_DIR"
```

4. Check for an entry template (optional but preferred)

```bash
gtimeout 5 ls -1 "$REC_DIR/recurrent_error_template.md"
```

5. Create the entry from template (if present)

```bash
gtimeout 5 cp "$REC_DIR/recurrent_error_template.md" "$ERR_FILE"
```

5.1) If no template exists, create a minimal scaffold

```bash
cat > "$ERR_FILE" << 'EOF'
### Title: <Human-readable error name>

#### Symptoms
- Brief, exact symptoms and visible impact

#### Root cause
- Confirmed cause with minimal reproduction evidence

#### Fix
- What changed and why

#### Prevention
- Guardrails, tests, tooling, or processes to reduce recurrence

#### Impacted areas
- List affected scripts/docs/systems

#### Metadata
- Status: one_off  # or recurrent
- Occurrence count: 1
- First seen: <YYYY-MM-DD>
- Last seen: <YYYY-MM-DD>

#### Backlinks
- Related: <add links to affected docs/scripts>
EOF
```

6. Open and complete the entry content (manual edit)

- Fill Symptoms, Root cause, Fix, Prevention, Impacted areas
- Set Metadata.Status to `one_off` or `recurrent` and update Occurrence count
- Add Backlinks to affected docs/scripts (see step 8)

7. Update the recurrent errors index (add an entry under `files`)

```bash
# Detect index path
if [ -f "_dev/docs/recurrent_errors/index.yaml" ]; then
  INDEX_FILE="_dev/docs/recurrent_errors/index.yaml"
elif [ -f "docs/recurrent_errors/index.yaml" ]; then
  INDEX_FILE="docs/recurrent_errors/index.yaml"
else
  INDEX_FILE="$REC_DIR/index.yaml"
fi
echo "$INDEX_FILE"
```

Paste this YAML under the `files:` list in the index (adjust description):

```yaml
- path: "docs/recurrent_errors/${DATE}_${ERR_SLUG}.md"
  status: "recurrent" # or "one_off"
  description: "Short, human-readable title"
```

8. Add backlinks in affected docs/scripts (manual edit)

- In each affected file, add a small “Related” or “See also” section with a link back to the new entry, for example:

```markdown
Related: docs/recurrent_errors/${DATE}_${ERR_SLUG}.md
```

9. Optional cross-index updates (when relevant)

- Add/refresh entries or cross-references in:
  - `trouble_shooting/index.yaml`
  - `lessons_learned/index.yaml`

10. Version control (stage, commit, push)

```bash
gtimeout 10 git add -A
```

```bash
gtimeout 5 git status --short | head -30
```

```bash
gtimeout 10 git commit -m "Recurrent error doc: ${ERR_SLUG} (${DATE}); add backlinks and index entries"
```

```bash
gtimeout 15 git push
```

## Notes

- Keep commands unchained and short; run one step at a time
- Use the template when possible for consistency
- Backlinks are critical for discoverability in affected areas
- If the cause/process implies a rules or tooling improvement, propose a rule update and run distribution workflows separately

---

**Last updated**: 2025-11-09
