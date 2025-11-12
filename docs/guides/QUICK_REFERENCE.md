# .cursorignore Management - Quick Reference

## 🚀 Quick Start

### 1. Check Current Exclusions
```bash
cat .cursorignore
```

### 2. Temporarily Allow Access
```bash
# Allow logs access
./scripts/cursor_ignore_override.sh "logs/"

# Allow specific file types
./scripts/cursor_ignore_override.sh "*.log"
```

### 3. Restore Exclusions
```bash
./scripts/cursor_ignore_restore.sh
```

### 4. Access Specific Files
```bash
# Read ignored file
./scripts/access_ignored_file.sh logs/error.log read

# Edit ignored file
./scripts/access_ignored_file.sh logs/app.log edit
```

## 🔒 Security Rules

### NEVER Override
- `.env` files
- `secrets/` directory
- `*.key`, `*.pem`, `*.crt` files

### Safe to Override
- `logs/` directory
- `*.log` files
- `venv/` (temporarily)
- `__pycache__/` (temporarily)

## 🛠️ Common Workflows

### Debugging with Logs
```bash
# 1. Allow log access
./scripts/cursor_ignore_override.sh "logs/"

# 2. Check specific log
./scripts/access_ignored_file.sh logs/app.log read

# 3. Search for errors
./scripts/access_ignored_file.sh logs/app.log search "ERROR"

# 4. Restore exclusions
./scripts/cursor_ignore_restore.sh
```

### Dependency Analysis
```bash
# 1. Allow venv access
./scripts/cursor_ignore_override.sh "venv/"

# 2. Analyze dependencies
ls venv/lib/python3.*/site-packages/

# 3. Restore exclusions
./scripts/cursor_ignore_restore.sh
```

### Model Configuration
```bash
# 1. Allow model access
./scripts/cursor_ignore_override.sh "model_cache/"

# 2. Check config
./scripts/access_ignored_file.sh model_cache/config.json read

# 3. Restore exclusions
./scripts/cursor_ignore_restore.sh
```

## 🚨 Emergency Commands

### Direct File Access
```bash
# Check if file exists
ls -la logs/

# Read file directly
cat logs/error.log

# Search in directory
find logs/ -name "*.log" | head -5
```

### AI Tool Access
```bash
# Use explicit paths with AI tools
read_file "logs/error.log"
edit_file "model_cache/config.json"
```

## 📋 File Structure

```
.cursorignore                    # Main exclusions
scripts/
├── cursor_ignore_override.sh   # Allow patterns
├── cursor_ignore_restore.sh    # Restore exclusions
└── access_ignored_file.sh      # Access files
.cursor/rules/
└── ignored_file_access_protocol.md  # AI protocols
docs/
└── cursorignore_management.md  # Full documentation
```

## ⚡ Quick Commands

| Action | Command |
|--------|---------|
| Allow logs | `./scripts/cursor_ignore_override.sh "logs/"` |
| Allow logs | `./scripts/cursor_ignore_override.sh "*.log"` |
| Allow venv | `./scripts/cursor_ignore_override.sh "venv/"` |
| Restore | `./scripts/cursor_ignore_restore.sh` |
| Read file | `./scripts/access_ignored_file.sh path/file read` |
| Edit file | `./scripts/access_ignored_file.sh path/file edit` |
| Search file | `./scripts/access_ignored_file.sh path/file search "term"` |

## 🔍 Troubleshooting

### File Not Found
```bash
# Check if file exists
ls -la path/to/file

# Check if pattern is ignored
grep "pattern" .cursorignore
```

### Permission Denied
```bash
# Check permissions
ls -la path/to/file

# Check user
whoami
```

### Security Warning
- Never override security exclusions
- Use alternative approaches for sensitive files
- Document any security-related access

---

**Remember**: Always restore exclusions after temporary access!
