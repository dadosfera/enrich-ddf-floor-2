# /dtao_deep_test_analyze_optimize – Deep Test Analyze & Optimize (Zero-Trust, Single-File)

<!-- COMMAND_ID: 055 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: dt_deep_test_analyze_optimize -->

Perform a **deep, zero-trust analysis** of a single test file against the actual codebase, then optimize the file to achieve **100% pass rate with zero skipped tests**.

This command treats tests with healthy skepticism: tests may be wrong, outdated, obsolete, or testing removed/changed functionality. The goal is to align tests with the **actual current behavior** of the codebase, not blindly "fix tests to pass."

**Use this command when:**

- Tests are failing and you don't know if the test or the code is wrong
- You want to deeply understand what a test file is actually testing
- You need to achieve 100% pass rate on a specific test file
- You suspect tests are obsolete or misaligned with current code
- You want to eliminate skipped tests with proper resolution

**Do NOT use when:**

- You just need to run tests (use `/tall_tests_all` or `/tcon_test_conversation`)
- You're doing quick conversation-scoped testing (use `/tcon_test_conversation`)
- You want to run all tests at once (this is single-file focused)

Backlinks:

- mini_prompt/lv1/test_improvement_mini_prompt.md
- mini_prompt/lv1/test_baseline_and_criticality_mini_prompt.md
- mini_prompt/lv2/test_obsolescence_adaptation_mini_prompt.md
- mini_prompt/lv2/automated_testing_mini_prompt.md
- commands/tcon_test_conversation.md
- commands/tall_tests_all.md

---

## Zero-Trust Testing Philosophy

This command operates under the **Zero-Trust Testing Policy**:

