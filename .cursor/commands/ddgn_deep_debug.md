---
category: quality
criticality: medium
scope: all
---
# /ddgn_deep_debug
<!-- COMMAND_ID: 006 -->
<!-- COMMAND_VERSION: 2.0.0 -->
<!-- COMMAND_TYPE: in_enhanced_deep_diag -->

Deep debugging via probes, instrumentation, and structured logging — with explicit lifecycle gating and a plan to keep code light after the incident while reusing high-value probes. Requires central debug flags and production/later-stage cleanup.

**Local Reference**: `commands/ddgn_deep_debug.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/ddgn_deep_debug.md`

Backlinks:
- commands/rcdg_root_cause_diag.md
- commands/rciv_investigate_root_cause.md
- commands/bdbg_browser_debug.md
- standards/code/debug_and_instrumentation_flags_standard.md
- standards/maturity/software_lifecycle_maturity.md

### Central debug gating (required)

All probes must be controlled by central debug flags and lifecycle gates. See `standards/code/debug_and_instrumentation_flags_standard.md`.

#### Probe plan

Add only targeted probes: request tracing, timing probes, state transitions, external call probes, error probes.

## Cleanup requirements (prd + beta/rc/ga)

Ensure production and later lifecycle stages remain clean by default; remove or gate ad-hoc probes and document keep/remove/convert decisions.

## Checklist

Confirm probes are centrally gated, safe (no secrets), evidence was captured, diagnosis is backed by logs, and cleanup is complete for production and later lifecycle stages.
