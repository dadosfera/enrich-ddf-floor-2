# /prop_propagate_fixes
<!-- COMMAND_ID: 038 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pr_propagate_fixes -->

End-of-session command that journals all fixes made during a long debugging/development conversation and propagates them to all deployment targets: local repo, cloud instances, container registries, and Infrastructure-as-Code.

**CRITICAL**: This command prevents the common problem of forgetting to persist fixes after a long debugging session. Run this BEFORE ending any significant conversation where cloud application fixes were made.

## Quick Checklist (TL;DR)

Before ending a debugging session, ensure:

- [ ] **Journaled** - All fixes documented in `lessons_learned/`
- [ ] **Secrets checked** - No hardcoded credentials in code
- [ ] **Templates updated** - `.env.template` matches new config vars
- [ ] **Committed** - All changes pushed to remote
- [ ] **Cloud synced** - Code/container deployed to instance
- [ ] **Migrations run** - Database schema updated (if applicable)
- [ ] **IaC updated** - Terraform/Ansible includes the fixes
- [ ] **Rollback documented** - Know how to revert if needed
- [ ] **Logs checked** - No new errors after deployment
- [ ] **Team notified** - Stakeholders know what changed

Backlinks:

- `mini_prompt/lv2/cloud_vs_local_repo_state_sync_mini_prompt.md`
- `commands/gsyn_git_sync.md`
- `commands/docu_document.md`
- `lessons_learned/` (for documenting key fixes)

## Prerequisites

- Fixes have been made during the conversation (code, config, env vars, etc.)
- Cloud instance is accessible (SSH or equivalent)
- Docker registry credentials are configured (if using containers)
- Terraform/IaC files are in scope (if updating infrastructure)

## Command Sequence (AI must execute each step individually)

### Phase 1: Journal the Fixes

**Purpose**: Create a permanent record of what was fixed and why before we forget.

1. **AI executes**: Review conversation and extract all fixes made

```bash
# Create a session journal entry with timestamp
JOURNAL_FILE="lessons_learned/$(date +%Y-%m-%d)_session_fixes_$(git rev-parse --short HEAD).md"
echo "Creating journal at: $JOURNAL_FILE"
```

2. **AI generates**: Session fixes journal with the following structure

```markdown
# Session Fixes Journal - YYYY-MM-DD

## Summary
Brief description of what application/service was being fixed.

## Environment
- Instance: (OCI instance name/IP, AWS EC2, etc.)
- Application: (app name, repo)
- Branch: (current branch)

## Fixes Applied

### Fix 1: [Short description]
- **Problem**: What was failing
- **Root Cause**: Why it was failing
- **Solution**: What change was made
- **Files Changed**: List of files
- **Verification**: How we verified the fix worked

### Fix 2: [Short description]
(repeat for each fix)

## Configuration Changes
- Environment variables added/changed
- Config files modified
- Secrets updated (reference only, not values)

## Infrastructure Changes Needed
- [ ] Terraform variables to update
- [ ] Docker image to rebuild
- [ ] Cloud config to modify
- [ ] Secrets manager updates

## Follow-up Tasks
- [ ] Update IaC to make fixes permanent
- [ ] Update documentation
- [ ] Add tests for the fix
- [ ] Notify team of changes
```

3. **AI executes**: Save the journal file

```bash
# After generating content, save to the journal file
# (AI writes the file using write tool)
```

### Phase 1.5: Config and Secrets Hygiene (CRITICAL)

**Purpose**: Ensure environment variables are propagated to templates but SECRETS are never committed.

4. **AI executes**: Check for environment variable drift

```bash
# Compare .env with .env.template (or similar)
diff <(grep -vE "^#|^$" .env | cut -d= -f1 | sort) <(grep -vE "^#|^$" .env.template | cut -d= -f1 | sort)
```

5. **AI executes**: Update templates if needed (DO NOT COMMIT REAL VALUES)

```bash
# If new variables were added to .env, add them to .env.template with placeholder values
# Example: NEW_VAR=placeholder_value
```

6. **AI executes**: Secrets Safety Check

```bash
# Scan for potential secrets before adding
grep -rE "API_KEY|PASSWORD|SECRET" . --exclude-dir={.git,node_modules,venv} | grep -vE "template|example"
```

