## /tall_tests_all – Full-Codebase Test Orchestrator (Moon-First)

<!-- COMMAND_ID: 043 -->
<!-- COMMAND_VERSION: 2.1.0 -->
<!-- COMMAND_TYPE: ta_tests_all -->

Run the **entire test surface of this repository** using Moon as the primary orchestrator, progressing from smallest affected scopes to a full `tests_all` run.
Use this for **codebase-wide health checks** (pre‑merge, pre‑release), not for individual conversation fixes (use `/tcon_test_conversation` for that).

**IMPROVEMENTS in v2.1.0:**
- ☁️ **Cloud First**: Checks for deployed instance (OCI) to offload testing and save local resources
- ✅ Repository-agnostic: Automatically detects Moon project structure
- ✅ Dynamic task discovery: Tries common Moon task patterns
- ✅ Graceful fallback: Uses test runner when Moon tasks unavailable

Backlinks:

- README.md (Moon section)
- mini_prompt/lv1/test_baseline_and_criticality_mini_prompt.md
- mini_prompt/lv2/automated_testing_mini_prompt.md
- tests/run_tests.sh

---

## Command sequence (run in order)

0. **Cloud/Remote Execution Check (Priority)**

- Goal: Run tests on cloud instance if available to avoid overloading local machine.

```bash
# Check for OCI instance and attempt remote execution
if [[ -n "$OCI_INSTANCE_IP" ]]; then
  echo "☁️  Cloud instance detected at $OCI_INSTANCE_IP"
  echo "🚀 Attempting to offload tests to cloud..."

  # Default remote path to same folder name in home if not specified
  REMOTE_PATH=${REMOTE_DIR:-"~/${PWD##*/}"}
  SSH_CMD=${SSH_COMMAND:-"ssh"}
  SSH_USR=${SSH_USER:-"ubuntu"}

  # Try to run make test on remote
  # Assuming code is already synced or deployed
  if $SSH_CMD -o ConnectTimeout=10 "$SSH_USR@$OCI_INSTANCE_IP" "cd $REMOTE_PATH && make test"; then
    echo "✅ Remote tests passed!"
    # Exit successfully to skip local execution
    exit 0
  else
    echo "⚠️  Remote execution failed or not available. Falling back to local..."
  fi
else
  echo "💻 No cloud instance configured (OCI_INSTANCE_IP). Running locally."
fi
```

1. Verify repository root and Moon availability

```bash
gtimeout 5 git rev-parse --show-toplevel
```

```bash
gtimeout 5 moon --version
```

- If `moon` is not installed or the second command fails, fall back to the direct runner section below.

2. **Detect Moon project structure** (NEW in v2.0.0)

- Goal: Automatically discover available Moon tasks without hardcoding project names.

**Detection strategy:**
1. First, try to detect the Moon project name:
   ```bash
   # Detect project name from available tasks
   MOON_PROJECT=$(moon query tasks 2>&1 | grep -E "^[^:]+:test" | head -1 | cut -d: -f1 2>/dev/null || echo "root")
   ```

2. Common patterns to try (in order):
   - `root:test_*` (most common - root-level tasks)
   - `{repo-name}:test_*` (project-scoped tasks, e.g., `docs-fera:tests_*`)
   - Fallback to test runner if no Moon tasks found

3. Start with **affected tests** per Moon category (fast, narrow)

- Goal: validate only what changed first, keep each block time‑boxed (≤60s).

**Try Moon tasks first (if available), with graceful fallback:**

For each category, try Moon tasks in order of likelihood, then fallback:

**Infrastructure/Unit tests:**
```bash
# Try: root:test_unit → root:tests_infrastructure → {project}:tests_infrastructure → fallback
gtimeout 60 moon run --affected root:test_unit 2>/dev/null || \
gtimeout 60 moon run --affected root:tests_infrastructure 2>/dev/null || \
gtimeout 60 bash tests/run_tests.sh --critical
```

**Integration tests:**
```bash
# Try: root:test_integration → root:tests_integration → {project}:tests_integration → fallback
gtimeout 60 moon run --affected root:test_integration 2>/dev/null || \
gtimeout 60 moon run --affected root:tests_integration 2>/dev/null || \
gtimeout 60 bash tests/run_tests.sh --unit
```

