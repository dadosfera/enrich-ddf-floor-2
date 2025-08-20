# Ignored File Access Protocol

## When AI Needs to Access Ignored Files

**DETECTION INDICATORS:**

- User mentions files that AI cannot find
- Error messages about missing files that should exist
- Request to edit files in excluded directories
- Need to access logs, configs, or generated content

**PROTOCOL:**

1. **Acknowledge the limitation**

   ```
   "I notice that [file/directory] may be in .cursorignore and not visible to me."
   ```

2. **Request explicit path**

   ```
   "Could you provide the exact file path so I can access it directly?"
   ```

3. **Use direct file operations**

   ```bash
   # Use explicit file paths with tools
   read_file "model_cache/specific_model.json"
   edit_file "logs/application.log"
   ```

4. **Offer temporary access solutions**
   ```
   "I can help you temporarily modify .cursorignore if you need me to have
   broader access to this directory."
   ```

## Common Ignored File Scenarios

**Scenario 1: Log File Analysis**

```
User: "Check the latest error in the logs"
AI Response: "I need the specific log file path since logs/ is excluded.
Could you specify which log file? For example: logs/error.log"
```

**Scenario 2: Model Configuration**

```
User: "Update the model config"
AI Response: "Model files are excluded from indexing. Please provide the
exact path to the config file, such as: model_cache/config.json"
```

**Scenario 3: Generated Content Review**

```
User: "Review the generated images"
AI Response: "Generated content is excluded. I can access specific files
if you provide paths like: generated_images/image_001.png"
```

## Emergency Access Commands

**Quick File Check:**

```bash
ls -la [ignored_directory]/
```

**Direct File Access:**

```bash
cat [ignored_file_path]
head -20 [ignored_file_path]
tail -20 [ignored_file_path]
```

**Search in Ignored Areas:**

```bash
find [ignored_directory] -name "*.ext" | head -10
grep -r "search_term" [ignored_directory]/ | head -10
```

## Management Scripts Usage

**Temporary Override:**

```bash
# Allow access to logs temporarily
./scripts/cursor_ignore_override.sh "logs/"

# Allow access to specific file types
./scripts/cursor_ignore_override.sh "*.log"

# Restore original exclusions
./scripts/cursor_ignore_restore.sh
```

**Direct File Access:**

```bash
# Read ignored file
./scripts/access_ignored_file.sh logs/error.log read

# Prepare for editing
./scripts/access_ignored_file.sh logs/app.log edit

# Search in ignored file
./scripts/access_ignored_file.sh logs/app.log search "ERROR"
```

## Security Considerations

**NEVER Override:**

- `.env` files (credentials)
- `secrets/` directory
- `*.key`, `*.pem`, `*.crt` files
- `credentials/` directory

**Safe to Override Temporarily:**

- `logs/` directory
- `*.log` files
- `venv/` directory (for dependency analysis)
- `__pycache__/` (for debugging)

## Best Practices

1. **Always use explicit paths** when possible
2. **Restore exclusions** immediately after use
3. **Document overrides** for team awareness
4. **Test access** before making changes
5. **Use management scripts** for consistency

## Troubleshooting

**File Not Found:**

- Verify the exact path exists
- Check if file is actually ignored
- Use `ls -la` to confirm file location

**Permission Denied:**

- Check file permissions
- Verify user has read/write access
- Use `chmod` if needed (with caution)

**Security Warnings:**

- Never override security exclusions
- Use alternative approaches for sensitive files
- Document any security-related access
