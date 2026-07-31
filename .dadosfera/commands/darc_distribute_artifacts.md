---
category: distribution
criticality: high
scope: all
---
# /darc_distribute_artifacts
<!-- COMMAND_ID: 098 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: dr_artifacts -->

Centralized entrypoint for D&ADDF distribution workflows. Run the local canonical refresh (commands JSON → markdown, collision checks, and generated command adapter refresh), then dispatch artifact installers for all configured entities. Cross-repo and global sync are explicit opt-in steps, not defaults.

**Critical rule**: Distribution is a **destructive-cleanup operation** by design for destination folders: stale files are removed from canonical destinations and replaced with distributed artifacts from docs-fera.

**Critical rule**: Run this only from an intended source repo (typically `docs-fera`) so global precedence and source-of-truth assumptions remain valid.

**Critical rule**: Cross-repo propagation (copy/commit/pr) is optional and requires explicit operator authorization. Do not run cross-repo modes by default.

**Critical rule**: Global distribution to home directories is optional and is **not** part of standard `darc_distribute_artifacts` first run.

**Local Reference**: `commands/darc_distribute_artifacts.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/darc_distribute_artifacts.md`

Backlinks:
- _dev/workflows/distribution/distribute_artifacts.sh
- _dev/workflows/command_distribution/build_commands_from_json.sh
- _dev/scripts/commands/generate_command_adapters_from_commands.py
- guides/commands/slash_command_distribution_workflow.md
- guides/distribution/distribution_workflow_unified.md

## When to Use

- After adding or changing commands, rules, skills, agents, or plugins in docs-fera
- Before requesting broad rollout to keep multiple repos and platforms in sync
- After command/source migrations when generated command adapters or platform instances may drift
- When verifying that commands, rules, and generated adapters were fully regenerated and distributed

## When NOT to Use

- For one-off local file fixes to a single repository
- When you only need repository-local `.cursor/commands/` and `.dadosfera/commands/` sync; use a local installer instead
- When cross-repo mass changes are already forbidden by policy and user instruction

## Command sequence (run in order)

### 1. Normalize canonical sources (local repo only)

```bash
python3 _dev/scripts/commands/check_command_collisions.py
bash _dev/workflows/command_distribution/build_commands_from_json.sh
python3 _dev/scripts/commands/generate_command_adapters_from_commands.py --check
```

> Always run collision check before generating distributions.
> Regenerate markdown and generated command adapters before any distribution step.

### 2. Distribute local platform command instances

```bash
bash _dev/scripts/distribution/distribute_platform_commands.sh
```

> Copies canonical markdown to `.cursor/commands/`, `.dadosfera/commands/`, and `.claude/commands/`.
> Run step 1 again first if you need to re-generate markdown from JSON.

### 3. Distribute all supported artifact families

```bash
bash _dev/workflows/distribution/distribute_artifacts.sh --type all
```

> This executes standardized installers for commands, rules, skills, agents, and plugins in one pass.

### 4. Validate distribution result

```bash
bash _dev/workflows/distribution/distribute_artifacts.sh --type all --verify
```

> Run whenever you need explicit drift verification before committing.

### 5. Optional: cross-repo command sync (no-default behavior)

Use one of these commands only when explicitly authorized and only after step 3 succeeded.

```bash
# Copy-only (safe, no git writes):
bash _dev/scripts/commands/sync_commands_cross_repo.sh --mode copy

# Specific repos only:
bash _dev/scripts/commands/sync_commands_cross_repo.sh --mode copy --repos repo1,repo2

# Commit-only across all local repos (if requested):
bash _dev/scripts/commands/sync_commands_cross_repo.sh --mode commit

# PR workflow across local repos (if requested):
bash _dev/scripts/commands/sync_commands_cross_repo.sh --mode pr
```

> Cross-repo command sync is not part of default `/darc_distribute_artifacts` behavior.
> Do not run cross-repo modes while another agent is mutating the same checkout set without explicit coordination.

### 6. Optional: global destination sync

Use only when you intentionally need global IDE-wide targets refreshed.

```bash
bash _dev/scripts/skills/distribute_skills_from_registry.sh --all

# Optional command copy for global folders (if needed by policy):
DOCS_FERA=$(git rev-parse --show-toplevel)
rsync -a --delete "$DOCS_FERA/.cursor/commands/" "$HOME/.cursor/commands/"
rsync -a --delete "$DOCS_FERA/.dadosfera/commands/" "$HOME/.dadosfera/commands/"
rsync -a --delete "$DOCS_FERA/.claude/commands/" "$HOME/.claude/commands/"
rsync -a --delete "$DOCS_FERA/.cursor/skills/" "$HOME/.cursor/skills/"
rsync -a --delete "$DOCS_FERA/.codex/skills/" "$HOME/.codex/skills/"
rsync -a --delete "$DOCS_FERA/.claude/skills/" "$HOME/.claude/skills/"
```

> Global sync has a broader blast radius and is intentionally opt-in.
> Validate `.git` state in each target repo before and after any optional global sync to avoid stale UI cache issues.

## Standard run sequence

| Phase | Commands |
| --- | --- |
| Local refresh | `python3 _dev/scripts/commands/check_command_collisions.py` 
`bash _dev/workflows/command_distribution/build_commands_from_json.sh` 
`python3 _dev/scripts/commands/generate_command_adapters_from_commands.py --check` |
| Platform rebuild | `bash _dev/scripts/distribution/distribute_platform_commands.sh` |
| Full distribution | `bash _dev/workflows/distribution/distribute_artifacts.sh --type all` |
| Verification | `bash _dev/workflows/distribution/distribute_artifacts.sh --type all --verify` |

Run the optional cross-repo/global steps only on explicit operator request.

## Related commands

- `/darc_distribute_artifacts` (this command)
- `/gsyn_git_sync`
- `/gswp_git_sweep`
- `/gsta_git_stash`
- `/gful_git_full_sync`
- `scripts-fera` distribution workflows for hooks/guards (no-op here unless explicitly integrated)


## Related documentation

- `guides/distribution/distribution_workflow_unified.md`
- `guides/commands/slash_command_distribution_workflow.md`
- `commands/README.md`
- `_dev/workflows/distribution/README.md`
- `_dev/workflows/distribution/entity_management_cli.sh`

## Related Commands

- `/gsyn_git_sync`
- `/gswp_git_sweep`
- `/gsta_git_stash`
- `/gful_git_full_sync`
- `/darc_distribute_artifacts`
