# /document

Document fixes and improvements from this conversation across multiple locations: README.md and AGENTS.md files in relevant subfolders, script console logs and helper functions, and other documentation files. Ensure comprehensive backlinking and cross-references.

Backlinks:
- mini_prompt/lv1/post_discovery_codebase_improvement_mini_prompt.md
- mini_prompt/lv1/directory_organization_and_indexing_mini_prompt.md
- mini_prompt/lv2/cross_repo_standardization_mini_prompt.md

## Command sequence (run in order)

1) Verify repository context
```bash
gtimeout 5 git rev-parse --show-toplevel
```

2) Snapshot current changes (identify what needs documentation)
```bash
gtimeout 5 git status --short
```
```bash
gtimeout 10 git diff --stat | head -50
```

3) Identify documentation targets from conversation and changes
- List all fixes, improvements, and new behaviors introduced
- Map each to relevant documentation locations:
  - Subdirectory README.md files (if functionality affects specific areas)
  - Subdirectory AGENTS.md files (for AI agent guidance)
  - Script files (console logs, helper function comments, usage examples)
  - Guide files in `/guides/` or patterns in `/patterns/`
  - Lessons learned entries in `/lessons_learned/`
  - Troubleshooting entries in `/trouble_shooting/`

4) Create or update README.md files
- For each affected subdirectory, create or update README.md with:
  - Purpose and usage overview
  - New behaviors or fixes
  - Examples and common use cases
  - Cross-references to related documentation

5) Create or update AGENTS.md files
- For complex subdirectories, create or update AGENTS.md with:
  - AI agent-specific guidance
  - Warnings about common pitfalls
  - References to critical rules and patterns
  - Examples of correct usage patterns

6) Update script documentation
- Update console log messages in scripts to reflect fixes
- Add or update helper function docstrings/comments:
  - Parameter descriptions
  - Return value explanations
  - Usage examples
  - References to related documentation
- Add inline comments explaining:
  - Why specific approaches were chosen
  - Common pitfalls to avoid
  - Warnings about breaking changes

7) Update guide and pattern documentation
```bash
gtimeout 5 find guides/ patterns/ -name "*.md" -type f | grep -E "(relevant|related)" | head -20
```
- Update relevant guide files with new information
- Create or update pattern documentation if new patterns emerged
- Ensure all patterns follow `_template.md` structure where available

8) Create lessons learned entry (if significant fix/improvement)
```bash
gtimeout 5 mkdir -p lessons_learned
```
- Create timestamped entry: `lessons_learned/YYYY-MM-DD_brief-description.md`
- Include key insights, context, and prevention strategies
- Cross-reference related documentation and tests

9) Update troubleshooting docs (if error-related)
```bash
gtimeout 5 ls -1 trouble_shooting/*.md 2>/dev/null | head -10
```
- Add entry or update existing troubleshooting guide
- Include symptoms, root cause, and resolution steps

10) Validate cross-references and backlinks
- Ensure all new documentation links to related files
- Verify README.md → AGENTS.md → script comments form coherent chain
- Check that index.yaml files reference new documentation if applicable

11) Version control (stage documentation changes)
```bash
gtimeout 5 git rev-parse --show-toplevel
```
```bash
gtimeout 10 git add -A
```
```bash
gtimeout 10 git status --short | grep -E "(README|AGENTS|\.md|\.sh|\.py)" | head -30
```
```bash
gtimeout 10 git commit -m "Document fixes and improvements from conversation across README, AGENTS, scripts, and guides"
```
```bash
gtimeout 15 git push
```

## Notes
- Keep commands unchained and short; one command per step
- Prioritize high-impact areas and error-prone code paths
- Follow existing documentation patterns and templates
- Ensure all documentation uses clear, concise language with examples
- Cross-reference related files to create documentation network
- Do not create duplicate documentation; update existing files when appropriate
- Validate all documentation changes before committing
