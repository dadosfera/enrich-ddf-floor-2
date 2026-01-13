# 🏗️ Project Creation & Management Command

<!-- COMMAND_ID: 037 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pr_project -->

**Shortcut:** `pro`
**Purpose:** Create and manage projects (standardized folders with meta-plans).

## 🚀 Usage

### 1. Create New Project

Scaffold a new project structure (`docs/projects/{status}/{slug}`) and its Meta Project plan.

> **Note**: For -fera repositories, use `_dev/docs/projects/{status}/{slug}`.

```bash
# Run the creation mini prompt
cat mini_prompt/lv1/create_project_mini_prompt.md | pbcopy
# Paste into your AI Assistant
```

### 2. Manage Existing Project

Navigate to project and review status.

```bash
# List all projects
ls -d docs/projects/*/*/ 2>/dev/null || ls -d _dev/docs/projects/*/*/ 2>/dev/null

# Review specific project
cd docs/projects/{status}/{project-slug}
# OR for -fera repos:
cd _dev/docs/projects/{status}/{project-slug}
```

## 📋 Context

A **Project** is a self-contained domain of work within the repository.
A **Meta Project** is the `meta_plan` inside a project that coordinates its internal plans.

## 🔗 Related Commands

- `pla` - Create individual plans
- `jou` - Journey (Meta Plan) management
- `inv` - Inventory & Priorities

## 📂 Artifacts

- **Mini Prompt:** `mini_prompt/lv1/create_project_mini_prompt.md`
- **Template:** `templates/meta_plan_template.md`
