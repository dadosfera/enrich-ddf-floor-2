---
# Dadosfera Metadata
category: maintenance
criticality: medium
scope: conversations
commandId: "091"
version: "1.1.0"
type: "renm_rename_conversation"
canonical: "docs-fera@/commands/renm_rename_conversation.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/renm_rename_conversation.md"
backlinks:
  - "commands/delc_delete_conversation.md"
  - "commands/cshr_conversation_session_health_report.md"
  - "commands/reva_review_active_conversation.md"
  - "commands/imco_import_conversation_chunknizing.md"
  - "guides/claude/session_health_management.md"
  - "guides/claude/claude_chats_extension_investigation.md"
  - "decisions/2026-02-01_claude_code_session_index_cache_and_operational_order.md"
  - "recurrent_errors/2026-02-01_claude_code_no_prompt_conversation_title.md"

# Claude Code Metadata
name: "Rename Conversation"
description: "Rename the current Claude Code conversation with proper title synchronization"
platforms:
  - claude
---
<!-- COMMAND_ID: 091 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: renm_rename_conversation -->
# /renm_rename_conversation

**Command**: `/renm_rename_conversation`

Rename the current Claude Code conversation using the built-in `/rename` CLI command. Automatically prompts the user to reload the window to see the updated title in the VS Code extension.

**Platform Support:** Claude Code (CLI + VS Code extension)

**How it works:**
1. Uses Claude Code's built-in `/rename` CLI command to update the conversation title
2. The CLI writes a `custom-title` message to the conversation's `.jsonl` file
3. Warns the user about VS Code extension sync lag and provides reload instructions

## Purpose

This command provides a guided workflow for renaming Claude Code conversations and ensures users know how to see the updated title in the VS Code extension.

## When to Use

- When you want to rename the current conversation to something more descriptive
- After completing a conversation and wanting to mark it as "DONE"
- When organizing conversations with prefixes like "(DONE)", "(WIP)", "(BLOCKED)"
- When the auto-generated title (first user message) is not descriptive enough

## Technical Background

### How Claude Code Stores Titles

Claude Code stores conversation titles using `custom-title` messages in the `.jsonl` file:

```json
{"type":"custom-title","customTitle":"Your New Title","sessionId":"..."}
```

The `/rename` command is a **built-in CLI command** (not a skill) that writes this message format.

### Known Issue: VS Code Extension Sync Lag

There's a known bug where the VS Code extension's conversation dropdown doesn't immediately reflect renamed titles:

- **CLI behavior**: Shows updated title immediately
- **VS Code extension behavior**: May continue showing old title until window reload
- **Root cause**: VS Code API doesn't allow extensions to programmatically update tab titles
- **Workaround**: Reload the window using Command Palette

