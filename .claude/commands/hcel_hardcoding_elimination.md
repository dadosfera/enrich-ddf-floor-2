---
category: quality
criticality: medium
scope: all
---
# /hcel_hardcoding_elimination
<!-- COMMAND_ID: 027 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: hc_hardcoding_elimination -->

Eliminate hardcoded ports, IPs, localhost references, and secrets; remove defaults and enforce fail-fast required parameters. Use the lv1 hardcoding mini prompts as the source of truth; follow their patterns and guard rails precisely.

**Local Reference**: `commands/hcel_hardcoding_elimination.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/hcel_hardcoding_elimination.md`

Backlinks:
- mini_prompt/lv1/hardcoding_ports_ips_and_secrets_elimination_mini_prompt.md
- mini_prompt/lv1/remove_defaults_hardcoding_fail_fast_mini_prompt.md

## Notes

- Follow guard rails from both lv1 mini prompts (absolute paths, timeouts, no chained commands, preserve functionality).
