# /ghst_git_history_stability

<!-- COMMAND_ID: 067 -->
<!-- COMMAND_VERSION: 1.0.0 -->

Analyze git history to identify recurrent instability patterns, "frequent flyer" files, and recurring fixes, then propose systemic solutions.

Backlinks:

- commands/cprs_commits_prs_rules_analysis.md
- commands/rerr_recurrent_errors.md
- commands/matc_code_quality_maturity_assessment.md

## Command sequence (run in order)

1. **Analyze Recurrent Issues**: Search git history for "fix", "fail", "error", or "broken" patterns.
2. **Identify Unstable Files**: Find files that appear most frequently in fix-related commits.
3. **Analyze Specific Patterns**: deeply investigate the history of the most unstable files to understand *why* they are changing.
4. **Propose Solutions**: Draft a plan to address the root causes (systemic fixes) rather than symptoms.

```bash
# 1. Overview of fix/fail activity (last 12 months)
echo "=== Fix/Fail Commit Activity ==="
git log --since="1 year ago" --grep="fix\|fail\|error\|broken" --oneline | head -n 20
echo "..."
echo "Total fix/fail commits: $(git log --since="1 year ago" --grep="fix\|fail\|error\|broken" --oneline | wc -l)"

# 2. Identify "Frequent Flyer" files (files with most fix-related churn)
echo -e "\n=== Most Frequently Fixed Files ==="
git log --since="1 year ago" --grep="fix\|fail\|error\|broken" --name-only --format="" | \
  grep -v "^$" | \
  sort | uniq -c | sort -nr | head -n 20

# 3. Analyze specific file history (replace FILENAME with top result)
# Example: git log --since="1 year ago" --patch -- "tests/unit/config/service-urls.test.ts" | grep -E "commit|Date:|fix:|fail:" | head -n 30
```

## Notes

- **Refix Pattern**: Look for files that are "fixed" repeatedly for the same issue (e.g., "fix import", "fix timeout", "fix type").
- **Churn vs. Evolution**: Distinguish between natural evolution (new features) and churn (repeated fixes). High churn in tests often indicates tight coupling or fragility.
- **Systemic vs. Symptomatic**: Use the evidence to propose systemic fixes (e.g., "standardize config loading") instead of symptomatic ones (e.g., "update timeout to 5000ms").
