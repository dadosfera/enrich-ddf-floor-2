# /dcon_docu_structure_audit
<!-- COMMAND_ID: 066 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: dc_structure_audit -->

## Description
Audits documentation structure and content quality (Layers 0-1) to ensure high-level summaries.

## Usage
`dcon_docu_structure_audit`

## Details
Runs `_dev/scripts/quality_governance/audit_documentation_content.py` to check:
1.  **Layer 0 (Root) & Layer 1 (Top-level)**: strictly high-level pointers, no implementation details.
2.  **Repetition/Garbage**: detects corrupted files (like "guides/guides/guides").
3.  **Required Files**: ensures `README.md` and `AGENTS.md` exist where expected.
4.  **Length Constraints**: warns if top-level documentation is too verbose.

## Command sequence (run in order)

1) Run the audit script
```bash
python3 _dev/scripts/quality_governance/audit_documentation_content.py
```

## Backlinks
- `_dev/scripts/quality_governance/audit_documentation_content.py`
- `commands/docu_document.md`
