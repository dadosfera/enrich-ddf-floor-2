## /tall_tests_all – Full-Codebase Test Orchestrator (Moon-First)

<!-- COMMAND_ID: 043 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ta_tests_all -->

Run the **entire test surface of this repository** using Moon as the primary orchestrator, progressing from smallest affected scopes to a full `tests_all` run.
Use this for **codebase-wide health checks** (pre‑merge, pre‑release), not for individual conversation fixes (use `/tcon_test_conversation` for that).

Backlinks:

- README.md (Moon section)
- mini_prompt/lv1/test_baseline_and_criticality_mini_prompt.md
- mini_prompt/lv2/automated_testing_mini_prompt.md
- tests/run_tests.sh

---

## Command sequence (run in order)

1. Verify repository root and Moon availability

```bash
gtimeout 5 git rev-parse --show-toplevel
```

```bash
gtimeout 5 moon --version
```

- If `moon` is not installed or the second command fails, fall back to the direct runner section below.

2. Start with **affected tests** per Moon category (fast, narrow)

- Goal: validate only what changed first, keep each block time‑boxed (≤60s).

```bash
gtimeout 60 moon run --affected docs-fera:tests_infrastructure
```

```bash
gtimeout 60 moon run --affected docs-fera:tests_integration
```

```bash
gtimeout 60 moon run --affected docs-fera:tests_ai
```

- If any affected run fails:
  - Stop escalation; fix failures in that category before proceeding.
  - Use `/tcon_test_conversation` if failures are tied to the current conversation; otherwise, treat them as global health issues and plan fixes explicitly.

3. Promote to **full categories** (still separated)

- Only after affected runs for a category are green:

```bash
gtimeout 120 moon run docs-fera:tests_infrastructure
```

```bash
gtimeout 180 moon run docs-fera:tests_integration
```

```bash
gtimeout 120 moon run docs-fera:tests_ai
```

- Keep categories independent:
  - You can run one category at a time (e.g., infra only on CI smoke stages).
  - Do not “fix” obviously obsolete tests here; instead, use the obsolescence/retirement mini prompts and adjust suites intentionally.

4. Optional dev tests and mutation tests

- When doing deeper quality sweeps (not every run):

```bash
gtimeout 180 moon run docs-fera:dev_tests_all
```

```bash
gtimeout 300 moon run docs-fera:tests_mutation
```

- Treat mutation failures as **test-quality** work, usually tracked via dedicated plans, not as quick “make it green” tasks.

5. Final **full‑suite run** (macro “run all tests”)

- Only when:
  - Category runs are green, and
  - You explicitly want a full‑suite verification (e.g., before tagging or major merges).

```bash
gtimeout 600 moon run docs-fera:tests_all
```

- If this step times out or fails:
  - Inspect which Moon task failed (infra / integration / ai).
  - Prefer re‑running that specific task and fixing it, rather than re‑running `tests_all` blindly.

6. Fallback when Moon is unavailable

- If Moon is not installed or misconfigured, use the central runner with the same small→large pattern:

```bash
gtimeout 60 bash tests/run_tests.sh --category infrastructure
```

```bash
gtimeout 90 bash tests/run_tests.sh --category integration --criticality=high
```

```bash
gtimeout 120 bash tests/run_tests.sh --category integration
```

```bash
gtimeout 180 bash tests/run_tests.sh --all
```

- Keep using category + criticality first; treat `--all` as the macro “run everything” step, just like the Moon `tests_all` task.

## Notes

- `/tcon_test_conversation` is **conversation‑scoped** (changed behavior only); `/tall_tests_all` is **codebase‑scoped** (global health / pre‑merge / pre‑release).
- Always walk from **affected → per‑category → full‑suite**; never jump straight to `tests_all` when diagnosing a single change.
- Respect timeouts (≤60s per narrow block; larger budgets only for full categories or final full‑suite runs) and prefer Moon over direct scripts when available.
