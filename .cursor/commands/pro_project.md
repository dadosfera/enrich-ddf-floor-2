# 🏗️ Project Creation & Management Command

**Shortcut:** `pro`
**Purpose:** Create and manage projects (standardized folders with meta-plans).

## 🚀 Usage

### 1. Create New Project
Scaffold a new project structure (`projects/{status}/{slug}`) and its Meta Project plan.

```bash
# Run the creation mini prompt
cat mini_prompt/lv1/create_project_mini_prompt.md | pbcopy
# Paste into your AI Assistant
```

### 2. Manage Existing Project
Navigate to project and review status.

```bash
# List all projects by status
ls -d projects/*/*/

# Review specific project
cd projects/{status}/{project-slug}
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
