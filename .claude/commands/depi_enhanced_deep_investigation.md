---
category: quality
criticality: medium
scope: all
---
# /depi_enhanced_deep_investigation
<!-- COMMAND_ID: 007 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: in_enhanced_deep_investigation -->

Deep investigation with active instrumentation and debugging enhancements. This command modifies code to add comprehensive logging, debugging capabilities, and monitoring before attempting to diagnose root cause. Use when surface-level investigation isn't sufficient or when you need to understand system behavior in detail.

**Local Reference**: `commands/depi_enhanced_deep_investigation.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/depi_enhanced_deep_investigation.md`

Backlinks:
- mini_prompt/lv2/deep_debugging_instrumentation_mini_prompt.md
- commands/rciv_investigate_root_cause.md
- commands/bdbg_browser_debug.md
- commands/xect_execute_plan.md

### Instrumentation Strategy

(Use standard status indicators: `[ ]`, `[~]`, `[x]`, etc. See `standards/project/task_status_standard.md`)

#### For Frontend/UI Issues:

- [ ] Enable browser console verbose logging

#### For Backend/API Issues:

- [ ] Add request/response logging with timestamps

#### For Database Issues:

- [ ] Enable query logging with timing

#### For Integration Issues:

- [ ] Enable cross-component tracing

## Phase 6: Instrumentation Cleanup Decision

(Use standard status indicators. See `standards/project/task_status_standard.md`)

## Checklist

(Use standard status indicators. See `standards/project/task_status_standard.md`)
