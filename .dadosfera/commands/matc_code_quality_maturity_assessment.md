# /matc_code_quality_maturity_assessment

<!-- COMMAND_ID: 026 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: maturity_assessment -->

**Shortcut**: `matc`

**Analysis only – read-only maturity scan of the codebase.** Assess the repository across all maturity standards (deployment, lifecycle, architecture, testing, pre-commit, logging) using the Agents&Devs Floors/Levels framework and existing mini prompts, and produce a consolidated scorecard plus recommended next‑level mini prompts. This command defines the assessment workflow; it does **not** implement changes or run heavy automation by itself.

Backlinks:

- **Local Reference**: `standards/maturity/index_maturity.yaml`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/index_maturity.yaml`
- **Local Reference**: `standards/maturity/deployment_maturity.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/deployment_maturity.md`
- **Local Reference**: `standards/maturity/software_lifecycle_maturity.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/software_lifecycle_maturity.md`
- **Local Reference**: `standards/maturity/testing_maturity.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/testing_maturity.md`
- **Local Reference**: `standards/maturity/pre_commit_maturity.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/pre_commit_maturity.md`
- **Local Reference**: `standards/maturity/logging_maturity.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/logging_maturity.md`
- **Local Reference**: `standards/maturity/architecture_maturity.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/architecture_maturity.md`
- **Local Reference**: `mini_prompt/index_mini_prompt.yaml`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/index_mini_prompt.yaml`
- **Local Reference**: `mini_prompt/lv2/repo_maturity_analysis_and_learning_mini_prompt.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv2/repo_maturity_analysis_and_learning_mini_prompt.md`

## Command sequence (run in order)

1. **Confirm repository context (for references only)**

   ```bash
   gtimeout 5 git rev-parse --show-toplevel
   ```

   - Detect whether the current repo is part of the Agents&Devs Dadosfera Framework (e.g. `*-ddf`, `*-fera`, or framework‑ddf family).
   - Record the absolute repo root path and repository name; you will need both when linking maturity results and plans.

2. **Inventory maturity standards and mini prompts (read‑only)**

   - List available maturity standards in this repo:
     ```bash
     gtimeout 5 ls -1 standards/maturity/ 2>/dev/null | head -50
     ```
   - From `standards/maturity/index_maturity.yaml`, identify all domains to be scored (currently: deployment, software lifecycle, architecture, testing, pre‑commit, run.sh logging).
   - From `mini_prompt/index_mini_prompt.yaml`, map for each domain:
     - Analysis / assessment mini prompts (e.g. `repo_maturity_analysis_and_learning`, `critical_files_review`, `config_claims_vs_code_incongruence_detector`).
     - Improvement mini prompts per category (testing, pre‑commit, logging, infrastructure, architecture, etc.).
   - If the repo is part of the broader Agents&Devs framework, also locate the **floor/level‑specific mini prompts** for each category and level in the framework repositories (framework‑ddf, planner‑ddf‑floor‑2, etc.). Do **not** run them yet; just catalogue them.

3. **Collect repository maturity signals per domain (no modifications)**

   - **Deployment:**
     - Check for deployment assets: `Jenkinsfile`, `Dockerfile`, `docker-compose*`, `k8s/`, `helm/`, `workflows/run.sh`, environment configs under `config/`.
     - Identify whether deployments are local only, VM‑based, container‑based, or Kubernetes/managed platforms as per `deployment_maturity.md`.
   - **Software lifecycle / structure:**
     - Inspect high‑level structure (`ls -1` at repo root) and look for lifecycle floors (`1_prototype/`, `2_alpha/`, `3_beta/`, `4_ga/`) or equivalent patterns described in `software_lifecycle_maturity.md`.
     - Note where core workflows, scripts, templates, and tests live relative to those floors.
   - **Architecture & modularity:**
     - Identify the main architectural building blocks (e.g. `domain/`, `application/`, `infrastructure/`, `ui/`, `features/`) and how they depend on each other.
     - Look for separation of concerns and clear boundaries between UI/transport, application/use‑case logic, domain logic, and infrastructure/adapters.
     - Check for architecture docs and ADRs describing allowed dependency directions and module responsibilities.
     - Treat explicit patterns (MVC, MVVM, Clean, hexagonal, feature‑sliced, etc.) as evidence of higher maturity, not as hard requirements; focus on layering and boundaries rather than on specific pattern names.
   - **Testing:**
     - Detect presence and depth of tests (`tests/`, `pyproject.toml` pytest config, `tests/run_tests.sh`, Playwright/Cypress configs, mutation‑test helpers, etc.).
     - Map evidence to Floors 0‑3 in `testing_maturity.md` (foundation, integration, product layer, AI excellence).
   - **Pre‑commit:**
     - Look for `.pre-commit-config.yaml`, hook installation scripts, and CI integration (`pre-commit run --all-files` in pipelines).
     - Cross‑check against levels in `pre_commit_maturity.md` (local hygiene → enterprise‑certified pipelines).
   - **run.sh logging:**
     - Inspect `workflows/run.sh` (or equivalent entry point) for colorized logging, timestamps, log file persistence, signal handling, resource detection, JSON logs, and PID tracking as per `logging_maturity.md`.

   Keep this step strictly read‑only: use `rg`, `ls`, `cat`, and other non‑mutating tools only.