1. **Tests are not automatically correct** – A failing test may indicate:

   - Bug in the code (test is correct, code is wrong)
   - Bug in the test (test is wrong, code is correct)
   - Outdated test (code intentionally changed, test wasn't updated)
   - Obsolete test (tests removed functionality)
   - Misaligned test (tests implementation details, not behavior)

2. **Every test must prove its value** – For each test, determine:

   - What business/functional behavior is being tested?
   - Is that behavior still expected in the current codebase?
   - Is the assertion actually correct for current code?

3. **No silent skips** – Every `skip`, `todo`, or `xtest` must be resolved:

   - Re-enable and fix the test, OR
   - Retire the test with documented rationale, OR
   - Convert to a real passing test

4. **Prefer code fixes when test is correct** – If the test correctly asserts expected behavior but code is wrong, fix the code (with verification from specs/docs/user intent).

---

## Input Parameters

```
/dtao_deep_test_analyze_optimize <test_file_path>
```

**Required:**

- `<test_file_path>` – Absolute or relative path to a single test file

**Examples:**

```
/dtao_deep_test_analyze_optimize tests/integration/test_user_auth.py
/dtao_deep_test_analyze_optimize tests/commands/test_xect_execute_plan.sh
/dtao_deep_test_analyze_optimize src/__tests__/UserService.test.ts
```

---

## Command Sequence (Run in Order)

### Phase 1: Discovery & Context Building

1. **Verify inputs and repository context**

```bash
gtimeout 5 git rev-parse --show-toplevel
```

```bash
TEST_FILE="${1:-}"
if [[ -z "$TEST_FILE" ]]; then
  echo "ERROR: Test file path required"
  echo "Usage: /dtao_deep_test_analyze_optimize <test_file_path>"
  exit 1
fi

if [[ ! -f "$TEST_FILE" ]]; then
  echo "ERROR: Test file not found: $TEST_FILE"
  exit 1
fi

# Sanity check for large files
LINE_COUNT=$(wc -l < "$TEST_FILE" | tr -d ' ')
if [[ "$LINE_COUNT" -gt 1000 ]]; then
  echo "WARNING: Large test file ($LINE_COUNT lines). Consider analyzing in chunks."
fi
```

2. **Read and analyze the test file structure**

The AI should:

- Read the entire test file
- Identify test framework (pytest, jest, vitest, bats, playwright, etc.)
- List all test cases (including skipped/todo/disabled ones)
- Note any setup/teardown, fixtures, or mocks
- Identify what modules/components are being imported/tested
- **Check for flakiness patterns** (e.g., `sleep`, `setTimeout`, `wait`, `async`)

3. **Map test subjects to actual codebase**

For each module/function/class being tested:

- Locate the actual source file in the codebase
- Read the current implementation
- Note the function signatures, types, and behavior
- Identify any recent changes (git log) that might affect tests
- **Verify production usage** to validate test assumptions:

```bash
# Search for usage of the tested component in src/ to see how it's actually used
gtimeout 10 grep -r "ComponentName" src/ | head -n 20
```

```bash
# Example: Find source files for modules under test
gtimeout 10 git log --oneline -10 -- "$(dirname "$TEST_FILE")"
```

4. **Understand the business/functional context**

Search for:

- Related documentation (README, specs, guides)
- Related mini prompts or standards
- Similar tests in adjacent files
- API contracts or interface definitions

---

### Phase 2: Deep Zero-Trust Analysis

5. **Create analysis document**

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
REPO_NAME=$(basename "$REPO_ROOT")
TEST_BASENAME=$(basename "$TEST_FILE" | sed 's/\.[^.]*$//')

if [[ "$REPO_NAME" == *-fera ]]; then
  ANALYSIS_DIR="_dev/docs/analysis/tests"
else
  ANALYSIS_DIR="docs/analysis/tests"
fi

gtimeout 5 mkdir -p "$ANALYSIS_DIR"

ANALYSIS_FILE="$ANALYSIS_DIR/$(date +%Y-%m-%d)_dtao_${TEST_BASENAME}.md"
```

6. **For EACH test case, perform zero-trust analysis**

Create a structured analysis with these sections for each test:

```markdown
# Deep Test Analysis: [Test File Name]

**Date**: [ISO timestamp]
**Test File**: [path]
**Test Framework**: [pytest/jest/vitest/bats/etc.]
**Analysis Status**: IN_PROGRESS

## Summary

| Metric           | Count |
| ---------------- | ----- |
| Total Tests      | X     |
| Passing          | X     |
| Failing          | X     |
| Skipped/Disabled | X     |
| Tests to Fix     | X     |
| Tests to Retire  | X     |
| Code to Fix      | X     |

---

## Test-by-Test Analysis

### Test 1: `test_function_name`

**Current Status**: ❌ FAILING / ✅ PASSING / ⏭️ SKIPPED

**What This Test Claims to Verify**:
[Extracted from test name, docstring, comments, or assertion semantics]

**Modules/Functions Under Test**:

- `module.function_a()` (file: path/to/source.py)
- `module.function_b()` (file: path/to/source.py)

**Current Source Code Behavior**:
[Summary of what the actual code does NOW based on reading the source]

**Zero-Trust Verdict**:

- [ ] 🟢 **TEST IS CORRECT** – Code has a bug, fix the code
- [ ] 🟡 **TEST IS OUTDATED** – Code intentionally changed, update the test
- [ ] 🔴 **TEST IS WRONG** – Test assertion was always incorrect, fix the test
- [ ] ⚫ **TEST IS OBSOLETE** – Tests removed functionality, retire the test
- [ ] 🟣 **TEST IS FLAKY** – Non-deterministic, needs hardening

**Evidence**:
[Specific code snippets, git history, documentation excerpts that support the verdict]

**Recommended Action**:

- [ ] Fix test: [specific changes]
- [ ] Fix code: [specific changes]
- [ ] Retire test: [rationale]
- [ ] Harden test: [changes for determinism]

---

### Test 2: `test_another_function`

[Same structure as above]

---

## Skipped/Disabled Tests Triage

### Skipped Test: `test_skipped_example`

**Skip Reason (if documented)**: [reason]

**Analysis**: [Why is this skipped? Is the underlying functionality still relevant?]

**Diagnosis**:

- [ ] Run test with skip removed to capture failure message:
      `pytest test_file.py -k test_skipped_example` (or equivalent)

**Resolution**:

- [ ] Re-enable and fix (functionality exists and should be tested)
- [ ] Remove skip and verify passing (skip was unnecessary)
- [ ] Retire test (functionality removed or obsolete)

---

## Implementation Changes Required

### Code Changes (if tests are correct but code is wrong)

| File   | Change        | Rationale             |
| ------ | ------------- | --------------------- |
| [path] | [description] | [why test is correct] |

### Test Changes (if tests need updating)

| Test   | Change        | Rationale                     |
| ------ | ------------- | ----------------------------- |
| [name] | [description] | [why test was wrong/outdated] |

### Test Retirements

| Test   | File   | Rationale      |
| ------ | ------ | -------------- |
| [name] | [path] | [why obsolete] |

---

## Final Checklist

- [ ] All failing tests analyzed with zero-trust methodology
- [ ] All skipped tests resolved (re-enabled or retired)
- [ ] Code fixes implemented (if tests were correct)
- [ ] Test fixes implemented (if tests were wrong/outdated)
- [ ] Obsolete tests moved to trash_git/ with rationale
- [ ] All tests now pass with zero skips
- [ ] Coverage maintained or improved

---

**Generated**: [timestamp]
**Command**: /dtao_deep_test_analyze_optimize
```

---

### Phase 3: Execute Fixes

7. **Run the test file to establish baseline**

```bash
# Detect test framework and run
TEST_EXT="${TEST_FILE##*.}"

case "$TEST_EXT" in
  py)
    gtimeout 120 python -m pytest "$TEST_FILE" -v --tb=short 2>&1 | tee /tmp/dtao_baseline.log
    ;;
  ts|js)
    # Try vitest first, then jest
    if command -v vitest &>/dev/null; then
      gtimeout 120 vitest run "$TEST_FILE" --reporter=verbose 2>&1 | tee /tmp/dtao_baseline.log
    else
      gtimeout 120 npx jest "$TEST_FILE" --verbose 2>&1 | tee /tmp/dtao_baseline.log
    fi
    ;;
  sh)
    gtimeout 120 bash "$TEST_FILE" 2>&1 | tee /tmp/dtao_baseline.log
    ;;
  *)
    echo "Unknown test framework for extension: $TEST_EXT"
    ;;
