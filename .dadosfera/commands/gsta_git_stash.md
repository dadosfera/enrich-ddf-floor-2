# /gsta_git_stash

<!-- COMMAND_ID: 021 -->
<!-- COMMAND_VERSION: 1.3.0 -->
<!-- COMMAND_TYPE: gs_git_stash -->

**CRITICAL: Guidance only. The AI must actively triage every stash (no laziness): inspect diffs for all stash parents, cherry-pick/merge valuable work back to main/master (or the active feature), and run tests/coverage to ensure no regressions.** Execute each step manually with `run_terminal_cmd`; no scripted batching, no force-push.

- **Why files remain changed**: This command shows documentation - it does NOT execute git operations automatically. The AI agent must run each git command separately using `run_terminal_cmd`.
- **AI execution requirement**: After displaying this guidance, the AI must execute each step one-by-one, stopping on any error and reporting results.
- **Safety first**: No automated scripts, no chaining, no force-push. Each command must be reviewed individually.
- **ITERATIVE PROCESSING REQUIRED**: Process **ONE stash at a time** in each iteration. Complete the full inspection → decision → action cycle for `stash@{0}` before moving to `stash@{1}`. After each drop, re-run `git stash list` to verify the new stash indices before proceeding to the next stash.

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

**CRITICAL: Process ONE stash at a time. Start with `stash@{0}`, complete the full cycle, then move to the next.**

For **each stash** `stash@{n}` (beginning with `stash@{0}`), execute this inspection sequence:

#### Step 2.1: Initial Stash Summary

```bash
# Get summary statistics for the stash
gtimeout 15 git stash show --stat stash@{n}
```

**AI Decision Point**: Review the stat output. Note which files are modified and the scope of changes.

#### Step 2.2: Inspect All Three Parents

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

#### Step 2.3: Per-File Comparison Against Working Tree

**MANDATORY**: For each file listed in the stash, compare it against the current working tree to determine if the stash content is unique or redundant.

```bash
# For each file in the stash, compare against working tree
# Replace <file_path> with actual file paths from Step 2.1
gtimeout 15 git diff stash@{n} -- <file_path>
```

**AI Decision Rule**:

- If the diff shows the stash content is **identical** to the current working tree → stash is **redundant**
- If the diff shows the stash content is **older** than current working changes → stash is **redundant**
- If the diff shows **unique/newer content** in the stash → stash contains **valuable work** → proceed to cherry-pick specific files

**Special Case: Lint-Staged Automatic Backups**

- If stash message contains "lint-staged" or "automatic backup", these are **usually redundant** once the working tree is stable
- **Still verify via diff**: Run `git diff stash@{n} -- <file_path>` to confirm before dropping
- If working tree is clean and stable, these can typically be dropped after verification

**Environment/Ports Evaluation**:

- If stash changes touch environment variables, ports, or configuration files, evaluate against the current strict environment policy
- If code enforces strict env (no fallback defaults), tests may seed env vars differently
- Do not assume fallbacks exist; verify that stash changes are compatible with current strict env requirements

### 3. Decision Rules & Triage Actions

**CRITICAL: Make explicit decisions based on diff analysis. No "likely" or "should" language—decide via diffs.**

#### Step 3.1: Pre-Action Check

```bash
# Ensure working directory is clean before branching or applying
gtimeout 10 git status --porcelain
# If output not empty:
# gtimeout 10 git stash push -m "WIP during triage"
```

#### Step 3.2: Explicit Decision Rules

Based on the diff analysis from Step 2.3, apply these decision rules:

**Rule 1: Redundant Stash (Identical to Working Tree)**

- **Condition**: `git diff stash@{n} -- <file>` shows no differences OR stash content is identical to current working tree
- **Action**: Mark stash as redundant → proceed to **Option C: Drop**

**Rule 2: Redundant Stash (Older Than Current Changes)**

- **Condition**: `git diff stash@{n} -- <file>` shows stash content is older/superseded by current working changes
- **Action**: Mark stash as redundant → proceed to **Option C: Drop**

**Rule 3: Valuable Work (Unique/Newer Content)**

- **Condition**: `git diff stash@{n} -- <file>` shows unique or newer content not present in working tree
- **Action**: Identify specific files to recover → proceed to **Option B: Selective Cherry-Pick** → then **Option C: Drop**

#### Step 3.3: Triage Actions

**Option A: Convert to Branch (Recommended for valuable work with multiple files)**

```bash
# Determine branch name
STASH_BRANCH_NAME="stash/$(date +%Y%m%d)/<short-context>"
# AI: Replace <short-context> with actual context from stash message
```

```bash
# Check if branch already exists locally or remotely
gtimeout 10 git show-ref --verify --quiet refs/heads/"$STASH_BRANCH_NAME" && echo "local_exists" || echo "local_not_found"
```

```bash
gtimeout 10 git show-ref --verify --quiet refs/remotes/origin/"$STASH_BRANCH_NAME" && echo "remote_exists" || echo "remote_not_found"
```

```bash
# If branch exists, append timestamp to make it unique
if gtimeout 10 git show-ref --verify --quiet refs/heads/"$STASH_BRANCH_NAME" 2>/dev/null || \
   gtimeout 10 git show-ref --verify --quiet refs/remotes/origin/"$STASH_BRANCH_NAME" 2>/dev/null; then
  STASH_BRANCH_NAME="stash/$(date +%Y%m%d_%H%M%S)/<short-context>"
  echo "Branch exists, using unique name: $STASH_BRANCH_NAME"
fi
```