**Reference:** [guides/claude/claude_chats_extension_investigation.md](guides/claude/claude_chats_extension_investigation.md#L120-L127)

### Why `custom-title` Is the Only Reliable Title

Claude Code derives the conversation title from the **first user message** in the JSONL file. However, several scenarios produce misleading or empty titles:

| Scenario | What happens | Title shown |
|----------|-------------|-------------|
| First message is `tool_result` | No text block to extract | "No prompt" |
| First message has system tags | Raw `<command-message>...</command-message>` leaks into title | Garbled XML |
| Conversation started via skill invocation (e.g., `/delc`, `/cshr`) | First user content is the command spec, not user text | Long spec text |
| First message is IDE selection context | `<ide_selection>` tags dominate the title | Selection context |

**`custom-title` overrides all of these.** When present, it takes priority over any auto-extracted title in both the CLI and the VS Code extension.

**Recommendation:** Rename conversations after skill invocations or any session where the first user message is not descriptive. This prevents "No prompt" entries in the session list and makes conversations easier to find.

## Command Sequence

### 1. Get the new title from the user

```bash
# Use AskUserQuestion tool to get the new conversation title
# Example prompt: "Enter the new conversation title:"
```

The user provides the new title. Common patterns:
- `(DONE) Import exported Cursor conversation`
- `(WIP) Implementing authentication feature`
- `(BLOCKED) Waiting for API key - Database migration`
- `Fix authentication bug in login flow`
- `Add dark mode toggle to settings`

### 2. Execute the built-in /rename command

The AI agent should output the `/rename` command exactly as the user would type it:

```
/rename <new_title>
```

**Example:**
```
/rename (DONE) Import exported Cursor conversation for autonomous improvement loop commands
```

**Important:** The AI agent outputs this as **text in the conversation**, not as a tool call. The `/rename` command is processed by Claude Code itself, not by the AI agent.

### 3. Confirm the rename and provide reload instructions

After the `/rename` command is executed by Claude Code, provide clear confirmation and instructions:

```markdown
✅ Conversation renamed successfully in CLI.

**New title:** <new_title>

⚠️ **Important - VS Code Extension Sync Issue:**

The VS Code extension may not immediately show the updated title in the conversation dropdown due to a known synchronization bug.

**To see the updated title in VS Code:**

1. Open Command Palette:
   - **macOS**: `Cmd + Shift + P`
   - **Windows/Linux**: `Ctrl + Shift + P`

2. Type and select: `Developer: Reload Window`

3. The conversation will reopen with the updated title

**Alternative:** Close and reopen the Claude Code tab (the title will update when the tab reopens).

---

**Technical Details:**
- The CLI has updated the conversation file with a `custom-title` message
- The VS Code extension will read this title when the window reloads or tab reopens
- This is a known limitation of the VS Code Tab API (tab titles are read-only)

**References:**
- [VS Code extension sync bug (Issue #16053)](https://github.com/anthropics/claude-code/issues/16053)
- [Claude Chats Extension Investigation](guides/claude/claude_chats_extension_investigation.md)
```

## Usage Examples

### Rename to mark as done

```bash
User: /renm_rename_conversation

Agent: Enter the new conversation title:
User: (DONE) Import exported Cursor conversation

Agent: /rename (DONE) Import exported Cursor conversation

Agent: ✅ Conversation renamed successfully in CLI.
[... provides reload instructions ...]
```

### Rename to describe work in progress

```bash
User: /renm (WIP) Implementing OAuth2 authentication

Agent: /rename (WIP) Implementing OAuth2 authentication

Agent: ✅ Conversation renamed successfully in CLI.
[... provides reload instructions ...]
```

### Rename with explicit title prompt

```bash
User: /renm_rename_conversation

Agent: Enter the new conversation title:
User: Fix memory leak in background worker

Agent: /rename Fix memory leak in background worker

Agent: ✅ Conversation renamed successfully in CLI.
[... provides reload instructions ...]
```

## Command Flags

- *(no flags)* - Prompts user for new title interactively
- Direct title argument: `/renm <title>` - Renames immediately without prompting

**Examples:**
```bash
/renm (DONE) Feature implementation
/renm_rename_conversation (BLOCKED) Waiting for API access
```

## Safety Features

- **Title validation**: Ensures title is not empty
- **Length check**: Warns if title exceeds 100 characters (recommended maximum)
- **Special character handling**: Preserves user input exactly (including emojis, parentheses, etc.)
- **Confirmation**: Shows new title before executing rename

## Constraints

### Must Do
- Use the built-in `/rename` CLI command (output as text, not a tool call)
- Provide clear reload instructions after renaming
- Explain the VS Code extension sync issue
- Show both keyboard shortcuts (macOS and Windows/Linux)

### Must Not Do
- Do not attempt to modify `.jsonl` files directly
- Do not use Bash tools to write `custom-title` messages
- Do not claim the title will update immediately in VS Code extension
- Do not skip the reload instructions

## Troubleshooting

### Title doesn't update after reload

1. **Verify the rename succeeded:**
   ```bash
   # Check the conversation file for custom-title message
   tail -50 ~/.claude/projects/{project-name}/{conversation-id}.jsonl | grep custom-title
   ```

2. **Try closing and reopening the tab** instead of reloading the window

3. **Check for multiple custom-title messages:**
   - If multiple exist, Claude Code uses the most recent one
   - This is normal and expected behavior

### "Command not found: /rename"

The `/rename` command is built into Claude Code CLI version 0.7.0+. If not available:
- Update Claude Code to the latest version
- Check CLI version: `claude --version`

### Title contains special characters that break the command

If the title contains quotes or special characters:
```bash
# Use single quotes to preserve special characters
/rename 'Title with "quotes" and $pecial characters'
```

## Implementation Notes

### Workflow

```python
# Pseudocode workflow
1. Get new title from user (via AskUserQuestion or command argument)
2. Validate title:
   - Not empty
   - Not too long (warn if > 100 chars)
3. Output the /rename command as text:
   /rename <new_title>
4. Display confirmation message with:
   - Success indicator
   - New title
   - VS Code extension sync warning
   - Reload instructions (Cmd+Shift+P / Ctrl+Shift+P)
   - Alternative (close/reopen tab)
   - Technical details
   - References
```

### Tool Usage

**Recommended approach:**

1. Use `AskUserQuestion` to get the new title (if not provided as argument)
2. Output the `/rename` command as **plain text** in the conversation
3. Provide **text output** for confirmation and instructions (no tool calls needed)

**Important:** The `/rename` command is executed by Claude Code itself, not by the AI agent. The agent only outputs the command text.

## Related Commands

- [`/delc_delete_conversation`](delc_delete_conversation.md) — Delete conversations with session health management
- [`/cshr_conversation_session_health_report`](cshr_conversation_session_health_report.md) — Read-only session health diagnostics
- [`/imco_import_conversation_chunknizing`](imco_import_conversation_chunknizing.md) — Import and organize exported conversations
- [`/reva_review_active_conversation`](reva_review_active_conversation.md) — Review conversation for archival/planning

## Related Resources

- [`session_health_management.md` guide](../guides/claude/session_health_management.md) — Session data model and firstPrompt extraction rules
- [`claude_chats_extension_investigation.md` guide](../guides/claude/claude_chats_extension_investigation.md) — `custom-title` format and VS Code extension title sync
- [DR-2026-004: sessions-index.json Is a Cache](../decisions/2026-02-01_claude_code_session_index_cache_and_operational_order.md) — Why `custom-title` is the only reliable title mechanism
- ["No prompt" recurrent error](../recurrent_errors/2026-02-01_claude_code_no_prompt_conversation_title.md) — Root causes for title extraction failures

## Version History

- **v1.1.0** (2026-02-01): Add firstPrompt caveat and rename recommendations
  - Documented why `custom-title` is the only reliable way to set a visible title
  - Added table of scenarios that produce misleading titles (tool_result, system tags, skill invocations, IDE selection)
  - Recommendation to rename after skill invocations to prevent "No prompt" entries

- **v1.0.0** (2026-01-31): Initial implementation
  - Built-in `/rename` CLI command wrapper
  - VS Code extension sync warning
  - Reload window instructions
  - Support for status prefixes: (DONE), (WIP), (BLOCKED)

## References

### Documentation
- [guides/claude/claude_chats_extension_investigation.md](guides/claude/claude_chats_extension_investigation.md) - Technical investigation of title synchronization
- [CLI reference - Claude Code Docs](https://code.claude.com/docs/en/cli-reference)

### GitHub Issues
- [Rename the conversation · Issue #7441](https://github.com/anthropics/claude-code/issues/7441)
- [VS Code extension doesn't sync conversation names after CLI /rename command · Issue #16053](https://github.com/anthropics/claude-code/issues/16053)
- [Feature Request: Allow users to set custom titles · Issue #13119](https://github.com/anthropics/claude-code/issues/13119)

---

**Local Reference**: `commands/renm_rename_conversation.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/renm_rename_conversation.md`

End Command ---
