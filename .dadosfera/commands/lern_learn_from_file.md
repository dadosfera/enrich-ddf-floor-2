# /lern_learn_from_file
<!-- COMMAND_ID: 031 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: le_learn_from_file -->

Ingests a knowledge source (PDF, Excel, Doc) into a local learning directory and generates appropriate documentation based on its content, relying on AI analysis rather than automated scripts.

Backlinks:
- commands/docu_document.md

## Command sequence (run in order)

1) Create learning directory (if needed)
```bash
mkdir -p learn
```

2) Copy source file to learning directory
```bash
cp "SOURCE_FILE_PATH" learn/
```
*(Replace `SOURCE_FILE_PATH` with the actual file path provided by the user)*

3) Analyze file content
- Read the file content from `learn/<filename>`.
- **Note**: For binary files (PDF, Excel), rely on your ability to read them if supported, or ask the user to provide a text export if direct reading fails.
- Extract key concepts, nomenclatures, and processes.

4) Generate documentation
- Create or update documentation in `docs/sales/` (or appropriate category based on content).
- Structure the documentation with:
    - Overview/Summary
    - Key Terminology
    - Detailed Processes
    - Actionable Insights
- Ensure the documentation follows project standards (markdown, clear headers).

## Notes
- Do not use automated scripts (OCR, parsing libraries) to "learn". The learning process is cognitive/AI-driven.
- "Sales" docs are the default target, but adjust based on the actual content of the file.
