---
# Dadosfera Metadata
category: planning
criticality: critical
scope: all
commandId: "077"
version: "1.0.0"
type: "im_import_conversation"
canonical: "docs-fera@/commands/imco_import_conversation_chunknizing.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/imco_import_conversation_chunknizing.md"
backlinks:
  - "_dev/conversations/README.md"
  - "commands/arch_archive.md"

# Claude Code Metadata
name: "Import Conversation"
description: "Import and chunk external conversations for analysis and context"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 077 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: im_import_conversation -->
# /imco_import_conversation_chunknizing

**Command**: `/imco_import_conversation_chunknizing`

Imports the last exported conversation from Cursor or Dadosfera in ~/Downloads (default folder), extracts the main objective, and saves it to `docs/conversations/` chunked into files of maximum 3000 lines each with descriptive names.

## Purpose

This command processes exported conversations from Cursor or Dadosfera by:
1. Finding the most recent exported conversation in ~/Downloads (or specified folder)
2. Analyzing the conversation content to identify the main objective
3. Chunking the conversation into manageable files (max 3000 lines each)
4. Saving to `docs/conversations/` with clear, descriptive filenames based on the main objective

## When to Use

- After exporting a conversation from Cursor or Dadosfera
- When you want to archive and organize conversations in the repository
- When you need to analyze conversation patterns or extract key objectives

## Command Sequence

**Note**: The code blocks below show internal logic/parameters, not bash commands to execute. This command is invoked via slash command syntax (e.g., `/imco_import_conversation_chunknizing`) in AI agent interfaces (Cursor, Dadosfera, Cline, etc.).

### 1. Verify Repository Context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

### 2. Set Default Parameters

**Internal Parameters:**
- `DOWNLOAD_FOLDER`: Default `~/Downloads`, can be overridden
- `MAX_LINES_PER_CHUNK`: Default `3000` lines per file
- `OUTPUT_DIR`: Default `docs/conversations/`

```bash
DOWNLOAD_FOLDER="${1:-$HOME/Downloads}"
MAX_LINES_PER_CHUNK=3000
OUTPUT_DIR="docs/conversations"
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
```

### 3. Find Last Exported Conversation

Find the most recent conversation file matching patterns:
- `cursor_*.md`
- `dadosfera_*.md`

```bash
# Find most recent exported conversation
LAST_CONV=$(find "$DOWNLOAD_FOLDER" -maxdepth 1 -type f \( -name "cursor_*.md" -o -name "dadosfera_*.md" \) -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -z "$LAST_CONV" ] || [ ! -f "$LAST_CONV" ]; then
  echo "❌ No exported conversations found in $DOWNLOAD_FOLDER"
  echo "   Looking for files matching: cursor_*.md or dadosfera_*.md"
  exit 1
fi

echo "✅ Found conversation: $(basename "$LAST_CONV")"
```

### 4. Analyze Conversation to Extract Main Objective

Read the conversation and analyze it to determine:
- Main topic/objective
- Key tasks discussed
- Primary focus area

**Analysis Strategy:**
- Read first 200 lines to understand context
- Look for explicit objectives in user messages
- Identify recurring themes
- Extract key technical terms or project names
- Generate a descriptive slug (lowercase, underscores, max 50 chars)

**CRITICAL: Create Meaningful, Descriptive Names**

The AI agent MUST create a meaningful, descriptive name that clearly identifies the conversation's main objective. The name should:
- Be specific and descriptive (not generic like "conversation_001" or "chat_export")
- Capture the primary purpose or outcome of the conversation
- Use clear, searchable terms that would help someone find this conversation later
- Follow the pattern: `{verb}_{noun}_{specific_detail}` when possible

**Good examples:**
- `exported_conversation_processing_command_creation` (describes what was created)
- `legal_terms_privacy_policy_analysis` (describes the analysis topic)
- `command_rename_cli_tool_implementation` (describes the implementation)
- `test_coverage_script_automation` (describes the automation)

