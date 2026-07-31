---
category: automation
criticality: medium
scope: all
---
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
- _dev/scripts/start_repo.sh

## When to Use

- Starting a new Dadosfera project from scratch
- Converting an existing project to Dadosfera standards
- Setting up a new module or service repository
- Bootstrapping AI-ready repositories with cursor rules

## When NOT to Use

- Creating internal project folders within an existing repo → use `/proj_project`
- Cloning an existing repository → use `git clone`
- Setting up temporary or throwaway projects

## Purpose

Initialize a new repository with the standard Dadosfera folder structure, AI agent rules, cursor commands, and CI/CD workflows. Wraps the `_dev/scripts/start_repo.sh` bootstrap script with guided configuration.

## Command Syntax

```bash
/init_repo <repo-name> [--type <type>]
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `repo-name` | Yes | - | Name of the repository to initialize |
| `--type` | No | `standard` | Repository type (see Repository Types below) |

### Repository Types

| Type | Description |
|------|-------------|
| `standard` | General-purpose project with docs, tests, scripts |
| `fera` | Internal Dadosfera `-fera` repository with `_dev/` structure |
| `service` | Microservice with API, Dockerfile, and CI pipeline |
| `library` | Shared library with packaging and publish workflow |