4. **Assign current Floors/Levels per maturity standard**

   For each maturity domain:

   - Read the corresponding standard in `standards/maturity/` and apply its scoring rules:
     - **Deployment** → 1–8 levels (local code → multi‑cloud K8s).
     - **Software Lifecycle** → floors `1_prototype` → `4_ga`.
     - **Architecture & Modularity** → Levels 0–4 (Ad‑hoc/entangled → Institutionalized architecture).
     - **Testing** → Floors 0–3 (Foundation, Integration, Product Layer, AI Excellence).
     - **Pre‑commit** → Levels 1–5 (Local Hygiene → Enterprise‑Certified Pipelines).
     - **Logging (run.sh)** → Levels 0–3 (Non‑compliant → Full compliance).
   - For each domain:
     - Document observed signals (files, configs, scripts).
     - Choose the **lowest clearly supported level/floor** when ambiguous and record any uncertainties.
     - Optionally, infer an **Agents&Devs Floor** (e.g. ADRF Floor 0–4) that this domain maps to, if that mapping exists in the broader framework.

   Store results in a structured in‑memory table (per‑domain row: current_level, evidence, confidence).

5. **Map to domain mini prompts and floor/level progression (do not execute them here)**

   - For each maturity domain, determine **next target level/floor** (usually current+1, bounded by the maximum defined in that standard).
   - Using `mini_prompt/index_mini_prompt.yaml` (and, when available, the Agents&Devs framework repositories):
     - Select **assessment mini prompts** that deepen analysis for that domain at the current floor/level.
     - Select **improvement mini prompts** that correspond to the **next target level/floor**.
   - For each (domain, target level/floor) pair, output:
     - A short rationale for the recommended target.
     - A list of mini prompts to run later (IDs + relative paths), clearly labeled as **NOT executed by this command**.

6. **Produce a consolidated maturity scorecard (conversation output only)**

   Structure the command’s response with:

   - **Maturity Scorecard Table**:
     - Columns: Domain, Current Level/Floor, Max Level/Floor, Evidence Summary, Confidence (Low/Med/High).
   - **Per‑Domain Recommendations**:
     - Recommended next target level/floor.
     - Suggested mini prompts to run (assessment + improvement), grouped as:
       - “Assess now (analysis‑only mini prompts)”
       - “Improve next (implementation‑oriented mini prompts or plans)”
   - **Global Summary**:
     - Overall maturity posture (e.g. “strong engineering practices, infra needs growth”).
     - 3–5 cross‑domain quick wins (QW\_‑style) that could be turned into prioritized plans in the improvement target repo.

   This command must **not**:

   - Edit files, move directories, or run refactors.
   - Create plans or projects directly. Use planning commands (`/prio_investigate_codebase_priorities`, `/pfac_plan_from_active_tasks_conversation`, `/arch_archive`) in follow‑up steps if the user wants plans.

7. **Relationship to other commands and frameworks**

- Use `/prio_investigate_codebase_priorities` **after** this command when you want to translate maturity gaps into concrete plans/projects.
- Use `/vrsl_verify_stack_n_licensing` before major modernization to validate stack/licensing assumptions.
- Use `/tcon_test_conversation`, `/lint_lint`, `/hook_hooks_setup`, or domain‑specific improvement commands **after** the relevant domain mini prompts have been selected.
- When working inside Agents&Devs framework repos (framework‑ddf and related), align each domain’s current and target levels with the **floor/level‑specific mini prompts** defined there; this command only **selects and recommends** those prompts, it does not execute them.

---

**Notes**

- This is an **assessment orchestrator command**: its job is to connect maturity docs and floor/level mini prompts into a coherent analysis; all code changes must happen via explicit follow‑up commands and plans.
- Keep executions bounded: avoid scanning huge monorepos exhaustively; favor top‑level folders, critical files, and existing test/CI/logging entry points when gathering signals.
- Always respect repository‑specific maturity docs if they override global defaults in `standards/maturity/`.
