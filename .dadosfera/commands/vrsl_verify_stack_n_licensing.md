# /vrsl_verify_stack_n_licensing
<!-- COMMAND_ID: 025 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: vr_verify_stack_n_licensing -->

**Shortcut:** `vrsl`
**Purpose:** Verify licensing and tech stack configuration (licensing + stack).

## 🚀 Usage
```bash
./scripts/verify_repo.sh
```

## 📋 Details
This command scans the repository root for:
- Licensing: license files and license fields in manifest files
- Tech stack indicators: presence of common config files (package.json, pyproject.toml, go.mod, etc.)

## 📂 Artifacts
- Script: `scripts/verify_repo.sh`