esac
```

8. **Apply fixes based on analysis**

For each test case, based on the zero-trust verdict:

**If TEST IS CORRECT (code bug)**:

- Locate the source code
- Understand the correct expected behavior from test + docs
- Fix the code to match expected behavior
- Verify the fix doesn't break other tests

**If TEST IS OUTDATED/WRONG**:

- Update assertions to match current correct behavior
- Update test setup/mocks if interfaces changed
- Add comments explaining the update

**If TEST IS OBSOLETE**:

- Move test to `trash_git/` with timestamp
- Add entry to `tests/TEST_RETIREMENTS.md` (create if doesn't exist)
- Document rationale

**If TEST IS SKIPPED**:

- Remove skip decorator/annotation
- Fix underlying issue that caused the skip
- Or retire if obsolete

9. **Re-run tests after each fix**

```bash
# After each fix, verify progress
gtimeout 60 python -m pytest "$TEST_FILE" -v --tb=short
# or equivalent for other frameworks
```

---

### Phase 4: Verification & Completion

10. **Final verification run**

```bash
# Run with strict settings - no skips allowed
case "$TEST_EXT" in
  py)
    gtimeout 120 python -m pytest "$TEST_FILE" -v --tb=short --strict-markers -W error::pytest.PytestUnhandledCoroutineWarning 2>&1
    ;;
  ts|js)
    if command -v vitest &>/dev/null; then
      gtimeout 120 vitest run "$TEST_FILE" --reporter=verbose 2>&1
    else
      gtimeout 120 npx jest "$TEST_FILE" --verbose --bail=false 2>&1
    fi
    ;;
  sh)
    gtimeout 120 bash "$TEST_FILE" 2>&1
    ;;
esac

# If flakiness patterns were detected earlier:
# Run repeatedly to verify stability
# gtimeout 180 python -m pytest "$TEST_FILE" --count=5
```

11. **Verify 100% pass rate**

```bash
# Check for any remaining failures or skips
# The AI should verify:
# - 0 failures
# - 0 errors
# - 0 skipped (except @pytest.mark.slow or similar tagged tests)
# - All tests accounted for
```

12. **Update analysis document with results**

Complete the analysis document with:

- Final pass/fail counts
- Summary of changes made
- Any remaining issues
- Recommendations for future maintenance

13. **Commit changes**

```bash
gtimeout 10 git add "$TEST_FILE" "$ANALYSIS_FILE"

# If test retirements occurred
if [[ -d "trash_git" ]]; then
  gtimeout 5 git add trash_git/
fi

if [[ -f "tests/TEST_RETIREMENTS.md" ]]; then
  gtimeout 5 git add tests/TEST_RETIREMENTS.md
fi
```

```bash
gtimeout 5 git status --short | head -20
```

```bash
gtimeout 10 git commit -m "test(dtao): deep analysis and optimization of $(basename "$TEST_FILE")

