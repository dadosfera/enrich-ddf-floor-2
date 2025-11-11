# /test

Create and run tests derived from this conversation’s changes. Produce unit tests, integration/E2E tests, and regression tests tied to fixes and improvements. Do not stop until all new and related existing tests pass.

Backlinks:
- mini_prompt/lv1/test_improvement_mini_prompt.md
- mini_prompt/lv2/automated_testing_mini_prompt.md
- mini_prompt/lv2/tests_optimization_phase2_mini_prompt.md
- mini_prompt/lv2/test_driven_commit_mini_prompt.md

## Command sequence (run in order)

1) Verify repository context
```bash
gtimeout 5 git rev-parse --show-toplevel
```

2) Snapshot current changes (helps scope what to test)
```bash
gtimeout 5 git status --short
```
```bash
gtimeout 10 git diff --stat | head -50
```

3) Identify impacted areas from conversation and diffs
- Enumerate the modules/files touched and expected behaviors changed
- Decide which tests are needed: unit, integration/E2E, regression
- Update `tests/index_tests.yaml` if adding new tests or categories

4) Create or update tests
- Place tests under `tests/` following existing structure and categories
- Prefer focused, readable tests with clear assertions and failure messages
- Add regression tests that reproduce any bugs discussed, then verify the fix

5) Run fast, high-signal tests first (iterate until green)
```bash
gtimeout 90 bash tests/run_tests.sh --category infrastructure
```
```bash
gtimeout 180 bash tests/run_tests.sh --category integration --criticality=high
```

6) Expand coverage (iterate until green)
```bash
gtimeout 240 bash tests/run_tests.sh --category integration
```

7) Run E2E tests (iterate until green)
```bash
gtimeout 480 bash tests/run_tests.sh --e2e
```

8) Final full sweep (ensure nothing regresses)
```bash
gtimeout 600 bash tests/run_tests.sh --all
```

9) Version control (only stage new/updated tests and related files)
```bash
gtimeout 5 git rev-parse --show-toplevel
```
```bash
gtimeout 10 git add tests/ tests/index_tests.yaml 2>/dev/null || true
```
```bash
gtimeout 10 git status --short
```
```bash
gtimeout 10 git commit -m "Add and update tests from conversation; all passing"
```
```bash
gtimeout 15 git push
```

## Notes
- Keep commands unchained and short; one command per step
- Iterate: write/adjust tests and fixes until all selected runs pass
- Do not introduce unrelated changes; keep scope tied to the conversation
- Prefer deterministic tests; avoid hardcoding ports (use random high ports when needed)
- If any command fails, stop, fix, and retry from the failing step
