---
# Dadosfera Metadata
category: maintenance
criticality: high
scope: conversations
commandId: "088"
version: "1.5.0"
type: "delc_delete_conversation"
canonical: "docs-fera@/commands/delc_delete_conversation.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/delc_delete_conversation.md"
backlinks:
  - "commands/reva_review_active_conversation.md"
  - "commands/tcon_test_conversation.md"
  - "commands/arch_archive.md"

# Claude Code Metadata
name: "Delete Conversation"
description: "Safely delete AI conversation/task files with default=current-conversation behavior across Claude Code, Cursor, Cline, and Dadosfera AutoDriveDDF"
platforms:
  - cursor
  - dadosfera
  - claude
  - cline
---
<!-- COMMAND_ID: 088 -->
<!-- COMMAND_VERSION: 1.5.0 -->
<!-- COMMAND_TYPE: delc_delete_conversation -->
# /delc_delete_conversation

**Command**: `/delc_delete_conversation`

Safely delete conversation/task files across all supported AI coding platforms. **Default behavior (no arguments): deletes the current conversation** from which the command was invoked.

**Platform Support:** Claude Code, Cursor, Cline, Dadosfera AutoDriveDDF
**Storage Locations:**
- Claude Code: `~/.claude/projects/{project-name}/*.jsonl`
- Cursor: `~/.cursor/projects/{project-name}/*.jsonl`
- Cline: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/{task-id}/`
- Dadosfera AutoDriveDDF: `~/Library/Application Support/Code/User/globalStorage/dadosfera.auto-drive-code-vs-extension/tasks/{task-id}/`

**Critical rule**: Default (no arguments) = delete the current conversation/task. The agent MUST auto-detect the current conversation and confirm before deleting.

**Critical rule**: Conversations are permanently deleted without backup. Deletion is irreversible.

**Critical rule**: If the current conversation is deleted, the user MUST exit immediately to prevent the phantom conversation bug (Claude Code/Cursor only).

## When to Use

- **Most common**: User runs `/delc` with no arguments to delete the current conversation they are in
- When you need to clean up old or stale conversation files
- When a conversation is cluttering the conversation list
- When explicitly asked to delete a specific conversation by title or ID
- When asked to scan conversations for deletion intent and clean up accordingly
- When the user asks to "delete all conversations" for a project

## When NOT to Use

- When the conversation might still be needed (consider archiving instead)

## Platform Detection (Step 0)

Before any operation, detect which platform is executing this command. The platform determines storage locations, file formats, and deletion methods.

### Detection Logic

```python
# Pseudocode for platform detection
def detect_platform():
    # Method 1: Check runtime environment
    if running_in_claude_code_cli():
        return "claude-code"  # Claude Code CLI or VS Code extension
    if running_in_cursor_ide():
        return "cursor"       # Cursor IDE (fork of VS Code)
    if running_in_cline():
        return "cline"        # Cline (saoudrizwan.claude-dev) VS Code extension
    if running_in_dadosfera():
        return "dadosfera"    # AutoDriveDDF Code Extension (Cline-based)

    # Method 2: Check which storage directories exist
    if os.path.exists("~/.claude/projects/"):
        return "claude-code"
    if os.path.exists("~/.cursor/projects/"):
        return "cursor"

    # Method 3: Agent self-identification
    # The AI agent knows which platform it's running on from its system prompt
    # Claude Code agents identify as "Claude Code"
    # Cursor agents run inside Cursor IDE
    # Cline agents run inside the Cline extension
    # Dadosfera agents run inside AutoDriveDDF

    return "unknown"
```

### Platform-Specific Configuration

| Platform | Conversation Format | Storage Path | Current Detection |
|----------|-------------------|--------------|-------------------|
| **Claude Code** | `.jsonl` files | `~/.claude/projects/{project-name}/` | File mtime < 60s |
| **Cursor** | `.jsonl` files | `~/.cursor/projects/{project-name}/` | File mtime < 60s |
| **Cline** | Task directories (JSON) | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/` | Most recently modified task |
| **Dadosfera AutoDriveDDF** | Task directories (JSON) | `~/Library/Application Support/Code/User/globalStorage/dadosfera.auto-drive-code-vs-extension/tasks/` | Most recently modified task |

