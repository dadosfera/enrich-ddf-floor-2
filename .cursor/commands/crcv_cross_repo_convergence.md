# /crcv_cross_repo_convergence
<!-- COMMAND_ID: 005 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: cr_cross_repo_convergence -->

Cross-repository convergence workflow for fixing inconsistencies across all Dadosfera repositories. Use this when you identify a pattern that varies between repos and needs standardization.

Backlinks:
- mini_prompt/lv1/cross_repo_convergence_mini_prompt.md
- standards/run_sh_resource_monitoring_compliance.md (example standard)
- scripts-fera/repo-management/check_console_log_compliance.sh (example check script)

## When to Use

- You notice the same thing is done differently in multiple repos
- A standard exists but repos don't follow it consistently
- You want to roll out a new standard across all repos
- You need to verify compliance across the organization

## Enforcement Mechanisms

Hooks are just **one way** to reinforce a central solution. Use multiple mechanisms:

| Mechanism | Location | When Enforced | Use Case |
|-----------|----------|---------------|----------|
| **Standards** | docs-fera/standards/ | Human reference | Define canonical convention |
| **Pre-commit hooks** | scripts-fera/hooks/, _dev/hooks/ | At commit time | Block non-compliant commits |
| **Check scripts** | scripts-fera/repo_management/ | On demand | Diagnose maturity across repos |
| **Templates** | scripts-fera/templates/ | At creation time | Provide correct starting points |
| **CI/CD** | .github/workflows/, .gitlab-ci.yml | At PR/push | Enforce in automation |

**Choose mechanisms based on enforcement timing:**
- **Preventive**: Hooks, templates (stop issues before they happen)
- **Detective**: Check scripts, CI/CD (find issues after they happen)
- **Corrective**: Convergence workflow (fix existing issues)

### Index Naming & Content Example

The index file standardization demonstrates a complete convergence:

**Standard**: `docs-fera/standards/naming/naming_convention.md`

**Hooks** (preventive):
- `scripts-fera/hooks/source/quality/validate_index_naming.py` - Enforces naming pattern
- `scripts-fera/hooks/source/quality/validate_index_content.py` - Enforces content structure

**Check Script** (detective):
- `scripts-fera/repo_management/check_index_naming_compliance.sh` - Audits all repos

**Results**: docs-fera and scripts-fera at Level 3 (Exemplary)

## Central Plan Management

**All cross-repo convergence plans live in docs-fera** (or another central -fera repo). The central plan:
- Tracks overall convergence progress across all repos
- Defines the canonical standard to converge toward
- Contains maturity assessment results
- Documents collective learnings from all repos

```bash
# Central plan location (always in docs-fera)
cat _dev/docs/plans/active/QW_{effort}_{priority}_converge_{topic}.md
```

## Execution Strategies

Choose one of two strategies for executing the convergence:

### Strategy A: Central Agent Execution

The agent from docs-fera (or central -fera repo) directly executes updates in each target repo:

- **Pros**: Single agent maintains context, faster execution, consistent implementation
- **Cons**: Requires agent to switch repos, may miss repo-specific nuances
- **Best for**: Simple, mechanical changes (e.g., adding a config file, updating a script)

```bash
# Agent switches to target repo and executes
cd ~/local_repos/{target_repo}
# ... make changes ...
git sync
cd ~/local_repos/docs-fera
# ... update central plan progress ...
```

### Strategy B: Distributed Plan Creation

The central agent creates `/active` plans in each target repo for the local agent to execute:

- **Pros**: Local agent knows repo context, parallel execution possible, respects repo ownership
- **Cons**: Slower, requires coordination, may diverge from standard
- **Best for**: Complex changes requiring repo-specific knowledge

```bash
# For -fera repos: create plan in _dev/docs/plans/active/
# For non-fera repos: create plan in docs/plans/active/

# Example: create plan in target repo
TARGET_REPO="data-app-assistenteddf"
REPO_NAME=$(basename "$TARGET_REPO")
[[ "$REPO_NAME" == *-fera ]] && PLANS_BASE="_dev/docs/plans" || PLANS_BASE="docs/plans"

# Create the plan file in target repo
cat > ~/local_repos/$TARGET_REPO/$PLANS_BASE/active/QW_1h_HIGH_converge_{topic}.md << 'EOF'
# Convergence Plan: {topic}

## Context
This plan was created by the cross-repo convergence workflow from docs-fera.
Central plan: `docs-fera/_dev/docs/plans/active/QW_{effort}_{priority}_converge_{topic}.md`

## Tasks
- [ ] Implement {topic} following the standard
- [ ] Run tests
- [ ] Commit with: `fix({topic}): converge to standard`

## Standard Reference
See: `docs-fera/standards/{topic}_standard.md`
EOF
```

## Execution Steps (run in order)

### Phase 1: Discovery & Analysis

1) Identify the topic to converge
```
# Examples:
# - Console logging format
# - Folder structure
# - Test framework setup
# - Configuration management
# - Error handling patterns
```

2) Check if standard exists in docs-fera
```bash
gtimeout 5 ls -la standards/ | head -30
```

3) If no standard exists, create one
```bash
# Use template
gtimeout 5 cat standards/_template.md
```
```bash
# Create new standard
gtimeout 5 touch standards/{topic}_standard.md
```

4) Check if enforcement mechanisms exist
```bash
# Check for compliance check script
gtimeout 5 ls -la scripts-fera/repo_management/ | grep -i {topic}

# Check for pre-commit hook
gtimeout 5 ls -la scripts-fera/hooks/source/quality/ | grep -i {topic}

# Check for template
gtimeout 5 ls -la scripts-fera/templates/ | grep -i {topic}
```