**WARNING**: If any real secrets are found in non-ignored files, STOP and move them to `.env` or a secure secrets manager. DO NOT COMMIT SECRETS.

### Phase 2: Update Local Repository

**Purpose**: Commit all changes locally and push to remote.

7. **AI executes**: Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

8. **AI executes**: Check current status

```bash
gtimeout 5 git status --short
```

9. **AI executes**: Stage all changes

```bash
gtimeout 10 git add -A
```

10. **AI executes**: Run pre-commit hooks

```bash
gtimeout 60 pre-commit run --all-files || echo "Pre-commit had issues, review above"
```

11. **AI executes**: Re-stage if hooks modified files

```bash
gtimeout 10 git add -A
```

12. **AI executes**: Commit with descriptive message

```bash
gtimeout 10 git commit -m "fix: session fixes for [app/service name] - [brief description]"
```

13. **AI executes**: Push to remote

```bash
gtimeout 15 git push
```

### Phase 3: Sync to Cloud Instance

**Purpose**: Deploy the fixes to the running cloud instance.

**Choose the appropriate sync method based on deployment type:**

#### Option A: Direct SSH Sync (for VM-based deployments)

14. **AI executes**: SSH and pull latest code

```bash
# Replace with actual instance details
ssh user@instance-ip "cd /app/path && git pull origin main"
```

15. **AI executes**: Restart services if needed

```bash
ssh user@instance-ip "cd /app/path && docker-compose restart"
# OR
ssh user@instance-ip "sudo systemctl restart app-service"
```

#### Option B: Docker Registry Push (for containerized deployments)

14. **AI executes**: Build and tag new Docker image

```bash
gtimeout 300 docker build -t app-name:latest .
```

15. **AI executes**: Tag for registry

```bash
# OCI Registry example
docker tag app-name:latest <region>.ocir.io/<namespace>/app-name:latest
docker tag app-name:latest <region>.ocir.io/<namespace>/app-name:$(date +%Y%m%d-%H%M%S)
```

16. **AI executes**: Push to registry

```bash
gtimeout 120 docker push <region>.ocir.io/<namespace>/app-name:latest
```

17. **AI executes**: Update running instance to use new image

```bash
ssh user@instance-ip "docker pull <region>.ocir.io/<namespace>/app-name:latest && docker-compose up -d"
```

#### Option C: Kubernetes/Helm Update

14. **AI executes**: Update Helm values or kubectl apply

```bash
kubectl set image deployment/app-name app-name=<registry>/app-name:latest
# OR
helm upgrade app-name ./charts/app-name -f values.yaml
```

### Phase 4: Update Infrastructure as Code

**Purpose**: Ensure fixes are persistent across all future deployments, not just the current instance.

18. **AI executes**: Check for separate Infrastructure Repo (Multi-repo setup)

```bash
# Ask user if infrastructure code lives in a separate repo
# If yes, switch context or provide instructions for that repo
```

19. **AI executes**: Identify IaC files that need updates

```bash
# Find terraform, ansible, or other IaC files
find . -name "*.tf" -o -name "*.tfvars" -o -name "ansible*.yml" | head -20
```

20. **AI generates**: List of IaC changes needed based on session fixes

For each fix from Phase 1, determine if it requires:
- **Terraform variable updates** (environment variables, instance config)
- **User data script updates** (startup scripts, cloud-init)
- **Ansible playbook updates** (configuration management)
- **Docker Compose updates** (service configuration)
- **Kubernetes manifests updates** (deployments, configmaps)

21. **AI executes**: Update relevant IaC files

```bash
# Example: Update terraform.tfvars
# (AI uses search_replace or write tool to update IaC files)
```

22. **AI executes**: Validate IaC changes

```bash
# For Terraform
gtimeout 30 terraform validate

# For Ansible
gtimeout 10 ansible-playbook --syntax-check playbook.yml
```

23. **AI executes**: Commit IaC changes

```bash
gtimeout 10 git add -A
gtimeout 10 git commit -m "chore(infra): update IaC to include session fixes from [date]"
gtimeout 15 git push
```

### Phase 4.5: Database Migrations (if applicable)

**Purpose**: Apply any database schema or data changes made during the session.

24. **AI asks**: Were any database changes made during this session?

If YES:

25. **AI executes**: Run migrations on cloud instance