**Bad examples (avoid these):**
- `conversation_001` (too generic)
- `chat_export` (not descriptive)
- `cursor_export` (doesn't describe content)
- `test` (too vague)

```bash
# Read conversation and extract main objective
CONV_CONTENT=$(cat "$LAST_CONV")
FIRST_LINES=$(head -200 "$LAST_CONV")

# Analyze to extract objective (this is done by AI agent, not script)
# The AI should:
# 1. Read the conversation content thoroughly
# 2. Identify the main objective/topic (what was the primary goal?)
# 3. Extract key actions, outcomes, or topics discussed
# 4. Generate a descriptive slug that clearly identifies the conversation's purpose
#    - Use format: {action}_{topic}_{specific_detail} when possible
#    - Make it searchable and meaningful (not generic)
#    - Examples: "exported_conversation_processing_command_creation", "legal_terms_privacy_policy_analysis"
# 5. Create a clear title (e.g., "Exported Conversation Processing Command Creation")
```

### 5. Create Folder Structure and Generate Descriptive Filename

**CRITICAL: Create Organized Folder Structure**

The AI agent MUST create a folder structure to organize conversations. Create a subfolder within `docs/conversations/` based on the main objective slug. This keeps related conversation chunks together and makes the directory more organized.

**Folder Structure Pattern:**
- Create folder: `docs/conversations/{objective_slug}/`
- Store all chunks for this conversation in this folder
- This prevents `docs/conversations/` from becoming cluttered with many files

**Example:**
- Objective: `exported_conversation_processing_command_creation`
- Folder: `docs/conversations/exported_conversation_processing_command_creation/`
- Files: `2026-01-16_cursor_part1.md`, `2026-01-16_cursor_part2.md`, etc.

Create filename based on:
- Date (YYYY-MM-DD format)
- Descriptive slug from main objective (used for folder name)
- Platform (cursor or dadosfera)

```bash
# Extract date from file or use current date
FILE_DATE=$(stat -f "%Sm" -t "%Y-%m-%d" "$LAST_CONV" 2>/dev/null || date +%Y-%m-%d)

# Determine platform
if [[ "$(basename "$LAST_CONV")" == cursor_* ]]; then
  PLATFORM="cursor"
else
  PLATFORM="dadosfera"
fi

# Generate base filename (AI agent determines OBJ_SLUG from analysis)
OBJ_SLUG="main_objective_slug"  # This is determined by AI analysis

# Create folder structure: docs/conversations/{objective_slug}/
CONV_FOLDER="$REPO_ROOT/$OUTPUT_DIR/$OBJ_SLUG"
mkdir -p "$CONV_FOLDER"

# Base filename for chunks (without folder path in name, folder is the organization)
BASE_FILENAME="${FILE_DATE}_${PLATFORM}"
```

### 6. Chunk Conversation into Files

Split the conversation into chunks of maximum 3000 lines each and store them in the organized folder:

```bash
# Count total lines
TOTAL_LINES=$(wc -l < "$LAST_CONV" | tr -d ' ')

# Calculate number of chunks needed
CHUNKS_NEEDED=$(( (TOTAL_LINES + MAX_LINES_PER_CHUNK - 1) / MAX_LINES_PER_CHUNK ))

# Split into chunks (files stored in CONV_FOLDER created in step 5)
if [ "$TOTAL_LINES" -le "$MAX_LINES_PER_CHUNK" ]; then
  # Single file
  OUTPUT_FILE="$CONV_FOLDER/${BASE_FILENAME}.md"
  cp "$LAST_CONV" "$OUTPUT_FILE"
  echo "✅ Created: $OUTPUT_FILE"
else
  # Multiple chunks
  CHUNK_NUM=1
  LINE_START=1

  while [ "$LINE_START" -le "$TOTAL_LINES" ]; do
    LINE_END=$((LINE_START + MAX_LINES_PER_CHUNK - 1))
    if [ "$LINE_END" -gt "$TOTAL_LINES" ]; then
      LINE_END=$TOTAL_LINES
    fi

    if [ "$CHUNKS_NEEDED" -eq 1 ]; then
      OUTPUT_FILE="$CONV_FOLDER/${BASE_FILENAME}.md"
    else
      OUTPUT_FILE="$CONV_FOLDER/${BASE_FILENAME}_part${CHUNK_NUM}.md"
    fi

    sed -n "${LINE_START},${LINE_END}p" "$LAST_CONV" > "$OUTPUT_FILE"

    # Add chunk header if multiple chunks
    if [ "$CHUNKS_NEEDED" -gt 1 ]; then
      HEADER="# Part $CHUNK_NUM of $CHUNKS_NEEDED\n\n*This conversation has been split into $CHUNKS_NEEDED parts for readability.*\n\n---\n\n"
      echo -e "$HEADER$(cat "$OUTPUT_FILE")" > "$OUTPUT_FILE"
    fi

    echo "✅ Created: $OUTPUT_FILE (lines $LINE_START-$LINE_END)"

    LINE_START=$((LINE_END + 1))
    CHUNK_NUM=$((CHUNK_NUM + 1))
  done
fi
```

### 7. Add Metadata Header

Add metadata to each created file in the conversation folder:

```bash
# Add metadata header to each file in the conversation folder
for FILE in "$CONV_FOLDER/${BASE_FILENAME}"*.md; do
  if [ -f "$FILE" ]; then
    METADATA="---
source: $(basename "$LAST_CONV")
platform: $PLATFORM
exported_date: $FILE_DATE
analyzed_date: $(date +%Y-%m-%d)
main_objective: $OBJ_SLUG
total_lines: $TOTAL_LINES
chunks: $CHUNKS_NEEDED
folder: $OBJ_SLUG
---

"
    echo -e "$METADATA$(cat "$FILE")" > "$FILE"
  fi
done
```

### 8. Create Summary

Output summary of what was created:

```bash
echo ""
echo "📊 Conversation Import Summary"
echo "================================"
echo "Source: $(basename "$LAST_CONV")"
echo "Platform: $PLATFORM"
echo "Total Lines: $TOTAL_LINES"
echo "Chunks Created: $CHUNKS_NEEDED"
echo "Main Objective: $OBJ_SLUG"
echo "Conversation Folder: $CONV_FOLDER"
echo ""
echo "Files created:"
ls -lh "$CONV_FOLDER/${BASE_FILENAME}"*.md
```

## Usage Examples

**Note**: These are slash commands used in AI agent prompt interfaces, NOT bash terminal commands.

```
# Basic usage (uses default ~/Downloads)
/imco_import_conversation_chunknizing

# Specify custom download folder
/imco_import_conversation_chunknizing /path/to/exports

# The command will automatically:
# 1. Find the most recent cursor_*.md or dadosfera_*.md file
# 2. Analyze it to extract a meaningful, descriptive main objective
# 3. Create a folder: docs/conversations/{objective_slug}/
# 4. Chunk it into files of max 3000 lines
# 5. Save chunks to the organized folder with descriptive names
```

## Constraints

### Must Do
- Verify repository context before proceeding
- Find the most recent exported conversation (cursor or dadosfera)
- Analyze conversation to extract meaningful, descriptive main objective (not generic names)
- Create a folder structure: `docs/conversations/{objective_slug}/` to organize conversation chunks
- Store all chunks for a conversation in its dedicated folder
- Chunk files exceeding 3000 lines
- Create descriptive filenames based on objective
- Add metadata headers to all created files
- Create `docs/conversations/` directory if it doesn't exist

### Must Not Do
- Do not modify the original exported conversation file
- Do not create files without analyzing the main objective first
- Do not skip chunking for large files (>3000 lines)
- Do not use generic names like "conversation_001.md"

## Output Format

Each created file will have:
1. **YAML frontmatter** with metadata:
   - source: original filename
   - platform: cursor or dadosfera
   - exported_date: date from original file
   - analyzed_date: current date
   - main_objective: descriptive slug
   - total_lines: total lines in conversation
   - chunks: number of chunks created

2. **Chunk header** (if multiple chunks):
   - Part number and total parts
   - Note about splitting

3. **Original conversation content**

## File Naming Convention

**Folder Structure:**
- Conversations are organized in folders: `docs/conversations/{objective_slug}/`
- Each conversation gets its own folder based on the main objective
- This keeps related chunks together and prevents directory clutter

**File Naming:**
- Format: `YYYY-MM-DD_{platform}_part{N}.md` (stored inside the objective folder)
- The folder name contains the objective slug, so filenames are simpler

**Examples:**
- Folder: `docs/conversations/legal_terms_privacy_policy_analysis/`
  - Files: `2026-01-16_cursor.md` (single file)
- Folder: `docs/conversations/exported_conversation_processing_command_creation/`
  - Files: `2026-01-16_cursor_part1.md`, `2026-01-16_cursor_part2.md`, etc. (multiple chunks)

## Reference

For related workflows, see:
- `commands/arch_archive.md` - Archive conversations and create plans
- `_dev/conversations/README.md` - Conversation documentation structure

---
**Local Reference**: `commands/imco_import_conversation_chunknizing.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/imco_import_conversation_chunknizing.md`

End Command ---
