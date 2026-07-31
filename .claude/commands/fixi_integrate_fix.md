---
category: infrastructure
criticality: medium
scope: all
---
# /fixi_integrate_fix
<!-- COMMAND_ID: 076 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: fi_fix_integration -->

Command to properly integrate a fix file (`.fix`, `.fixed`, `fixes`, patch files, etc.) into the main codebase, ensuring the fix becomes part of the codebase, tests, deployments, and releases—not just a disconnected file that lives apart.

**Local Reference**: `commands/fixi_integrate_fix.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/fixi_integrate_fix.md`

Backlinks:
- mini_prompt/lv1/find_deprecated_fix_files_mini_prompt.md
- commands/prop_propagate_fixes.md
- commands/merg_merge.md
- commands/gsyn_git_sync.md

## When to Use

- You've found a fix file (`.fix`, `.fixed`, `fixes`, `.patch`, etc.) that needs to be integrated
- A fix exists as a separate file but should be part of the main codebase
- A patch or workaround needs to be permanently applied
- You want to ensure a fix is included in deployments and releases

## Fix File

- Path: $FIX_FILE

## Fix Content Summary

[AI analyzes and describes what the fix does]

## Target Files Identified

[List of files in main codebase that need the fix]

## Integration Strategy

[How the fix should be applied]

### Primary Target

- File: [path/to/target/file]

### Secondary Targets (if any)

- File: [path/to/other/file]

### Files That Reference the Fix

- File: [path/to/file]

## Fix File

- Original: $FIX_FILE

## Integration Complete

- ✅ Fix applied to: [list of target files]

## Next Steps

1. Review changes: `git show HEAD`
