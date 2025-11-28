# /hce_hardcoding_elimination

Eliminate hardcoded ports, IPs, localhost references, and secrets; remove defaults and enforce fail-fast required parameters. Use the lv1 hardcoding mini prompts as the source of truth; follow their patterns and guard rails precisely.

Backlinks:
- mini_prompt/lv1/hardcoding_ports_ips_and_secrets_elimination_mini_prompt.md
- mini_prompt/lv1/remove_defaults_hardcoding_fail_fast_mini_prompt.md

## Execution steps (run in order)

1) Verify repository context
```bash
gtimeout 5 git rev-parse --show-toplevel
```

2) Prepare inventory file (read/write)
```bash
gtimeout 5 mkdir -p analysis
```
```bash
gtimeout 5 touch analysis/hardcodes_inventory.md
```

3) Discovery scans (quick pass; see the mini prompt for complete patterns)
- Note: Keep output short; refine with the full patterns from the lv1 prompt afterward.
```bash
gtimeout 8 rg -n --hidden -S "(localhost|127\\.0\\.0\\.1)" | head -200
```
```bash
gtimeout 8 rg -n --hidden -S ":[0-9]{2,5}([/\"'[:space:]]|$)" | head -200
```
```bash
gtimeout 8 rg -n --hidden -S "(API_KEY|SECRET|TOKEN|PASSWORD)" | head -200
```

4) Document findings
- Summarize paths/snippets/categories in `analysis/hardcodes_inventory.md`.
- Define a mapping to central variables (env/config) for each finding.

5) Central variable definition (dev templates; non‑sensitive only)
- Ensure config templates exist and include the mapped variables:
  - `config/.env.dev.template`, `config/ports.yaml`, `config/config.yaml`
- Keep real secrets out of git; only placeholders/IDs in templates/config.

6) Refactor replacements (ports/hosts/URLs/secrets)
- Replace literals with env/config reads.
- Maintain temporary fallbacks only when required to preserve behavior during rollout.
- Re-run scans from step 3 to confirm elimination.

7) Remove defaults and enforce fail‑fast required parameters
- Introduce/ensure “require” helpers per language.
- Replace silent defaults/fallbacks with explicit validations (see lv1 prompt).

8) Lint, build, and tests (use repo’s central runners)
```bash
gtimeout 60 bash tests/run_tests.sh --category infrastructure
```
```bash
gtimeout 180 bash tests/run_tests.sh --category integration --criticality=high
```
```bash
gtimeout 600 bash tests/run_tests.sh --all
```

9) Commit logically (group by area), then push
- Prefer small, focused commits per subsystem (e.g., frontend URLs, backend ports, CI templates).
- Use single-line messages without emojis.

## Notes
- Follow guard rails from both lv1 mini prompts (absolute paths, timeouts, no chained commands, preserve functionality).
- Do not commit real secrets; use templates/placeholders and reference a secret manager for production.
- If scans still detect hardcoding, iterate: update mapping/templates and refactor again before committing.
