---
category: testing
criticality: high
scope: all
---
# /tcon_test_conversation
<!-- COMMAND_ID: 042 -->
<!-- COMMAND_VERSION: 1.2.0 -->
<!-- COMMAND_TYPE: tc_test_conversation -->

Create, adapt, or retire tests only for behavior touched in this conversation. Use scope/criticality to pick a small, fast test slice first, and treat clearly obsolete tests via adaptation/retirement – do not blindly fix every red test.

**Critical rule**: Do not blindly fix every red test - focus on behavior touched in this conversation

**Local Reference**: `commands/tcon_test_conversation.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/tcon_test_conversation.md`

## When to Use

- Testing changes made in the current conversation
- Adapting tests for modified behavior
- Retiring obsolete tests

## When NOT to Use

- Codebase-wide health checks (use /tall_tests_all instead)

## Related Commands

- `/tall_tests_all`