**AI/Regression tests:**
```bash
# Try: root:test_regression → root:tests_ai → {project}:tests_ai → fallback
gtimeout 60 moon run --affected root:test_regression 2>/dev/null || \
gtimeout 60 moon run --affected root:tests_ai 2>/dev/null || \
gtimeout 60 bash tests/run_tests.sh --unit
```

- If any affected run fails:
  - Stop escalation; fix failures in that category before proceeding.
  - Use `/tcon_test_conversation` if failures are tied to the current conversation; otherwise, treat them as global health issues and plan fixes explicitly.

4. Promote to **full categories** (still separated)

- Only after affected runs for a category are green:

**Try Moon tasks first (if available), with graceful fallback:**

**Infrastructure/Unit tests:**
```bash
gtimeout 120 moon run root:test_unit 2>/dev/null || \
gtimeout 120 moon run root:tests_infrastructure 2>/dev/null || \
gtimeout 120 bash tests/run_tests.sh --unit
```

**Integration tests:**
```bash
gtimeout 180 moon run root:test_integration 2>/dev/null || \
gtimeout 180 moon run root:tests_integration 2>/dev/null || \
gtimeout 180 bash tests/run_tests.sh --integration
```

**AI/Regression tests:**
```bash
gtimeout 120 moon run root:test_regression 2>/dev/null || \
gtimeout 120 moon run root:tests_ai 2>/dev/null || \
gtimeout 120 bash tests/run_tests.sh --unit
```

- Keep categories independent:
  - You can run one category at a time (e.g., infra only on CI smoke stages).
  - Do not "fix" obviously obsolete tests here; instead, use the obsolescence/retirement mini prompts and adjust suites intentionally.

5. Optional dev tests and mutation tests

- When doing deeper quality sweeps (not every run):

```bash
gtimeout 180 moon run root:test_active 2>/dev/null || \
gtimeout 180 moon run root:dev_tests_all 2>/dev/null || \
gtimeout 180 bash tests/run_tests.sh --all
```

```bash
gtimeout 300 moon run root:test_analysis 2>/dev/null || \
gtimeout 300 moon run root:tests_mutation 2>/dev/null || \
echo "Mutation tests not available, skipping"
```

- Treat mutation failures as **test-quality** work, usually tracked via dedicated plans, not as quick "make it green" tasks.

6. Final **full‑suite run** (macro "run all tests")

- Only when:
  - Category runs are green, and
  - You explicitly want a full‑suite verification (e.g., before tagging or major merges).

```bash
gtimeout 600 moon run root:test_all 2>/dev/null || \
gtimeout 600 moon run root:tests_all 2>/dev/null || \
gtimeout 600 moon run root:test_all_canonical 2>/dev/null || \
gtimeout 600 make test 2>/dev/null || \
gtimeout 600 bash tests/run_tests.sh --all
```

- If this step times out or fails:
  - Inspect which Moon task failed (infra / integration / ai).
  - Prefer re‑running that specific task and fixing it, rather than re‑running `tests_all` blindly.

7. Fallback when Moon is unavailable or tasks not found

- If Moon is not installed, misconfigured, or tasks don't exist, use the central runner with the same small→large pattern:

```bash
gtimeout 60 bash tests/run_tests.sh --critical
```

```bash
gtimeout 90 bash tests/run_tests.sh --unit
```

```bash
gtimeout 120 bash tests/run_tests.sh --integration
```

```bash
gtimeout 180 make test || bash tests/run_tests.sh --all
```

- Keep using category + criticality first; treat `--all` or `make test` as the macro "run everything" step, just like the Moon `tests_all` task.

## Notes

- `/tcon_test_conversation` is **conversation‑scoped** (changed behavior only); `/tall_tests_all` is **codebase‑scoped** (global health / pre‑merge / pre‑release).
- Always walk from **affected → per‑category → full‑suite**; never jump straight to `tests_all` when diagnosing a single change.
- Respect timeouts (≤60s per narrow block; larger budgets only for full categories or final full‑suite runs) and prefer Moon over direct scripts when available.
- **v2.0.0**: Command now automatically adapts to repository's Moon configuration without hardcoding project names.
