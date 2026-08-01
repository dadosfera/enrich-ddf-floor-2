# Integrate Isolated Worktree — Reference

Read this when Step 0 inventory is non-trivial, merge is blocked, or you need
the full anti-loss gate list for multi-agent / multi-worktree environments.

## Plans root resolution

Canonical rule (same as `guides/collaboration/pending_to_merge_worktree.md`):

| Repo class | Plans root |
|------------|------------|
| `*-fera` (infrastructure / docs hubs) | `_dev/docs/plans` |
| Product / service / other (`*-ddf*`, etc.) | `docs/plans` |

Lifecycle folders used by this skill: `active/`, `backlog/`, `finished/`.

If both trees exist, prefer the class rule above; if only one exists, use that.
Never invent a third plans root.

## Anti-loss gates

Run before destructive git operations. Goal: minimize information loss when
several agents share one git object store via many worktrees.

### A. Identity & ownership

- [ ] Confirm you are inside **your** worktree path (`pwd` == recorded path)
- [ ] Confirm branch name matches the work being integrated
- [ ] List sibling worktrees (`git worktree list`) and label owners if known
- [ ] Never run `checkout` / `reset` / `stash -u` / `clean` in a tree you did not create

### B. Working tree inventory

- [ ] `git status --porcelain` saved to session notes
- [ ] Every dirty path classified: **this conversation** / **other agent** / **ignored tooling**
- [ ] Untracked deliverables staged intentionally (not left for `clean`)
- [ ] Secrets / credentials excluded from commits

### C. Stash & reflog safety

- [ ] `git stash list` inspected; age + message recorded
- [ ] Before any `stash drop`: patch backup under `.tmp/stash_backups/`
- [ ] Prefer `wip/<topic>-YYYYMMDD` branch over stash for overnight parking
- [ ] If work vanished: check `git reflog`, `git fsck --lost-found`, stash list before declaring loss

### D. Conversation vs other agents

- [ ] Use `/chkp_check_pending` when classification is unclear
- [ ] Other-agent items go to pending-to-merge worktree + aggregate plan
  (`guides/collaboration/pending_to_merge_worktree.md`) — not into your PR
- [ ] Do not "helpfully" rewrite another agent's uncommitted files

### E. Durability before delete

- [ ] All in-scope deliverables have commit hashes on the feature branch
- [ ] Feature branch pushed to `origin`
- [ ] PR merged (`gh pr view` → `MERGED`)
- [ ] Primary checkout `main` contains the merge commit (`merge-base --is-ancestor`)
- [ ] Finished plan + backlog (if any) present on `main` (or on the merged PR)
- [ ] Only then: `git worktree remove`

### F. Post-remove verification

- [ ] `git worktree list` no longer shows the removed path
- [ ] `git worktree prune` run
- [ ] Local feature branch deleted only after merge (optional; remote may already be gone via `gh pr merge --delete-branch`)
- [ ] No leftover `backup-pre-merge-*` tags that still hold the only copy of work

## Suggested extras beyond the main checklist

These steps are easy to skip and are the usual source of multi-agent data loss.
Treat them as mandatory when concurrency is possible:

1. **Freeze a manifest** — write `.tmp/worktree_integrate_<branch>_<UTC>.md` with
   path list, commit SHAs, stash list, sibling worktrees. Keep until Step 9 passes.
2. **Push before polish** — if the branch has unpushed commits, push early so a
   crashed agent session does not strand unique commits only on one disk.
3. **Do not reuse the primary checkout for "just a quick fix"** while siblings exist.
4. **Merge order** — if this PR depends on another open PR from a sibling worktree,
   merge the dependency first; never rebase another agent's branch without agreement.
5. **Avoid `git stash -u` as coordination** — it steals other agents' untracked files.
6. **Avoid `git clean -fd` to unblock `worktree remove`** — classify and park first.
7. **Record PR URL in the finished plan** — chat history is not durable across agents.
8. **Backlog file per deferred theme** — one rolling dump of "misc leftovers" is
   acceptable only if each item has a checkbox and origin pointer.
9. **IDE / agent session handoff** — if another agent must continue, leave
   `templates/wip_handoff.md`-style notes with hashes, not "see conversation".
10. **Primary checkout sync last** — pull `main` on the primary only after merge;
    do not reset the primary onto the feature branch while other worktrees exist.

## Merge blocked — recovery paths

| Blocker | Action |
|---------|--------|
| Required checks failing | Fix in this worktree; push; wait for checks — not `/gbyp` |
| Branch protection / reviews | Run Step 7b bypass-rights pre-check first; only then suggest authorized `/gbyp` Scenario A |
| Actor not on `bypass_pull_request_allowances` | Request review, or authorize `/gbyp` phase 4 to add actor — never assume admin ⇒ bypass |
| Org-level rulesets | Escalate to org owner; repo `/gbyp` cannot override |
| Conflicts with `main` | Merge/rebase **your** branch in **your** worktree only |
| Secrets in history | Stop; rotate; follow repo incident process — do not force-push `main` |
| Other-agent dirty files in tree | Pending-to-merge path; do not commit them into your PR |

### Bypass-rights pre-check (before suggesting `/gbyp`)

Read-only fields that matter for PR review bypass (not push restrictions):

- `enforce_admins.enabled`
- `required_pull_request_reviews.required_approving_review_count`
- `required_pull_request_reviews.require_code_owner_reviews`
- `required_pull_request_reviews.bypass_pull_request_allowances.users|teams|apps`
- Whether `gh api user` login is in that allowances list (`USER_HAS_BYPASS`)
- Org rulesets present (cannot be bypassed by repo admins)

Only after that evidence + explicit user authorization for **this PR number**,
invoke `/gbyp_git_protection_bypass` Scenario A. Prefer that command over ad-hoc
protection edits. Full command SSoT: `commands/gbyp_git_protection_bypass.md`.

Prefer `_dev/docs/plans/template/agent_branch_merge_workflow_template.md` for
enterprise merge/rollback tagging when the repo uses that template.

## Verify scope (no deploy)

Step 8 proves ancestry on `main` + local lint/test gates. **Out of scope / forbidden
in verify:** redeploy scripts, SSH cloud mutate, staging/prod pull-restart, live
environment “smoke that changes state.” Deploy is a separate user request after
verify is already green.

## Failure taxonomy (report to user)

When aborting, report with evidence:

```text
ABORT integrate-isolated-worktree
- Step failed: <N>
- Reason: <one line>
- Evidence: <command + snippet>
- Preserved: branch <name> @ <sha>, worktree <path> (NOT deleted)
- Next human/agent action: …
```

Never delete the worktree on abort.

## Related SSoT

- `guides/collaboration/multi_agent_worktree_workflow.md`
- `guides/collaboration/pending_to_merge_worktree.md`
- `guides/agent_session_closure.md`
- `templates/wip_handoff.md`
- `guides/git/branch_cleanup_policy.md`