> **Note on Dadosfera extension ID**: The published extension ID is `dadosfera.auto-drive-code-vs-extension`. During development, the fork may still use the Cline extension ID (`saoudrizwan.claude-dev`). If neither is found, scan `globalStorage/` for directories containing "dadosfera" or "autodrive".

> **Note on Cline variants**: Some Cline forks use different extension IDs. If `saoudrizwan.claude-dev` is not found, also check for `cline.cline` or scan `globalStorage/` for directories containing "cline" or "claude-dev".

### Path Normalization (Claude Code / Cursor)

Claude Code and Cursor convert workspace paths to project directory names:
- Forward slashes (`/`) → dashes (`-`)
- Backslashes (`\`) → dashes (`-`)
- Underscores (`_`) → dashes (`-`)
- Drive letters (Windows): `C:\` → `c--`

Example: `/Users/luismartins/local_repos/case-ddf` → `-Users-luismartins-local-repos-case-ddf`

## Command Sequence (run in order)

### 1. Default Behavior: Delete Current Conversation (no arguments)

When the user runs `/delc` or `/delc_delete_conversation` with no arguments, the command **automatically targets the current conversation**.

**For Claude Code / Cursor (JSONL-based):**

```bash
# 1. Determine current project directory name
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
# Apply path normalization: replace / _ \ with -
PROJECT_NAME=$(echo "$GIT_ROOT" | sed 's|[/_\\]|-|g')

# 2. Find the current conversation file (most recently modified .jsonl)
# For Claude Code:
CONV_DIR="$HOME/.claude/projects/$PROJECT_NAME"
# For Cursor:
# CONV_DIR="$HOME/.cursor/projects/$PROJECT_NAME"

# NOTE: Use "$CONV_DIR/." to prevent dash-prefixed directory names
# from being interpreted as find flags.
# See: recurrent_errors/2026-01-30_dash_prefixed_directory_silent_find_ls_failure.md
CURRENT_FILE=$(find "$CONV_DIR/." -maxdepth 1 -type f -name "*.jsonl" \
  ! -name "*.backup" \
  ! -name "*.deleted-backup-*" \
  ! -name "history.jsonl" \
  -exec stat -f '%m %N' {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

# 3. Verify it's actively being written to (mtime < 60 seconds)
CURRENT_TIME=$(date +%s)
FILE_MTIME=$(stat -f %m "$CURRENT_FILE" 2>/dev/null || stat -c %Y "$CURRENT_FILE" 2>/dev/null)
TIME_DIFF=$((CURRENT_TIME - FILE_MTIME))

if [ $TIME_DIFF -lt 60 ]; then
  echo "Detected current conversation: $CURRENT_FILE"
fi
```

**For Cline / Dadosfera AutoDriveDDF (task-based):**

```bash
# 1. Determine globalStorage path
# For Cline:
TASKS_DIR="$HOME/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks"
# For Dadosfera AutoDriveDDF:
# TASKS_DIR="$HOME/Library/Application Support/Code/User/globalStorage/dadosfera.auto-drive-code-vs-extension/tasks"

# 2. Find the most recently modified task directory
CURRENT_TASK=$(ls -t "$TASKS_DIR" 2>/dev/null | head -1)
CURRENT_TASK_DIR="$TASKS_DIR/$CURRENT_TASK"

# 3. Verify task directory exists and has content
if [ -d "$CURRENT_TASK_DIR" ] && [ -n "$(ls -A "$CURRENT_TASK_DIR" 2>/dev/null)" ]; then
  echo "Detected current task: $CURRENT_TASK"
fi
```

> **Default flow**: Detect current → Show details → Confirm with "DELETE CURRENT" → Delete → Instruct exit

### 2. Current Conversation Detection (when targeting specific conversations)

When a specific conversation ID or pattern is provided, detect if the target happens to be the current active conversation.

```bash
# Method 1: Check file modification time (most reliable for JSONL platforms)
TARGET_FILE="/path/to/conversation.jsonl"
CURRENT_TIME=$(date +%s)
FILE_MTIME=$(stat -f %m "$TARGET_FILE" 2>/dev/null || stat -c %Y "$TARGET_FILE" 2>/dev/null)
TIME_DIFF=$((CURRENT_TIME - FILE_MTIME))

if [ $TIME_DIFF -lt 60 ]; then
  IS_CURRENT_CONVERSATION=true
else
  IS_CURRENT_CONVERSATION=false
fi

# Method 2: Cross-check with session ID (additional verification)
SESSION_ID=$(grep -m 1 '"sessionId"' "$TARGET_FILE" | grep -o '[0-9a-f-]\{36\}' | head -1)
```

> If IS_CURRENT_CONVERSATION=true: Require explicit "DELETE CURRENT" confirmation
> If IS_CURRENT_CONVERSATION=false: Proceed with normal "DELETE" confirmation

### 3. Discovery Phase (when using flags or search patterns)

Search for conversations using the platform-aware fallback directory strategy.

```bash
# 1. Enumerate all possible storage locations (platform-aware)
LOCATIONS=(
  # Claude Code
  "$HOME/.claude/projects/"
  "$HOME/.claude/projects/_archive/"
  "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/conversations/"
  "$(git rev-parse --show-toplevel 2>/dev/null)/claude-chats/"
  # Cursor
  "$HOME/.cursor/projects/"
  # Cline (VS Code)
  "$HOME/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/"
  # Dadosfera AutoDriveDDF (VS Code, Cline-based)
  "$HOME/Library/Application Support/Code/User/globalStorage/dadosfera.auto-drive-code-vs-extension/tasks/"
)

# 2. For JSONL locations (Claude Code / Cursor):
for loc in "${LOCATIONS[@]}"; do
  if [[ -d "$loc" ]] && [[ "$loc" == *"projects"* ]]; then
    find "$loc/." -type f -name "*.jsonl" \
      ! -name "*.backup" \
      ! -name "*.deleted-backup-*" \
      ! -name "history.jsonl"
  fi
done

# 3. For task-based locations (Cline / Dadosfera):
for loc in "${LOCATIONS[@]}"; do
  if [[ -d "$loc" ]] && [[ "$loc" == *"tasks"* ]]; then
    # List task directories with metadata
    for task_dir in "$loc"/*/; do
      if [ -d "$task_dir" ]; then
        TASK_ID=$(basename "$task_dir")
        # Extract task info from api_conversation_history.json or similar
        echo "$TASK_ID"
      fi
    done
  fi
done

# 4. Extract metadata from each file/task:
#    - JSONL: Parse first 10 lines for custom-title/summary/first-user-message
#    - Tasks: Parse api_conversation_history.json for task title
#    - Skip warmup summaries
#    - Extract: timestamp, size, message count
```

> Default: search current project only (for the detected platform)
> Show all conversations sorted by modification date (newest first)
> Limit display to 20 most recent

### 3.5. Intent Scan Phase (when using `--intent` or `--intent-delete`)

Scan user messages inside each discovered conversation for deletion intent. This identifies conversations where the user previously expressed a desire to delete or clean up conversations, allowing batch cleanup.

**Intent Detection Algorithm:**

```python
# Pseudocode for intent scanning
DELETION_INTENT_PATTERNS = [
    # English patterns (case-insensitive)
    r"delete\s+(this\s+)?conversation",
    r"delete\s+all\s+(the\s+)?conversations?",
    r"delete\s+all\s+(the\s+)?messages?",
    r"clean\s*up\s+(old\s+)?conversations?",
    r"remove\s+(this\s+)?conversation",
    r"clear\s+(this\s+)?conversation",
    r"get\s+rid\s+of\s+(this\s+)?conversation",
    r"wipe\s+(this\s+)?conversation",
    # Portuguese patterns (case-insensitive)
    r"apagar\s+(esta\s+)?conversa",
    r"remover\s+(esta\s+)?conversa",
    r"limpar\s+(as\s+)?conversas?",
    r"deletar\s+(esta\s+)?conversa",
    r"excluir\s+(esta\s+)?conversa",
    # Command invocation patterns
    r"/delc",
    r"delete.conversation.command",
]

# For each conversation file:
for conv_file in discovered_files:
    for line in conv_file:
        record = json.loads(line)
        if record.get("type") != "user":
            continue
        content = record.get("message", {}).get("content", [])
        for block in content:
            if block.get("type") != "text":
                continue
            text = block["text"]
            if any(re.search(p, text, re.IGNORECASE) for p in DELETION_INTENT_PATTERNS):
                mark_conversation_as_deletion_candidate(conv_file, text)
                break
```

**False Positive Reduction:**

Skip matches that appear inside:
- Tool result blocks (`type: "tool_result"`)
- System prompt or command documentation text (lines > 500 characters are likely system context)
- Quoted code blocks (text surrounded by triple backticks)
- Messages where the user is clearly discussing the delete command itself (e.g., "improve the delete conversation command") -- these are meta-discussions, not deletion requests

**Intent Scan Output:**

```
Intent scan found 3 conversations with deletion intent:

[1] "change the delete conversation command to not generate backups" (a77c0b39)
    Intent: "delete conversation" at 2026-01-30 21:35
    Size: 1020.0 KB | Messages: 45

[2] "Fix authentication bug" (abc123)
    Intent: "delete this conversation please" at 2026-01-29 14:30
    Size: 45.2 KB | Messages: 24

[3] "Deploy staging environment" (def456)
    Intent: "/delc" at 2026-01-28 09:15
    Size: 89.1 KB | Messages: 67

Excluded (current conversation): 52b04a02 - "Check all the messages..."
```

**Flags:**
- `--intent`: Scan and report conversations with deletion intent (dry-run, no deletion)
- `--intent-delete`: Scan for deletion intent AND delete matching conversations (with confirmation)

### 4. Confirmation Phase

Present the conversation details and require explicit confirmation.

**Default (no arguments) — deleting the current conversation:**

```
You are about to delete the CURRENT conversation.

Platform: Claude Code
- Title: "Improve delete conversation command"
- Conversation ID: 52b04a02 (CURRENT)
- Path: ~/.claude/projects/-Users-luismartins-local-repos-docs-fera/52b04a02.jsonl
- Modified: 2026-01-31 14:40 (Active now)
- Size: 128.5 KB
- Messages: 42

CRITICAL: This is the conversation you are currently using. After deletion:
1. The file will be permanently removed (no backup)
2. You MUST exit this conversation immediately (type 'exit' or Ctrl+C)
3. Continuing to use this conversation after deletion causes the "phantom conversation bug"

Type 'DELETE CURRENT' to confirm, or anything else to cancel.
```

**For Cline/Dadosfera (task-based, default no-args):**

```
You are about to delete the CURRENT task.

Platform: Cline
- Task ID: 1738300000000
- Path: ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/1738300000000/
- Modified: 2026-01-31 14:40 (Active now)
- Size: 256.3 KB

CRITICAL: This is the task you are currently using. After deletion:
1. The task directory will be permanently removed (no backup)
2. You MUST close this task in the Cline sidebar

Type 'DELETE CURRENT' to confirm, or anything else to cancel.
```

**Single conversation (not current, targeted by ID/pattern):**

```
Found conversation to delete:
- Title: "Fix authentication bug"
- Conversation ID: abc123
- Path: ~/.claude/projects/-case-ddf/abc123.jsonl
- Modified: 2026-01-29 14:30:00
- Size: 45.2 KB
- Messages: 24

WARNING: This will permanently delete this conversation. No backup will be created.

Type 'DELETE' to confirm, or anything else to cancel.
```

**Batch deletion (multiple conversations, e.g., `--intent-delete` or `--delete-all`):**

```
Found 25 conversations to delete for project "case-ddf":

 # | Conversation ID  | Title (first user message)           | Modified           | Size
---|------------------|--------------------------------------|--------------------|--------
 1 | 0ade29dc         | "Run the full test suite..."         | 2026-01-30 10:15   | 45.2 KB
 2 | 10623a65         | "Fix the i18n locale bug..."         | 2026-01-30 11:20   | 89.1 KB
...
25 | f81bad35         | "Analyze migration status..."        | 2026-01-30 22:00   | 32.8 KB

EXCLUDED (current conversation): 52b04a02 - "Check all the messages..."

Total: 25 conversations | 15.2 MB
WARNING: This will permanently delete ALL listed conversations. No backup will be created.
The current conversation will NOT be deleted.

Type 'DELETE ALL' to confirm batch deletion, or anything else to cancel.
```

```bash
# Ask for confirmation using AskUserQuestion tool
# Default (no-args): require "DELETE CURRENT"
# Single non-current: require "DELETE"
# Batch: require "DELETE ALL"
```

> User must type DELETE / DELETE CURRENT / DELETE ALL to confirm
> Any other input cancels the operation

### 5. Deletion

Execute deletion with platform-specific safety checks:

**For Claude Code / Cursor (JSONL-based):**

1. **Path validation**: Ensure file is in `~/.claude/projects/` or `~/.cursor/projects/` directory
2. **Existence check**: Verify file exists before deletion
3. **Delete file**: Use Bash `rm` command to remove the .jsonl file
4. **Delete subagents**: If a matching subdirectory with subagents exists, delete it too
5. **Status report**: Provide clear success/error feedback

```bash
# Validate path contains .claude/projects/ or .cursor/projects/
# Then delete
rm "{filepath}"
# If subagents directory exists:
rm -rf "{filepath%.jsonl}/subagents/"
```

**For Cline / Dadosfera AutoDriveDDF (task-based):**

1. **Path validation**: Ensure directory is inside the extension's `tasks/` directory
2. **Existence check**: Verify task directory exists
3. **Delete task directory**: Remove the entire task directory tree
4. **Status report**: Provide clear success/error feedback

```bash
# Validate path is inside globalStorage/.../tasks/
# Then delete the task directory
rm -rf "{task_dir}"
```

> No backup is created - deletion is permanent
> Subagent directories / task checkpoints are cleaned up automatically

### 6. Exit Instruction

Immediately after deletion, instruct the user based on the platform.

**If current conversation was deleted (Claude Code / Cursor):**
```
Conversation deleted permanently.

IMPORTANT: To prevent the "phantom conversation" bug, you MUST
exit this conversation now by typing 'exit' or Ctrl+C.

Continuing to use this conversation will cause it to be recreated as a phantom.
```

**If current task was deleted (Cline / Dadosfera AutoDriveDDF):**
```
Task deleted permanently.

Please close this task in the sidebar to complete cleanup.
```

**If a different conversation/task was deleted:**
```
Conversation deleted permanently.
```

```bash
# Report success
echo "Conversation/task deleted permanently."

# Platform-specific exit instructions:
# Claude Code/Cursor: "Exit this conversation now to prevent phantom bug."
# Cline/Dadosfera: "Close this task in the sidebar."
```

> CRITICAL: If current conversation was deleted on Claude Code/Cursor, user MUST exit immediately

## Conversation Discovery Strategy

The command searches multiple locations in priority order to find conversation files across all supported platforms:

### Search Order

1. **Primary: Active project conversations (Claude Code)**
   - `~/.claude/projects/{project-name}/*.jsonl`
   - All subdirectories under `~/.claude/projects/` (excluding `_archive`)

2. **Secondary: Archived conversations (Claude Code)**
   - `~/.claude/projects/_archive/{project-name}/*.jsonl`

3. **Tertiary: Project-local storage** (if configured)
   - `{git-root}/.claude/conversations/*.jsonl`
   - `{git-root}/claude-chats/*.jsonl`

4. **Cursor**
   - `~/.cursor/projects/{project-name}/*.jsonl`

5. **Cline (VS Code)**
   - macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/`
   - Linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/`
   - Windows: `%APPDATA%/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/`

6. **Dadosfera AutoDriveDDF (VS Code, Cline-based)**
   - macOS: `~/Library/Application Support/Code/User/globalStorage/dadosfera.auto-drive-code-vs-extension/tasks/`
   - Linux: `~/.config/Code/User/globalStorage/dadosfera.auto-drive-code-vs-extension/tasks/`
   - Windows: `%APPDATA%/Code/User/globalStorage/dadosfera.auto-drive-code-vs-extension/tasks/`
   - Fallback IDs: `saoudrizwan.claude-dev` (dev/fork mode), `dadosfera.autodriveddf`

7. **Cross-platform fallbacks**
   - Windows: `%USERPROFILE%\.claude\projects\`
   - WSL: Both `~/.claude/` and `/mnt/c/Users/{user}/.claude/`

### Project Name Detection

The "current project" is determined by:
1. Git repository root directory name (preferred)
2. Current working directory name (fallback)
3. User can override with `--project <name>` flag

### File Filtering

**JSONL platforms (Claude Code / Cursor):**
- **Include**: `*.jsonl` files only
- **Exclude**: `*.backup`, `*.deleted-backup-*`, `history.jsonl`
- **Title extraction**: Parse first 10 lines, prioritize custom-title > summary > first user message
- **Skip warmup**: Ignore summaries matching `/warmup|readiness|initialization|ready|assistant ready/i`

**Task platforms (Cline / Dadosfera):**
- **Include**: Task directories containing `api_conversation_history.json` or similar
- **Exclude**: `checkpoints/`, `settings/`, `cache/` directories
- **Title extraction**: Parse the first user message from the conversation history JSON

## Safety Features

- **Directory validation**: Only deletes files in known platform-specific directories
- **Current conversation detection**: Auto-detected as default target; requires "DELETE CURRENT" confirmation
- **Platform-aware path validation**: JSONL paths validated against `~/.claude/projects/` or `~/.cursor/projects/`; task paths validated against `globalStorage/.../tasks/`
- **Explicit confirmation**: User must type 'DELETE', 'DELETE CURRENT', or 'DELETE ALL' to confirm
- **Error handling**: Clear error messages for permission issues, missing files, etc.
- **Path traversal protection**: Reject paths containing `..` or absolute paths outside known directories

## Command Flags

- *(no flags)* - **Default: delete the current conversation/task** (auto-detected)
- `--all` - Search all fallback locations across all platforms
- `--archived` - Search only archived conversations (Claude Code only)
- `--project <name>` - Override project name detection
- `--platform <name>` - Force platform (`claude-code`, `cursor`, `cline`, `dadosfera`)
- `--verbose` - Show all search paths attempted and platform detection results
- `--dry-run` - Show what would be deleted without actually deleting
- `--intent` - Scan user messages for deletion intent and report matches (no deletion)
- `--intent-delete` - Scan for deletion intent AND delete matching conversations (with confirmation)
- `--delete-all` - Delete all conversations for the current project (excludes current conversation)

## Usage Examples

### Delete the current conversation (default)

```bash
User: /delc
User: /delc_delete_conversation
```

Auto-detects the current conversation/task and deletes it after "DELETE CURRENT" confirmation.

### Delete by pattern matching

```bash
User: /delc_delete_conversation test
```

Searches for conversations with "test" in the title or filename.

### Delete specific conversation

```bash
User: /delc_delete_conversation abc123
```

Finds and deletes conversation with ID `abc123.jsonl`.

### Delete by title

```bash
User: /delc_delete_conversation "Fix authentication bug"
```

Finds conversations with matching title.

### Force a specific platform

```bash
User: /delc_delete_conversation --platform cline
```

Uses Cline storage paths regardless of auto-detection.

### Scan for deletion intent (report only)

```bash
User: /delc_delete_conversation --intent
```

Scans all conversations for user messages expressing deletion intent. Reports matches without deleting.

### Scan and delete by intent

```bash
User: /delc_delete_conversation --intent-delete
```

Scans conversations for deletion intent, then deletes matching conversations after confirmation.

### Delete all conversations for current project

```bash
User: /delc_delete_conversation --delete-all
```

Lists all conversations for the current project and deletes them after "DELETE ALL" confirmation. Always excludes the current conversation.

### Search across all platforms and locations

```bash
User: /delc_delete_conversation --all
```

Searches all fallback directories across all platforms.

### Search in archived conversations only

```bash
User: /delc_delete_conversation --archived "old feature"
```

Searches only `~/.claude/projects/_archive/` tree.

### Search with project override

```bash
User: /delc_delete_conversation --project other-repo "bug fix"
```

Searches conversations for a different project than current working directory.

## Troubleshooting

### No conversations found

If the command reports no conversations found:

1. **Verify storage location exists:**
   ```bash
   ls -la ~/.claude/projects/
   ```

2. **Check for conversations manually:**
   ```bash
   # Use /. suffix to handle dash-prefixed directory names
   find ~/.claude/projects/. -name "*.jsonl" ! -name "*.backup" | head -10
   ```

3. **Verify current project detection:**
   ```bash
   basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
   ```

4. **Try --all flag to search all platforms and locations:**
   ```bash
   /delc_delete_conversation --all
   ```

5. **Check Cline/Dadosfera task storage:**
   ```bash
   ls "$HOME/Library/Application Support/Code/User/globalStorage/" | grep -iE "claude-dev|dadosfera|cline|autodrive"
   ```

### find/ls returns nothing despite conversations existing

Claude Code stores projects under directories that start with a dash (e.g., `-Users-foo-local-repos-bar`). Both `find` and `ls` silently interpret leading dashes as command flags and return zero results. Use `find "$path/." ...` or `ls -- "$path"` to fix. See `recurrent_errors/2026-01-30_dash_prefixed_directory_silent_find_ls_failure.md`.

### Cline/Dadosfera extension ID not found

If the expected globalStorage directory doesn't exist:
1. List all globalStorage extensions: `ls ~/Library/Application\ Support/Code/User/globalStorage/`
2. Look for directories containing "claude-dev", "cline", "dadosfera", or "autodrive"
3. Use `--platform` flag with the correct extension path override

### Conversations in unexpected location

If you know conversations exist but aren't found:

1. Use `--verbose` flag to see all search paths and platform detection results
2. Check platform-specific locations (WSL, Cursor, etc.)
3. Verify file permissions on storage directories

## Edge Cases & Error Handling

### File not found
```
Error: Conversation file not found.
Please verify the conversation ID or title and try again.
```

### Permission denied
```
Error: Permission denied when deleting: {path}
Check file permissions and try again.
```

### Invalid path (security check)
```
Error: Invalid path - file is outside known platform directories.
For security reasons, only files in recognized platform storage locations can be deleted.
```

### Unknown platform
```
Warning: Could not auto-detect platform. Use --platform flag to specify.
Supported: claude-code, cursor, cline, dadosfera
```

## Implementation Notes

### Tool Usage

**Recommended approach:**

1. Use `Glob` to find conversation files (JSONL platforms) or task directories (Cline/Dadosfera)
2. Use `Read` to extract metadata (title from first line or task JSON)
3. Use `Bash` for deletion
4. Provide clear text output for confirmations

### Workflow

```python
# Pseudocode workflow
1. Detect platform (Claude Code, Cursor, Cline, Dadosfera)
2. Parse user input (flags, search pattern, or conversation ID)
3. IF no arguments provided (default behavior):
   a. Auto-detect current conversation/task for the detected platform
   b. Display current conversation details
   c. Ask for "DELETE CURRENT" confirmation
   d. Delete on confirmation
   e. Instruct user to exit (platform-specific instructions)
   f. DONE
4. IF arguments provided:
   a. Glob for files in current project (respecting flags)
   b. Filter by pattern if provided
   c. Identify current conversation (mtime < 60s or matching session ID)
5. If --intent or --intent-delete:
   a. For each conversation file (excluding subagents):
      - Read line by line, parse JSON
      - For type=="user" messages, check content against DELETION_INTENT_PATTERNS
      - Skip tool_result blocks, system context, and meta-discussions
      - Record matching conversations with the matched text snippet
   b. Display intent scan results
   c. If --intent (report only): stop here
   d. If --intent-delete: proceed to confirmation with matched conversations as targets
6. If --delete-all:
   a. List all conversations for the project
   b. Exclude current conversation
   c. Proceed to confirmation with all non-current conversations as targets
7. Display targets with metadata (title, ID, modified date, size)
8. Ask for confirmation:
   - Current conversation: require "DELETE CURRENT"
   - Non-current single: require "DELETE"
   - Batch (multiple): require "DELETE ALL"
9. Validate user confirmation matches expected prompt
10. For each target:
    a. Validate path is in known platform directory
    b. JSONL: Delete .jsonl file + subagents directory
    c. Task: Delete task directory recursively
11. Report success with count
12. If current conversation was deleted:
    - Claude Code/Cursor: remind user to exit immediately
    - Cline/Dadosfera: remind user to close task in sidebar
```

## Version History

- **v1.5.0** (2026-01-31): Default=delete-current and 4-platform support
  - **Breaking**: Default behavior (no arguments) now deletes the current conversation instead of listing all
  - Added platform auto-detection: Claude Code, Cursor, Cline, Dadosfera AutoDriveDDF
  - Added Cline task storage support (`~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/`)
  - Added Dadosfera AutoDriveDDF task storage support (Cline-based, different extension ID)
  - Added `--platform` flag to force platform selection
  - Platform-specific deletion: JSONL files (Claude Code/Cursor) vs task directories (Cline/Dadosfera)
  - Platform-specific exit instructions after current conversation deletion
  - Cross-platform path validation for all 4 platforms
  - Added Cline/Dadosfera troubleshooting section

- **v1.4.0** (2026-01-30): Intent scanning and batch deletion
  - Added `--intent` flag to scan user messages for deletion intent patterns
  - Added `--intent-delete` flag to scan and delete matching conversations
  - Added `--delete-all` flag to delete all conversations for current project
  - Batch deletion confirmation with "DELETE ALL" prompt
  - Intent detection supports English and Portuguese patterns
  - False positive reduction: skips tool results, system context, and meta-discussions
  - Current conversation always excluded from batch deletion

- **v1.3.0** (2026-01-30): Cross-platform compatibility
  - Explicitly documented support for both Claude Code and Cursor
  - Command works with both `~/.claude/projects/` and `~/.cursor/projects/` storage locations
  - Unified conversation deletion across platforms
  - Ready for distribution to both `.claude/commands/` and `.cursor/commands/`

- **v1.2.0** (2026-01-30): Remove backup functionality
  - Conversations are now permanently deleted without backup
  - Simplified deletion flow (no backup creation or verification steps)
  - Removed Recovery Instructions section (no longer applicable)
  - Added subagent directory cleanup

- **v1.1.0** (2026-01-30): Current conversation detection
  - Added logic to detect if target conversation is the current active conversation
  - Different confirmation prompts: "DELETE" for other conversations, "DELETE CURRENT" for active conversation
  - Prevents accidental deletion of current conversation without clear warning
  - File modification time check (< 60 seconds = likely current)
  - Session ID extraction for additional verification

- **v1.0.0** (2026-01-30): Initial implementation
  - Safe deletion with backups
  - Phantom bug prevention instructions
  - Recovery procedures documented

## Related Commands

- `/reva_review_active_conversation`
- `/tcon_test_conversation`
- `/arch_archive`

**Local Reference**: `commands/delc_delete_conversation.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/delc_delete_conversation.md`
