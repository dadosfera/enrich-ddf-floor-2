# /memo_memory_management
<!-- COMMAND_ID: 032 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: me_memory_management -->

Review and manage AI agent memories for the current workspace. This command provides analysis of all memories with suggestions for cleanup and autonomous execution capabilities.

**Local Reference**: `commands/memo_memory_management.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/memo_memory_management.md`

## Prerequisites

⚠️ **CRITICAL**: For autonomous memory management (delete/update operations), you must use:
- **Claude Sonnet 4.5** or newer
- **GPT-5.1** or newer

Lower-tier models lack the `update_memory` tool and can only provide read-only analysis.

## Purpose

AI agents accumulate memories over time that may become:
- **Outdated**: Information no longer accurate
- **Duplicated**: Same concept stored multiple times
- **Contradictory**: Conflicting instructions
- **Stale**: References to removed files/features

This command helps identify and manage these issues.

## When to Use

- Periodically (weekly/monthly) to maintain memory hygiene
- When AI behavior seems inconsistent with expectations
- After major codebase changes that invalidate old patterns
- When debugging unexpected AI actions
- When onboarding to understand current AI configuration

## When NOT to Use

- During active task execution (can distract from primary goal)
- When you need to create/update memories immediately (use `update_memory` tool directly)
- When using lower-tier models that lack memory management capabilities

## Command Sequence

### 1. List All Current Memories

The AI agent will display all memories it has access to in a structured table:

```markdown
| ID | Title | Summary | Age | Potential Issues |
|----|-------|---------|-----|------------------|
| <id> | <title> | <first 50 chars...> | <days> | <issues if any> |
```

### 2. Identify Potential Issues

The AI agent will analyze memories for:

**Duplicates**
- Memories with similar titles or overlapping content
- Example: Multiple memories about "git sync" or "terminal commands"

**Outdated References**
- References to files/paths that no longer exist
- References to deprecated tools or patterns

**Contradictions**
- Memories that give conflicting instructions
- Example: One memory says "use docs/plans/" another says "use _dev/docs/plans/"

**Stale Information**
- Memories older than 90 days that haven't been validated
- Project-specific details that may have changed

### 3. Generate Recommendations

For each identified issue, suggest:
- **DELETE**: For clearly incorrect or duplicate memories
- **UPDATE**: For memories needing refresh with current information
- **KEEP**: For memories that are still valid and useful
- **MERGE**: For duplicate memories that should be consolidated

### 4. Output Format

```markdown
## Memory Review Summary

**Total Memories**: X
**Analyzed**: X
**Issues Found**: Y

### Healthy Memories (no action needed)
| ID | Title | Last Validated |
|----|-------|----------------|
| ... | ... | ... |

### Recommended Actions

#### 🗑️ DELETE (clearly incorrect/obsolete)
| ID | Title | Reason |
|----|-------|--------|
| <id> | <title> | <reason for deletion> |

#### 🔄 UPDATE (needs refresh)
| ID | Title | Current Issue | Suggested Update |
|----|-------|---------------|------------------|
| <id> | <title> | <issue> | <suggestion> |

#### 🔀 MERGE (duplicates to consolidate)
| IDs | Titles | Merge Strategy |
|-----|--------|----------------|
| <id1>, <id2> | <title1>, <title2> | <how to merge> |
```

### 5. User Authorization & Execution

After presenting the analysis, the AI must:

1. **Check Model Capability**: Verify if `update_memory` tool is available
2. **Present Next Steps**: Clearly outline what will be done
3. **Request Explicit Approval**: Wait for user to say **"proceed"** or similar affirmative response

**If tool is NOT available:**
```markdown
## ⚠️ Action Required

The current model does not have memory management capabilities.

**To enable autonomous memory cleanup:**
1. Switch to **Claude Sonnet 4.5** or **GPT-5.1** (or newer)
2. Re-run `/memo_memory_management`
3. Say **"proceed"** to execute the cleanup

**Alternative (Manual):**
- Open Cursor Settings > Rules for AI > Memories
- Manually delete the IDs listed above
```

**If tool IS available:**
```markdown
## 🚀 Ready to Execute

I can now autonomously delete/update the memories listed above.

**Proposed Actions:**
- Delete X redundant memories
- Update Y outdated memories
- Merge Z duplicate memories

**Say "proceed" to execute these changes.**
```

## Memory Categories

When reviewing, categorize memories into:

1. **Workflow Preferences** - How the user wants tasks executed
2. **Code Conventions** - Project-specific coding standards
3. **Tool Configuration** - Settings for specific tools
4. **Path/Location Rules** - Where files should be stored
5. **Git/Version Control** - Commit, branch, sync preferences
6. **Testing Preferences** - How tests should be run
7. **Documentation Standards** - How docs should be written

## Notes

- This command provides **analysis** and can execute **autonomous cleanup** with proper model
- The AI must request user approval before any memory changes
- Memory IDs are required for update/delete operations
- Some memories may be system-generated and should not be modified
- **Always wait for explicit "proceed" confirmation before executing changes**

## Example Analysis

```markdown
## Memory Review Summary

**Total Memories**: 15
**Analyzed**: 15
**Issues Found**: 3

### Recommended Actions

#### 🗑️ DELETE
| ID | Title | Reason |
|----|-------|--------|
| 2762408 | Git sync | Duplicate of 2762523 (identical content) |

#### 🔄 UPDATE
| ID | Title | Current Issue | Suggested Update |
|----|-------|---------------|------------------|
| 3490063 | Port Management | References old path pattern | Already updated ✅ |

#### 🔀 MERGE
| IDs | Titles | Merge Strategy |
|-----|--------|----------------|
| 4388922, 4388925 | Terminal prefs, Logging | Combine into single "Terminal & Logging Preferences" |

---

## 🚀 Ready to Execute

I can now autonomously delete/update the memories listed above.

**Proposed Actions:**
- Delete 1 redundant memory (2762408)
- Update 1 outdated memory (3490063)
- Merge 2 duplicate memories (4388922, 4388925)

**Say "proceed" to execute these changes.**
```

## Integration with Other Commands

- **`/reva_review_active_conversation`**: May identify memory-related issues during conversation analysis
- **`/proj_project`**: Project context may inform which memories are relevant
- **`/xect_execute_plan`**: Memory issues can affect plan execution

## Workflow Checklist

### For AI Agent:
- [ ] List all current memories with IDs
- [ ] Analyze for duplicates, contradictions, outdated refs
- [ ] Categorize memories by type
- [ ] Generate specific recommendations with IDs
- [ ] Check if `update_memory` tool is available
- [ ] Present clear next steps
- [ ] **Wait for user to say "proceed" before executing**
- [ ] Execute approved changes
- [ ] Confirm completion with summary

### For User:
- [ ] Review the analysis and recommendations
- [ ] **If tool unavailable**: Switch to Claude Sonnet 4.5 or GPT-5.1
- [ ] Verify proposed changes make sense
- [ ] **Say "proceed"** to authorize execution
- [ ] Review completion summary

## Future Enhancements

- Automatic memory validation against codebase
- Memory usage tracking (which memories are most referenced)
- Memory conflict resolution wizard
- Export/import memories between workspaces
- Scheduled periodic memory audits
