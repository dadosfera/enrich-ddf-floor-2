# Rule Activation Guide - Priority & Context

## Rule Priority Levels
- **P1 (Critical)**: Must always be followed - preserve_all_functionality, autonomy_userhandoff
- **P2 (High)**: Apply during major operations - folder_structure_discipline, file_lifecycle_discipline
- **P3 (Medium)**: Apply for specific contexts - central_runsh_interface, environment_platform_configs
- **P4 (Low)**: Apply when relevant - streamlit_config_sync, js_floor_rules

## When to Apply Rules

### File Operations Context
- **Creating new files**: folderstructure_discipline (P2), avoid_duplication (P2)
- **Moving/renaming files**: filelifecycle_discipline (P2), logging_observability (P3)
- **Deleting files**: preserve_all_functionality (P1), filelifecycle_discipline (P2)

### Development Context
- **JavaScript/TypeScript projects**: js_floor_rules (P4), dadosfera_floors (P3)
- **Configuration changes**: configfile_editing (P3), central_runsh_interface (P3)
- **Script creation**: minimize_new_files (P3), avoid_duplication (P2)

### Platform Context
- **Replit environment**: platformspecific_notes (P3), central_runsh_interface (P3)
- **Cursor environment**: platformspecific_notes (P3), restrictions_on_editing_ignored_files (P2)
- **Production deployment**: dadosfera_floors (P3), dryrun_first (P2)

## Rule Application Strategy

1. Always start by checking P1 (Critical) rules
2. Then evaluate P2 (High) rules based on current context
3. Apply P3 (Medium) rules when specific conditions are met
4. Consider P4 (Low) rules for optimization and best practices

## Contextual Activation Principles

- **Prioritize Safety**: P1 rules prevent destructive actions
- **Ensure Structural Integrity**: P2 rules maintain project organization
- **Optimize Workflow**: P3 rules improve development efficiency
- **Enhance Quality**: P4 rules provide additional guidance

## Rule Learning and Evolution System

### Alteration History Tracking
- **Purpose**: Systematically document rule violations, improvements, and learning patterns
- **Location**: `00_alteration_history.md` in both `.clinerules/` and `.cursor/rules/` directories
- **Key Components**:
  1. Incident Documentation
  2. Root Cause Analysis
  3. Pattern Recognition
  4. Continuous Improvement Tracking

### Tracking Categories
- **Rule Violations**: Identify recurring pattern breaks
- **Gap Identification**: Discover missing rule coverage
- **Structure Issues**: Improve rule format and effectiveness
- **Enhancement Requests**: Evolve rules based on real usage
- **Cross-Platform Conflicts**: Resolve inconsistencies between platforms

### Success Metrics
- **Violation Reduction Rate**
- **Rule Application Consistency**
- **Learning Extraction Quality**
- **System Reliability Improvement**

## Available Rules by Priority

### Priority 1 (Critical) - Always Apply
- **1_01**: Preserve All Functionality (`1_01_preserve_all_functionality.md`)
- **1_02**: Autonomy & User Handoff (`1_02_autonomy_user_handoff.md`)

### Priority 2 (High) - Major Operations
- **2_01**: Branch Naming & Documentation (`2_01_branch_naming_documentation.md`)

### Priority 3 (Medium) - Specific Contexts

### Priority 4 (Low) - When Relevant
- **4_01**: Folder-Structure Discipline (`4_01_folder_structure_discipline.md`)
- **4_02**: Config-File Editing (`4_02_config_file_editing.md`)
- **4_03**: Central `run.sh` Interface (`4_03_central_runsh_interface.md`)
- **4_04**: Environment & Platform Configs (`config/`) (`4_04_environment_platform_configs_config.md`)
- **4_05**: Streamlit & Config Sync (`4_05_streamlit_config_sync.md`)
- **4_06**: Path Handling (`4_06_path_handling.md`)
- **4_07**: File-Lifecycle Discipline (`4_07_file_lifecycle_discipline.md`)
- **4_08**: Avoid Duplication (`4_08_avoid_duplication.md`)
- **4_09**: Logging & Observability (`4_09_logging_observability.md`)
- **4_10**: Planning, Docs & CI Standards (`4_10_planning_docs_ci_standards.md`)
- **4_11**: Minimize New Files (`4_11_minimize_new_files.md`)
- **4_12**: Recurrent Errors (`4_12_recurrent_errors.md`)
- **4_13**: Dadosfera Floors (`4_13_dadosfera_floors.md`)
- **4_14**: JS Floor Rules (`4_14_js_floor_rules.md`)
- **4_15**: NO "Simplified / Stand-alone / Partial / Backup" Clones (`4_15_no_simplified_stand_alone_partial_backup_clones.md`)
- **4_16**: Dry-Run First (`4_16_dry_run_first.md`)
- **4_17**: Multi-Command Lines (`4_17_multi_command_lines.md`)
- **4_18**: Platform-Specific Notes (`4_18_platform_specific_notes.md`)
- **4_19**: Restricted Folder Usage (`4_19_restricted_folder_usage.md`)
- **4_20**: Branch Protection Bypass Authorization (`4_20_branch_protection_bypass_authorization.md`)

---
*Generated automatically from .cursor/rules/ directory on $(date)*
