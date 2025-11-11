#!/bin/bash
# Validate core directory structure
REQUIRED_DIRS=(
  "config"
  "docs"
  "logs"
  "scripts"
  "src"
  "tests"
  "workflows"
  ".cursor"
)

# Optional directories (present in some repos like scripts-fera)
OPTIONAL_DIRS=(
  "docs-fera"
)


for dir in "${REQUIRED_DIRS[@]}"; do
  if [[ ! -d "$dir" ]]; then
    echo "❌ Required directory missing: $dir"
    exit 1
  fi
done

# Prevent direct modifications to critical files
PROTECTED_FILES=(
  ".gitignore"
  ".gitmodules"
  "LICENSE"
  "README.md"
  "package.json"
  ".pre-commit-config.yaml"
)

# Optional directories (present in some repos like scripts-fera)
OPTIONAL_DIRS=(
  "docs-fera"
)


for file in "${PROTECTED_FILES[@]}"; do
  if git diff --cached --name-only | grep -q "^$file$"; then
    echo "❌ Protected file $file cannot be directly modified"
    exit 1
  fi
done

# Ensure no unauthorized files in root
ROOT_FILES=$(find . -maxdepth 1 -type f | grep -v "^\./\.git" | grep -v "^\./\.pre-commit-config\.yaml$")
if [[ -n "$ROOT_FILES" ]]; then
  echo "❌ Unauthorized files in project root:"
  echo "$ROOT_FILES"
  exit 1
fi

# Validate directory naming conventions
INVALID_DIRS=$(find . -type d \( -name "*-copy" -o -name "*-backup" -o -name "*-partial" \))
if [[ -n "$INVALID_DIRS" ]]; then
  echo "❌ Invalid directory names detected:"
  echo "$INVALID_DIRS"
  exit 1
fi


# Check optional directories (log but don't fail)
for dir in "${OPTIONAL_DIRS[@]}"; do
  if [[ ! -d "$dir" ]]; then
    echo "⚠️  Optional directory not found: $dir (some repos may not have this)"
  fi
done

exit 0