```bash
# Django
ssh user@instance-ip "cd /app/path && python manage.py migrate"

# Rails
ssh user@instance-ip "cd /app/path && rails db:migrate"

# Alembic
ssh user@instance-ip "cd /app/path && alembic upgrade head"

# Raw SQL (use with caution)
ssh user@instance-ip "psql -U user -d dbname -f migrations/YYYY-MM-DD_fix.sql"
```

26. **AI executes**: Verify migration applied

```bash
# Check migration status
ssh user@instance-ip "cd /app/path && python manage.py showmigrations | tail -10"
```

### Phase 5: Rollback Plan

**Purpose**: Document how to revert if something goes wrong.

27. **AI generates**: Rollback instructions in the journal

```markdown
## Rollback Plan

### Git Rollback
```bash
git revert <commit-hash>
git push
```

### Docker Rollback
```bash
docker pull <registry>/app-name:<previous-tag>
docker-compose up -d
```

### Database Rollback (if migrations applied)
```bash
# Command to revert migration
alembic downgrade -1
# OR restore from backup
pg_restore -d dbname backup_YYYY-MM-DD.dump
```

### Previous Working State
- Commit: <previous-commit-hash>
- Docker image: <previous-image-tag>
- Last known good: <timestamp>
```

### Phase 6: Post-Deployment Monitoring

**Purpose**: Verify no new errors were introduced.

28. **AI executes**: Check application logs for errors

```bash
# Recent logs
ssh user@instance-ip "docker logs app-container --tail 50 --since 5m" 2>&1 | grep -iE "error|exception|fail" | head -20

# Or journalctl
ssh user@instance-ip "journalctl -u app-service --since '5 minutes ago' | grep -iE 'error|exception' | head -20"
```

29. **AI executes**: Check monitoring dashboards (if available)

```bash
# Example: Check Prometheus/Grafana alerts
curl -s "http://prometheus:9090/api/v1/alerts" | jq '.data.alerts[] | select(.state=="firing")'

# Or check cloud monitoring
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --period 300 --statistics Average --start-time $(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --dimensions Name=InstanceId,Value=i-xxxxx
```

30. **AI generates**: Monitoring summary

```markdown
## Post-Deployment Health (5 min after deploy)
- [ ] No new errors in logs
- [ ] Response times normal
- [ ] Memory/CPU stable
- [ ] No alerts firing
```

### Phase 7: Final Verification

**Purpose**: Confirm success and document completion.

31. **AI executes**: Final health check

```bash
# Health check the deployed application
gtimeout 10 curl -s https://app-url/health || echo "Health check failed"
```

32. **AI generates**: Propagation summary

```markdown
## Propagation Complete

### Repository
- [x] Changes committed: <commit-hash>
- [x] Pushed to remote: origin/main

### Cloud Instance
- [x] Code synced to: <instance-name>
- [x] Services restarted: <service-list>

### Container Registry
- [x] Image pushed: <image:tag>

### Infrastructure as Code
- [x] Updated files: <file-list>
- [x] Changes validated: terraform validate passed

### Verification
- [x] Health check: PASSED
- [x] Application responding: YES
```

## Notes

- **Always run this before ending a long debugging session** - it's easy to forget steps when tired
- **Journal entries become lessons learned** - they help future debugging sessions
- **IaC updates are critical** - without them, the next deployment will lose your fixes
- **If any step fails, stop and troubleshoot** - partial propagation is dangerous

## Common Pitfalls

1. **Forgetting to update terraform.tfvars** - new env vars won't persist
2. **Not tagging Docker images** - can't rollback if needed
3. **Skipping the journal** - next week you won't remember what was fixed
4. **Not restarting services** - old code still running
5. **Missing secrets in secrets manager** - works on instance but not in IaC
6. **Forgetting database migrations** - code expects schema that doesn't exist
7. **No rollback plan** - stuck when deployment fails at 2am
8. **Not checking logs after deploy** - silent failures go unnoticed
9. **Dependency drift** - requirements.txt updated locally but not on instance
10. **Cache not invalidated** - old cached responses still being served

## Related Commands

- `/gsyn_git_sync` - Just the git sync portion
- `/docu_document` - Document fixes in README/guides
- `/rerr_recurrent_errors` - If the fix should be documented as a recurrent error
- `/jour_journey_meta_best_track` - For ongoing development workflow

---

**Last Updated**: 2025-11-29
