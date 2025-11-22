# /gst-git-stash

**CRITICAL: This command displays guidance only. The AI must manually execute each step individually using terminal commands.**

- **Why files remain changed**: This command shows documentation - it does NOT execute git operations automatically. The AI agent must run each git command separately using `run_terminal_cmd`.
- **AI execution requirement**: After displaying this guidance, the AI must execute each step one-by-one, stopping on any error and reporting results.
- **Safety first**: No automated scripts, no chaining, no force-push. Each command must be reviewed individually.
- **Manual execution required**: The AI cannot create or run bash scripts for git operations.

## Required AI execution flow (AI must run these commands individually):

**AI must execute each of these commands individually using `run_terminal_cmd`:**

### 1. Inventory & Baseline Assessment

```bash
# Assess working directory and staging area
gtimeout 10 git status --porcelain
```

```bash
# List all stashes with metadata
gtimeout 10 git stash list
```

**Risk Assessment**:
- **High Risk**: Count > 10 OR oldest stash > 14 days → **MANDATORY** full triage
- **Medium Risk**: Count 5-10 OR oldest 7-14 days → Review and triage

### 2. Deep Inventory (Untracked/WIP Awareness)

For each relevant stash `stash@{n}`, inspect all three parents:

```bash
# Tracked Changes (Main Diff)
gtimeout 15 git show --name-only --pretty=fuller stash@{n}
gtimeout 30 git show -p stash@{n} | head -50
```

```bash
# Staged Changes (Index State)
gtimeout 15 git show --name-only --pretty=fuller stash@{n}^2
```

```bash
# Untracked Files (Hidden WIP!) - CRITICAL
gtimeout 15 git show --name-only --pretty=fuller stash@{n}^3
```

### 3. Triage Actions

**Pre-Action Check**:
```bash
# Ensure working directory is clean before branching or applying
gtimeout 10 git status --porcelain
# If output not empty:
# gtimeout 10 git stash push -m "WIP during triage"
```

**Option A: Convert to Branch (Recommended for valuable work)**

```bash
# Name pattern: stash/YYYYMMDD/<short-context>
# AI: Replace <short-context> with actual context
gtimeout 10 git stash branch "stash/$(date +%Y%m%d)/<short-context>" stash@{n}
```

**Option B: Selective Apply & Restore**

```bash
# Restore specific file from stash
gtimeout 15 git checkout stash@{n} -- path/to/file
# OR
gtimeout 15 git show stash@{n}:path/to/file > path/to/file
```

**Option C: Drop (Only after review)**

```bash
gtimeout 5 git stash drop stash@{n}
```

### 4. Resolution & Cleanup

If you created a branch or recovered files:

1.  **Cherry-pick/Merge**: Bring valuable changes back to main/feature branch.
2.  **Verify**: Ensure no data loss.
3.  **Cleanup**: Delete temporary stash branches if merged.

### 4. Validation

```bash
# Verify final state
gtimeout 10 git stash list
```

**Success Criteria**:
- Stash count ≤ 10
- No stashes older than 14 days
- Valuable work preserved in branches

---
**Source**: `mini_prompt/lv1/git_stash_management_mini_prompt.md`