- Analyzed with zero-trust methodology
- [X] tests fixed, [Y] tests retired, [Z] code fixes
- Achieved 100% pass rate with 0 skips"
```

---

## Decision Framework

### When to Fix Code vs Fix Test

```
┌─────────────────────────────────────────────────────────────┐
│           Zero-Trust Test Failure Decision Tree              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │ Test is failing. Why?   │
              └─────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │ Test asserts│   │ Test asserts│   │ Test asserts│
   │ CORRECT     │   │ INCORRECT   │   │ OUTDATED    │
   │ behavior    │   │ behavior    │   │ behavior    │
   └─────────────┘   └─────────────┘   └─────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │ FIX THE     │   │ FIX THE     │   │ Check: Was  │
   │ CODE        │   │ TEST        │   │ change      │
   │             │   │             │   │ intentional?│
   └─────────────┘   └─────────────┘   └─────────────┘
                                              │
                            ┌─────────────────┼─────────────────┐
                            ▼                                   ▼
                     ┌─────────────┐                     ┌─────────────┐
                     │ YES: UPDATE │                     │ NO: CODE    │
                     │ TEST to new │                     │ REGRESSION  │
                     │ behavior    │                     │ FIX THE CODE│
                     └─────────────┘                     └─────────────┘
```

### Evidence Sources for Verdicts

To determine if test or code is correct, examine:

1. **Documentation** – README, API docs, specs
2. **Git history** – When did behavior change? Was it intentional?
3. **PR/Commit messages** – Rationale for changes
4. **User-facing behavior** – What do users expect?
5. **Related tests** – Do sibling tests agree?
6. **Type definitions** – What do interfaces promise?
7. **Error messages** – What does the code say it should do?

---

## Handling Common Scenarios

### Scenario 1: Test uses deprecated API

**Symptoms**: Test calls `old_method()` which no longer exists

**Analysis**: Check if new API exists, understand migration path

**Resolution**: Update test to use new API, verify same behavior is tested

### Scenario 2: Test asserts wrong value

**Symptoms**: `assert result == 42` but correct answer is `43`

**Analysis**: Check specs, docs, related tests for correct value

**Resolution**: If 43 is correct, fix test. If 42 should be correct, fix code.

### Scenario 3: Test for removed feature

**Symptoms**: Test references `FeatureX` which was removed

**Analysis**: Confirm feature was intentionally removed (PRs, docs)

**Resolution**: Retire test to trash_git/ with documented rationale

### Scenario 4: Flaky test

**Symptoms**: Test passes/fails randomly

**Analysis**: Identify non-determinism (time, random, async, external deps)

**Resolution**: Add deterministic mocks, seeded randomness, or await conditions

### Scenario 5: Skipped test with no reason

**Symptoms**: `@pytest.mark.skip` with no comment

**Analysis**: Try running the test, understand why it was skipped

**Resolution**: Fix and re-enable, or retire with documented reason

---

## Success Criteria

The command succeeds when:

- [ ] **100% pass rate** – All tests in the file pass
- [ ] **0 skipped tests** – Every skip resolved (fixed or retired)
- [ ] **0 todo tests** – Every todo resolved (implemented or retired)
- [ ] **Analysis documented** – Full analysis file created with verdicts
- [ ] **Changes committed** – All changes tracked in git
- [ ] **Coverage maintained** – No decrease in meaningful coverage

---

## Related Commands

| Command                             | Use When                               |
| ----------------------------------- | -------------------------------------- |
| `/tcon_test_conversation`           | Quick, conversation-scoped test work   |
| `/tall_tests_all`                   | Full codebase test orchestration       |
| `/rerr_recurrent_errors`            | Diagnosing and fixing recurring issues |
| `/depi_enhanced_deep_investigation` | Deep debugging with instrumentation    |

---

## Checklist

- [ ] Test file path provided and verified
- [ ] Test framework identified
- [ ] All test cases enumerated (including skipped)
- [ ] Source code for tested modules located and read
- [ ] Each test analyzed with zero-trust methodology
- [ ] Verdicts assigned with evidence
- [ ] Fixes applied (code or test, as appropriate)
- [ ] Obsolete tests retired with rationale
- [ ] Skipped tests resolved
- [ ] Final run achieves 100% pass, 0 skips
- [ ] Analysis document completed
- [ ] Changes committed

---

**Last updated**: 2025-12-11
