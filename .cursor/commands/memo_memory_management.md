---
category: infrastructure
criticality: medium
scope: all
---
# /memo_memory_management
<!-- COMMAND_ID: 032 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: me_memory_management -->

Review and manage AI agent memories for the current workspace. This command provides analysis of all memories with suggestions for cleanup and autonomous execution capabilities.

**Local Reference**: `commands/memo_memory_management.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/memo_memory_management.md`

## When to Use

- Periodically (weekly/monthly) to maintain memory hygiene
- When AI behavior seems inconsistent with expectations
- After major codebase changes that invalidate old patterns
- When debugging unexpected AI actions
- When onboarding to understand current AI configuration

## When NOT to Use

- During active task execution (can distract from primary goal)
- When you need to create/update memories immediately (use update_memory tool directly)
- When using lower-tier models that lack memory management capabilities

## Command sequence (run in order)

### 1. List All Current Memories

The AI agent will display all memories it has access to in a structured table:

```markdown
| ID | Title | Summary | Age | Potential Issues |
|----|-------|---------|-----|------------------|
| <id> | <title> | <first 50 chars...> | <days> | <issues if any> |
```

### Healthy Memories (no action needed)

| ID | Title | Last Validated |

#### 🗑️ DELETE (clearly incorrect/obsolete)

| ID | Title | Reason |

#### 🔄 UPDATE (needs refresh)

| ID | Title | Current Issue | Suggested Update |

#### 🔀 MERGE (duplicates to consolidate)

| IDs | Titles | Merge Strategy |

#### 🗑️ DELETE

| ID | Title | Reason |

#### 🔄 UPDATE

| ID | Title | Current Issue | Suggested Update |

#### 🔀 MERGE

| IDs | Titles | Merge Strategy |

## Workflow Checklist

(Use standard status indicators. See `standards/project/task_status_standard.md`)

### For AI Agent:

- [ ] List all current memories with IDs

### For User:

- [ ] Review the analysis and recommendations
