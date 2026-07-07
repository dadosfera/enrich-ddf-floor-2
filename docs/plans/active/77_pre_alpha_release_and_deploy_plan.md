# 🚀 Pre-Alpha Release & Deploy — enrich-ddf-floor-2

**Status:** Active — Not started
**Priority:** P1 (Critical — blocks a downstream consumer)
**Timeline:** ~0.5–1 week
**Owner:** luis@dadosfera.ai
**Last Updated:** 2026-07-07

## 🎯 Objective

Get `enrich-ddf-floor-2` (the "Unified Data Enrichment Platform", FastAPI + Vite) into a **clean, merged, deployed pre-alpha on STG** with a stable public HTTP API, so downstream consumers can integrate against it.

## ⬇️ Downstream consumer (why this exists now)

This is **Phase 0.A–0.E** for CRM-DDF sub-plan **`p3_m6_hva_enrichment_buyer_discovery.md`** (High-Value Assets cross-border buyer discovery). The CRM will call this service (aliased `enrich-ddf`) for firmographic/person enrichment and company search. No CRM integration work starts until this plan exits green. Keep this repo's API stable once published.

## 📊 Current state (2026-07-07)

- On branch `chore/hooks-installer-20260127b` with a **dirty tree** (heavy `.cursor/commands` distribution churn).
- Stale branches not merged: `chore/hooks-installer-20260127`, `chore/commands-sync-20260115_124459`, `…_180218`.
- Has `compose.yml`, `Makefile`, `Jenkinsfile`, Alembic; **no `deploy/standalone/` or Helm chart yet** (deploy-standalone Scenario B).
- Root litter: several `compose.yml.bak.*` / `Makefile.bak.*` — clean up.

## ✅ Exit criteria

- [ ] Working tree clean; all intended work committed; `main` is authoritative.
- [ ] Stale/merged branches deleted (local + origin).
- [ ] Green CI on `main` (Jenkins + GitHub Actions); tests pass with **no masking skips**.
- [ ] `deploy/standalone/` (compose) + `deploy/helm-chart/` exist and pass `docker compose config` / `helm lint` / `helm template`.
- [ ] Pre-alpha deployed to STG (`*.stg.dadosfera.ai`), health endpoint live, versioned/tagged.
- [ ] STG service + projected call volume registered in `budget-ddf`.
- [ ] Consumer API contract published (company enrich, person enrich, company search) + recorded fixtures handed to the CRM repo.

## 🔧 Tasks

### 0.A — Repo hygiene & branch convergence
- [ ] Triage the dirty tree with `/gscv_git_sync_conversation` or `/gsyn_git_sync` — separate real changes from `.cursor/commands` churn; **no blind `git add -A`**. `/gsta_git_stash` per-hunk for anything ambiguous.
- [ ] Remove `compose.yml.bak.*` / `Makefile.bak.*` litter.
- [ ] Commit intended work; classify each stale branch (merge / delete); merge to `main` via PR+CI or `/merg_merge`.
- [ ] Delete merged/stale branches locally and on origin.

### 0.B — Green build & test on `main`
- [ ] Clean checkout of `main`; `make install`.
- [ ] Full pytest suite green, no skips masking failures; `pre-commit run --all-files` clean.
- [ ] CI green on `main`.

### 0.C — Deploy artifacts (`/deploy-standalone` skill)
- [ ] Map components: FastAPI API (`main.py`), Vite frontend, DB (SQLite dev / Postgres via Alembic).
- [ ] Scaffold `deploy/standalone/docker-compose.prod.yml` + `.env.example` (build-local default, `*_IMAGE` overridable) and `deploy/helm-chart/`.
- [ ] `docker compose` only; idempotent; placeholders (no real secrets); STG ingress `*.stg.dadosfera.ai`; frontend `API_UPSTREAM` proxy `/api → backend`.
- [ ] **Verify:** `docker compose config`, `helm lint`, `helm template`, frontend build — all pass.

### 0.D — Pre-alpha release to STG
- [ ] Follow canonical flow (`pre-main → beta → main`; pre-alpha = STG artifact off `beta`). See docs-fera deployment guide.
- [ ] Version/tag the pre-alpha; record image ref.
- [ ] Helm dry-run → apply to STG; confirm health endpoint responds live.
- [ ] Register STG service + expected enrichment-API volume in `budget-ddf`.

### 0.E — Publish consumer API contract
- [ ] Document real request/response for: **company enrich** (name/domain/tax-id/country), **person enrich** (name/email/company-domain), **company search** (industry/keywords/countries/size). Confirm auth (API key vs OAuth), base URL, rate limits.
- [ ] Export recorded fixtures → hand to CRM repo (`server/integrations/__fixtures__/enrich-ddf/`) for M6's fixture-based client tests.

## 🔗 References

- Canonical flow & rules: `submodules/docs-fera/guides/dadosfera_deployment/dadosfera_deployment_guide.md`; `deploy-standalone` skill; reference deployer `deployer-ddf-mod-open-llms` (`dist-pre-alpha/`).
- Downstream consumer: CRM-DDF `docs/plans/active/p3_m6_hva_enrichment_buyer_discovery.md` (§2.6 Phase 0, §5 clients).
