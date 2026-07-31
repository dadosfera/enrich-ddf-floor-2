---
category: testing
criticality: high
scope: all
---
# /tall_tests_all
<!-- COMMAND_ID: 043 -->
<!-- COMMAND_VERSION: 2.1.0 -->
<!-- COMMAND_TYPE: ta_tests_all -->

Run the entire test surface of this repository using Moon as the primary orchestrator, progressing from smallest affected scopes to a full tests_all run. Use this for codebase-wide health checks (pre-merge, pre-release), not for individual conversation fixes.

**Critical rule**: Use /tcon_test_conversation for individual conversation fixes, not this command

**Local Reference**: `commands/tall_tests_all.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/tall_tests_all.md`

## When to Use

- Pre-merge health checks
- Pre-release validation
- Codebase-wide test verification

## When NOT to Use

- Individual conversation fixes (use /tcon_test_conversation instead)

## Related Commands

- `/tcon_test_conversation`