5) Create missing enforcement mechanisms based on patterns
```bash
# Check script pattern
gtimeout 5 cat scripts-fera/repo_management/check_folder_structure.sh

# Hook pattern
gtimeout 5 cat scripts-fera/hooks/source/quality/validate_indexes.py
```

### Phase 2: Maturity Assessment & Collective Learning

6) Run compliance check across ALL local repos
```bash
gtimeout 60 bash scripts-fera/repo-management/check_{topic}_compliance.sh
```

7) Create maturity assessment with levels
```bash
# Save baseline with maturity levels to analysis/
gtimeout 5 mkdir -p analysis
```

Maturity levels:
- **Level 0 - Non-compliant**: Does not implement the pattern
- **Level 1 - Partial**: Implements some aspects, missing key elements
- **Level 2 - Compliant**: Meets the standard requirements
- **Level 3 - Exemplary**: Exceeds standard, has innovations worth adopting

```bash
# Generate maturity assessment
gtimeout 30 bash scripts-fera/repo-management/check_{topic}_compliance.sh --json > analysis/{topic}_maturity_$(date +%Y-%m-%d).json
```

8) Analyze Level 3 repos for collective learning
```bash
# Extract best practices from exemplary repos
# Look for patterns that should be incorporated into the canonical standard
```

Document findings in the analysis:
- What are Level 3 repos doing that others aren't?
- Are there innovations worth adopting organization-wide?
- Should the standard be updated based on these learnings?

9) Update canonical standard with collective learnings
```bash
# If Level 3 repos have better approaches, update the standard
# This ensures the standard evolves based on real-world implementations
```

### Phase 3: Planning

10) Create or update central plan in docs-fera
```bash
# Central plan always lives in docs-fera/_dev/docs/plans/active/
gtimeout 5 ls _dev/docs/plans/active/ | grep -i {topic}
```

```bash
# Plan should include:
# - Maturity assessment summary
# - List of repos by level
# - Execution strategy (A or B)
# - Target state for each repo
# - Collective learnings incorporated
```

11) Choose execution strategy
- **Strategy A**: Central agent will execute directly
- **Strategy B**: Create distributed plans in target repos

### Phase 4: Execution

12) Execute based on chosen strategy

**If Strategy A (Central Execution):**
```bash
# Fix repos one by one, starting with Level 0
# For each repo:
cd ~/local_repos/{target_repo}
# ... implement changes following standard ...
# Run tests
# Commit: fix({topic}): converge to standard
git sync
cd ~/local_repos/docs-fera
# Update central plan progress
```

**If Strategy B (Distributed Plans):**
```bash
# Create plans in each target repo
# For -fera repos: _dev/docs/plans/active/
# For non-fera repos: docs/plans/active/

# Then wait for local agents to execute
# Monitor progress via compliance check
```

13) Re-run compliance check after each repo
```bash
gtimeout 60 bash scripts-fera/repo-management/check_{topic}_compliance.sh
```

### Phase 5: Verification & Documentation

14) Final verification
```bash
gtimeout 60 bash scripts-fera/repo-management/check_{topic}_compliance.sh
```

15) Update documentation
- Update compliance status in standard
- Move central plan to `_dev/docs/plans/finished/`
- Create summary in `analysis/{topic}_convergence_summary_$(date +%Y-%m-%d).md`
- Document any exceptions and their justifications

## Example: Console Logging Convergence

```bash
# 1. Run maturity assessment
gtimeout 60 bash scripts-fera/repo-management/check_console_log_compliance.sh

# 2. Analyze results - identify Level 3 repos
# Example output:
# Level 3: scripts-fera (has color support, log levels, timestamps)
# Level 2: prompts-fera (meets standard)
# Level 1: data-app-assistenteddf (partial implementation)
# Level 0: ml-models-fera (no logging functions)

# 3. Extract learnings from Level 3 repos
# scripts-fera has: color_echo(), log_info(), log_error(), log_debug()
# Consider adding these to the canonical standard

# 4. Update standard with collective learnings
# Add color support and log levels to standards/console_logging_standard.md

# 5. Choose strategy and execute
# Strategy A for simple repos, Strategy B for complex ones

# 6. Track progress in central plan
cat _dev/docs/plans/active/QW_4h_HIGH_converge_console_log_standards.md
```

## Guard Rails

- **One repo at a time**: Never mass-edit multiple repos simultaneously
- **Tests must pass**: Run full test suite after each fix
- **Conventional commits**: Use `fix({topic}): converge to standard` format
- **Document exceptions**: Some repos may have valid reasons to differ
- **Update standard**: When Level 3 repos have better approaches, update the canonical standard
- **Respect repo ownership**: Strategy B is preferred when repo has active maintainers

## Notes

- Central plan always lives in docs-fera (or designated central -fera repo)
- Maturity assessment enables prioritization (fix Level 0 first)
- Collective learning ensures standards evolve based on real implementations
- Strategy B respects distributed ownership while maintaining convergence
- Use JSON output from check scripts for programmatic processing

## Related

- Mini Prompt: `mini_prompt/lv1/cross_repo_convergence_mini_prompt.md`
- Example Check Script: `scripts-fera/repo_management/check_console_log_compliance.sh`
- Example Hook: `scripts-fera/hooks/source/quality/validate_indexes.py`
- Example Standard: `standards/run_sh_resource_monitoring_compliance.md`
- Central Plans: `_dev/docs/plans/active/` (always in docs-fera for cross-repo work)
