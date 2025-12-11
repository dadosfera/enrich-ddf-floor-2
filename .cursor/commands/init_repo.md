# /init_repo

<!-- COMMAND_ID: 046 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: in_repo -->

Initialize a new repository with standard Dadosfera folder structure, rules, and commands.

**Local Reference**: `commands/init_repo.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/init_repo.md`

Backlinks:

- standards/project/project_structure_standard.md
- templates/git_repository.md
- scripts/start_repo.sh

## Purpose

Bootstrap a new repository with the complete Dadosfera standard structure, including:

- Standard folder structure based on repository type (-fera, -ddf, standard)
- `.cursor/rules/` and `.cursor/commands/` copied from docs-fera
- `.dadosfera/` configuration if available
- README.md, AGENTS.md, Makefile, and workflows/run.sh templates
- Proper .gitignore

## When to Use

- Starting a new Dadosfera project from scratch
- Converting an existing project to Dadosfera standards
- Setting up a new module or service repository
- Bootstrapping AI-ready repositories with cursor rules

## When NOT to Use

- Creating internal project folders within an existing repo → use `/proj_project`
- Cloning an existing repository → use `git clone`
- Setting up temporary or throwaway projects

## Command Syntax

```bash
/init_repo <target_directory> [-t TYPE] [-f]
```

### Parameters

| Parameter            | Required | Default     | Description                                   |
| -------------------- | -------- | ----------- | --------------------------------------------- |
| `<target_directory>` | Yes      | -           | Path where the new repo will be created       |
| `-t TYPE`            | No       | auto-detect | Repository type: `fera`, `ddf`, or `standard` |
| `-f`                 | No       | false       | Force overwrite if directory exists           |

### Repository Types

| Type       | Name Pattern | Plans Directory    | Example Repos           |
| ---------- | ------------ | ------------------ | ----------------------- |
| `fera`     | `*-fera`     | `_dev/docs/plans/` | docs-fera, scripts-fera |
| `ddf`      | `*-ddf`      | `docs/plans/`      | agent-ddf, case-ddf     |
| `standard` | (any other)  | `docs/plans/`      | my-project              |

## Usage Examples

### Example 1: Create a -fera repository

```bash
/init_repo ~/local_repos/tools-fera

# Auto-detects type as 'fera' from name
# Creates: _dev/docs/plans/active/, _dev/hooks/, etc.
```

### Example 2: Create a -ddf repository

```bash
/init_repo ~/local_repos/analytics-ddf

# Auto-detects type as 'ddf' from name
# Creates: docs/plans/active/, standard structure
```

### Example 3: Force specific type

```bash
/init_repo ~/local_repos/my-service -t ddf

# Forces 'ddf' structure regardless of name
```

### Example 4: Overwrite existing directory

```bash
/init_repo ~/local_repos/existing-project -f

# WARNING: Removes existing directory first!
```

## What Gets Created

```
<repo>/
├── config/                    # Configuration files
├── scripts/                   # Utility scripts
├── tests/                     # Test files
├── workflows/
│   └── run.sh                 # Main entry point script
├── logs/                      # Log files
├── .cursor/
│   ├── rules/                 # AI rules (copied from docs-fera)
│   └── commands/              # AI commands (copied from docs-fera)
├── .dadosfera/                # Dadosfera config (if exists in docs-fera)
├── README.md                  # Project README
├── AGENTS.md                  # AI agent documentation
├── Makefile                   # Make targets
└── .gitignore                 # Git ignore patterns
```

### For -fera repositories (additional):

```
<repo>/
└── _dev/
    ├── docs/
    │   └── plans/
    │       ├── active/
    │       ├── finished/
    │       ├── backlog/
    │       └── prioritized/
    ├── hooks/
    └── scripts/
```

### For -ddf/standard repositories (additional):

```
<repo>/
└── docs/
    └── plans/
        ├── active/
        ├── finished/
        ├── backlog/
        └── prioritized/
```

## Post-Creation Steps

After running `/init_repo`:

1. **Navigate to the new repository**:

   ```bash
   cd ~/local_repos/<new-repo>
   ```

2. **Initialize git**:

   ```bash
   git init
   ```

3. **Make initial commit**:

   ```bash
   git add .
   git commit -m "Initial repository structure"
   ```

4. **Set up remote** (if GitHub repo exists):

   ```bash
   git remote add origin git@github.com:dadosfera/<repo-name>.git
   git push -u origin main
   ```

5. **Verify structure**:
   ```bash
   make help
   bash workflows/run.sh --help
   ```

## Implementation

The command delegates to `scripts/start_repo.sh`:

```bash
bash scripts/start_repo.sh <target_directory> [-t TYPE] [-f]
```

## Error Handling

| Error             | Message                        | Solution                         |
| ----------------- | ------------------------------ | -------------------------------- |
| Missing target    | "Target directory is required" | Provide target directory path    |
| Directory exists  | "Directory already exists"     | Use `-f` flag to overwrite       |
| Invalid type      | "Invalid repository type"      | Use `fera`, `ddf`, or `standard` |
| docs-fera missing | "Cannot find .cursor/rules"    | Ensure running from docs-fera    |

## Related Commands

- **`/proj_project`**: Create internal project folders within a repo
- **`/pfac_plan_from_active_tasks_conversation`**: Create plans for new repos
- **`/expp_xpand_plan`**: Expand plans with detailed tasks

## Related Documents

- **Standard**: `standards/project/project_structure_standard.md`
- **Template**: `templates/git_repository.md`
- **Script**: `scripts/start_repo.sh`
- **Validation**: `scripts/validate_project_structure.sh`

## Notes

- The script requires docs-fera to be available locally at `$DOCS_FERA_ROOT`
- Rules and commands are copied, not symlinked, for repository independence
- The created `workflows/run.sh` follows Level 2 compliance standards
- Consider running `git init` immediately after creation to enable version control
