# /ctra_capability_transplant_transfer

<!-- COMMAND_ID: 050 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ct_capability_transplant -->

Coordinate a **capability transplant** from a reference repo into a target repo: learn from an existing implementation (e.g., authentication layer), build inventories and boundary specs, and create a contextualized plan in the target repo using the standardized template.

Backlinks:

- `mini_prompt/lv2/capability_transplant_from_reference_repo_mini_prompt.md`
- `_dev/docs/plans/template/capability_transplant_plan_template.md`
- `commands/crcv_cross_repo_convergence.md`
- `architecture/feature_sliced_architecture.md`

---

## When to Use

Use `/ctra_capability_transplant_transfer` when:

- You have a **proven implementation** of a capability in one repo (e.g., auth, payments, file uploader, notifications) and want to **reuse it in another repo**.
- You need to **move more than just code**: tests, scripts, workflows, infra hooks, and docs must move or be re-created coherently.
- You want a **single, explicit plan file inside the target repo** that explains how the transplanted capability works in that context.

Avoid using this command when:

- You are doing very small, local code reuse (one or two files) with no cross-repo implications.
- You only need **organization-wide standardization** (then prefer `/crcv_cross_repo_convergence`).

---

## Command sequence (run in order)

### 1) Clarify capability and repositories

With the user, capture:

- `source_repo_path` and `source_branch` (where the good implementation already lives).
- `target_repo_path` and `target_branch` (where the capability will be transplanted).
- `source_capability_slug` (e.g., `auth_layer`, `payments`, `file_uploader`).
- `target_repo_type`:
  - `fera_repo` → plans under `_dev/docs/plans/**`
  - `app_repo` → plans under `docs/plans/**`

Keep this configuration visible in the conversation (or a small YAML snippet) so it can be reused across steps.

---

### 2) Run the lv2 mini prompt for cross-repo learning

Use the specialized lv2 mini prompt to orchestrate discovery and analysis:

```text
mini_prompt/lv2/capability_transplant_from_reference_repo_mini_prompt.md
```

Ask the agent to:

- Work in **read-only mode** on the source repo.
- Produce:
  - `analysis/capabilities/{source_capability_slug}/source_inventory.md`
  - `analysis/capabilities/{source_capability_slug}/capability_boundary_spec.md`
  - `analysis/capabilities/{source_capability_slug}/target_integration_design.md` (in the target repo)
- Respect terminal safety and absolute path rules (`$HOME` vs project roots, no project-local `~/.oci`).

This step ensures that the transplant is **grounded in how the capability actually works**, not just file copying.

---

### 3) Create the capability transplant plan in the target repo

Using the docs-fera template:

```text
_dev/docs/plans/template/capability_transplant_plan_template.md
```

Guide the agent to:

1. Determine the correct plan base directory in the **target repo**:
   - `fera_repo` → `_dev/docs/plans/(active|prioritized)/`
   - `app_repo` → `docs/plans/(active|prioritized)/`
2. Copy the template into the target repo as a concrete plan, for example:
   - `QW_4h_HIGH_capability_transplant_auth_layer_from_planner_ddf.md`
3. Fill all placeholders using:
   - `source_inventory.md`
   - `capability_boundary_spec.md`
   - `target_integration_design.md`
   - Repo-specific architecture constraints (e.g., feature-sliced layout, tenancy model).

Keep this plan **small but complete**: it should tell a new maintainer how the capability is meant to work in the target repo without opening the source repo.

---

### 4) Align execution with existing commands and standards

Once the plan exists in the target repo:

- Use `/xect_execute_plan` to execute the conversation-related active plan when ready.
- Use `/expp_xpand_plan` if the generated plan is too sparse (< ~500 lines) and needs deeper detailing.
- Optionally, use `/crcv_cross_repo_convergence` if the capability transplant is part of a broader **standardization** effort across multiple repos.
- Refer to `architecture/feature_sliced_architecture.md` (or the target repo’s architecture docs) to choose the correct module layout and boundaries.

Make sure to:

- Preserve existing functionality in the target repo; avoid regressions in other features.
- Keep commits and branches **scoped to the capability transplant**, with meaningful messages.

---

### 5) Verification, rollout, and documentation

The final stage is **verification and rollout**, driven by the capability transplant plan in the target repo:

- Ensure tests (unit, integration, E2E) are enhanced to cover the transplanted capability.
- Validate CI pipelines and any new workflows introduced.
- Update or create:
  - Capability overview docs (e.g., `docs/capabilities/{slug}.md`).
  - Runbooks for operations, incident response, and debugging.
- Document intentional divergences from the source implementation in the target plan.

When the capability is stable and validated:

- Move the plan file from `active/` to `finished/` (following the repo’s plan lifecycle).
- Add cross-links in docs-fera (or central docs) if this transplant should become a reusable reference for future work.

---

## Notes

- This command is **coordination guidance**, not an auto-run script: each step should be executed explicitly by the agent, respecting repository-specific rules and safety standards.
- For sensitive capabilities (e.g., authentication, payments), ensure that **security and compliance reviews** are part of the plan before considering the transplant complete.



