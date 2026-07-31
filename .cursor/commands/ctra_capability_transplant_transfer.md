---
category: infrastructure
criticality: medium
scope: all
---
# /ctra_capability_transplant_transfer
<!-- COMMAND_ID: 050 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: ct_capability_transplant -->

Coordinate a **capability transplant** from a reference repo into a target repo: learn from an existing implementation (e.g., authentication layer), build inventories and boundary specs, and create a contextualized plan in the target repo using the standardized template.

**Local Reference**: `commands/ctra_capability_transplant_transfer.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/ctra_capability_transplant_transfer.md`

Backlinks:
- mini_prompt/lv2/capability_transplant_from_reference_repo_mini_prompt.md
- templates/plans/capability_transplant_plan_template.md
- commands/crcv_cross_repo_convergence.md
- architecture/feature_sliced_architecture.md
- --

## When to Use

- You have a **proven implementation** of a capability in one repo (e.g., auth, payments, file uploader, notifications) and want to **reuse it in another repo**.
- You need to **move more than just code**: tests, scripts, workflows, infra hooks, and docs must move or be re-created coherently.
- You want a **single, explicit plan file inside the target repo** that explains how the transplanted capability works in that context.
- You are doing very small, local code reuse (one or two files) with no cross-repo implications.
- You only need **organization-wide standardization** (then prefer `/crcv_cross_repo_convergence`).