```bash
# Create branch from stash
gtimeout 10 git stash branch "$STASH_BRANCH_NAME" stash@{n}
```

**Option B: Selective Cherry-Pick (PREFERRED for targeted file recovery)**

**CRITICAL**: Do not apply or drop the stash until uniqueness is confirmed via diffs (Step 2.3).

```bash
# Restore specific file from stash (PREFERRED METHOD)
# Replace <file_path> with actual file paths identified in Step 2.3
gtimeout 15 git checkout stash@{n} -- <file_path>
```

**Alternative for single file extraction**:

```bash
# Extract single file content (use only if checkout fails)
gtimeout 15 git show stash@{n}:<file_path> > <file_path>
```

**After cherry-picking**:

1. Verify the recovered files are correct
2. Check for conflicts or issues
3. Proceed to **Option C: Drop** the stash

**Option C: Drop (Only after review and confirmation)**

**MANDATORY**: Only drop after:

- Diff analysis confirms redundancy (Rule 1 or Rule 2), OR
- Valuable files have been cherry-picked (Rule 3) and verified

```bash
# Drop the stash
gtimeout 5 git stash drop stash@{n}
```

**After dropping**:

```bash
# Re-run stash list to verify new indices
gtimeout 10 git stash list
```

**IMPORTANT**: The stash indices will shift after each drop. The previous `stash@{1}` becomes `stash@{0}`. Always re-list after each drop before proceeding to the next stash.

#### Step 3.4: Logging Decision

**Brief logging note** (for future reference):

- Which stash was dropped: `stash@{n}` (original index)
- Why it was dropped: "redundant - identical to working tree" OR "redundant - older than current changes" OR "valuable work cherry-picked, then dropped"
- Files recovered (if any): List specific file paths

### 4. Post-Action Verification (After Each Stash Decision)

**MANDATORY**: After each stash decision (drop, cherry-pick, or branch creation), verify the tree state:

```bash
# Verify working tree state after stash operations
gtimeout 10 git status --short
```

**AI Decision Point**:

- If a new stash was created (WIP during triage), re-run `git stash list` and ensure it's intentional
- Verify that cherry-picked files are present and correct
- Check for any unexpected changes or conflicts

### 5. Resolution & Validation (main/master focus)

If you created a branch or recovered files:

1. **Cherry-pick/Merge to main/master (or the active feature branch)**: Bring valuable changes back, resolve conflicts consciously.
2. **Run tests/coverage to avoid regressions** (pick the repo’s standard entrypoint; examples):
   ```bash
   # Examples (choose what the repo uses)
   gtimeout 120 bash tests/run_tests.sh --all
   # or
   gtimeout 120 bash workflows/run.sh --tests
   ```
   - Fail on any coverage drop or new failures; fix before continuing.
   - **Safety Constraint**: If tests or environment depend on specific files, do not drop stashes until tests pass and environment is confirmed stable.
3. **Cleanup**: Delete temporary stash branches after merge; re-check `git status`.

### 6. Safety Constraints

**ABSOLUTE PROHIBITIONS**:

- ❌ **NEVER** chain git commands with `&&` operators
- ❌ **NEVER** use destructive git commands: `git reset --hard`, `git clean -fd`
- ❌ **NEVER** skip diff analysis before dropping stashes
- ❌ **NEVER** process multiple stashes in parallel—one at a time only

**MANDATORY REQUIREMENTS**:

- ✅ **ALWAYS** use timeouts for all git commands (already enforced in examples)
- ✅ **ALWAYS** re-run `git stash list` after each drop to verify new indices
- ✅ **ALWAYS** run `git status --short` after each stash decision
- ✅ **ALWAYS** verify diff uniqueness before cherry-picking or dropping

### 7. Final Validation

```bash
# Verify final state
gtimeout 10 git stash list
```

```bash
# Verify working tree is clean
gtimeout 10 git status --short
```

**Success Criteria**:

- Stash count ≤ 10, none older than 14 days.
- Valuable work cherry-picked/merged back to main/master or feature branch.
- Tests/coverage unchanged or improved; no new failures.
- Working tree state verified and clean.

## Order of Operations Summary

**CRITICAL: Follow this exact sequence for EACH stash, one at a time:**

1. **List**: `git stash list` (get current stash indices)
2. **Show Stat**: `git stash show --stat stash@{N}` (get summary for current stash)
3. **Inspect Parents**: `git show stash@{N}`, `git show stash@{N}^2`, `git show stash@{N}^3` (inspect all three parents)
4. **Per-File Diff**: `git diff stash@{N} -- <file_path>` (compare each file against working tree)
5. **Decide**: Apply decision rules (redundant vs. valuable work)
6. **Action**: Cherry-pick specific files (if valuable) OR drop (if redundant)
7. **Re-List**: `git stash list` (verify new indices after drop)
8. **Verify**: `git status --short` (verify tree state)
9. **Repeat**: Move to next stash (now at new index) and repeat from step 2

**Iteration Pattern**: Complete steps 1-8 for `stash@{0}`, then move to the new `stash@{0}` (previously `stash@{1}`) and repeat. Do not batch process multiple stashes.

---

**Source**: `mini_prompt/lv1/git_stash_management_mini_prompt.md`
**Version History**:

- 1.3.0: Added branch existence checks before creating stash branches to prevent conflicts
- 1.2.0: Added explicit inspection workflow, decision rules, iterative processing requirements, safety constraints, and post-action verification
- 1.1.0: Added active triage requirements and test/coverage validation
- 1.0.0: Initial version
