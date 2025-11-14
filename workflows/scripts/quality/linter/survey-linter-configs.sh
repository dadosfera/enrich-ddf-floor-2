#!/bin/bash
# Survey all linter configurations across local repos

set -e

SURVEY_OUTPUT="active/linter-config-survey-$(date +%Y%m%d_%H%M%S).json"
REPO_BASE="$HOME/local_repos"

echo "🔍 Surveying linter configurations across local repos..."
echo "Output: $SURVEY_OUTPUT"

# Initialize JSON output
echo "{" > "$SURVEY_OUTPUT"
echo "  \"survey_date\": \"$(date -Iseconds)\"," >> "$SURVEY_OUTPUT"
echo "  \"repos\": [" >> "$SURVEY_OUTPUT"

first=true
repo_count=0
python_count=0
js_count=0
precommit_count=0

for repo in "$REPO_BASE"/*/; do
    if [ ! -d "$repo" ]; then
        continue
    fi

    repo_name=$(basename "$repo")
    repo_path="$repo"

    # Skip if not a git repo
    if [ ! -d "$repo/.git" ]; then
        continue
    fi

    repo_count=$((repo_count + 1))

    # Check for Python linter configs
    has_pyproject=false
    has_ruff=false
    has_pylint=false
    has_mypy=false

    if [ -f "$repo/pyproject.toml" ]; then
        has_pyproject=true
        python_count=$((python_count + 1))

        if grep -q "\[tool.ruff" "$repo/pyproject.toml" 2>/dev/null; then
            has_ruff=true
        fi
        if grep -q "\[tool.pylint" "$repo/pyproject.toml" 2>/dev/null; then
            has_pylint=true
        fi
        if grep -q "\[tool.mypy" "$repo/pyproject.toml" 2>/dev/null; then
            has_mypy=true
        fi
    fi

    # Check for JavaScript linter configs
    has_eslint=false
    has_prettier=false

    if [ -f "$repo/.eslintrc.json" ] || [ -f "$repo/.eslintrc.js" ] || [ -f "$repo/.eslintrc.yaml" ]; then
        has_eslint=true
        js_count=$((js_count + 1))
    fi

    if [ -f "$repo/.prettierrc" ] || [ -f "$repo/.prettierrc.json" ] || grep -q "prettier" "$repo/package.json" 2>/dev/null; then
        has_prettier=true
    fi

    # Check for pre-commit configs
    has_precommit=false
    if [ -f "$repo/.pre-commit-config.yaml" ]; then
        has_precommit=true
        precommit_count=$((precommit_count + 1))
    fi

    # Write repo data
    if [ "$first" = false ]; then
        echo "," >> "$SURVEY_OUTPUT"
    fi
    first=false

    echo "    {" >> "$SURVEY_OUTPUT"
    echo "      \"name\": \"$repo_name\"," >> "$SURVEY_OUTPUT"
    echo "      \"path\": \"$repo_path\"," >> "$SURVEY_OUTPUT"
    echo "      \"has_pyproject\": $has_pyproject," >> "$SURVEY_OUTPUT"
    echo "      \"has_ruff\": $has_ruff," >> "$SURVEY_OUTPUT"
    echo "      \"has_pylint\": $has_pylint," >> "$SURVEY_OUTPUT"
    echo "      \"has_mypy\": $has_mypy," >> "$SURVEY_OUTPUT"
    echo "      \"has_eslint\": $has_eslint," >> "$SURVEY_OUTPUT"
    echo "      \"has_prettier\": $has_prettier," >> "$SURVEY_OUTPUT"
    echo "      \"has_precommit\": $has_precommit" >> "$SURVEY_OUTPUT"
    echo -n "    }" >> "$SURVEY_OUTPUT"
done

echo "" >> "$SURVEY_OUTPUT"
echo "  ]," >> "$SURVEY_OUTPUT"
echo "  \"summary\": {" >> "$SURVEY_OUTPUT"
echo "    \"total_repos\": $repo_count," >> "$SURVEY_OUTPUT"
echo "    \"python_configs\": $python_count," >> "$SURVEY_OUTPUT"
echo "    \"js_configs\": $js_count," >> "$SURVEY_OUTPUT"
echo "    \"precommit_configs\": $precommit_count" >> "$SURVEY_OUTPUT"
echo "  }" >> "$SURVEY_OUTPUT"
echo "}" >> "$SURVEY_OUTPUT"

echo "✅ Survey complete!"
echo "📊 Summary:"
echo "   Total repos: $repo_count"
echo "   Python configs: $python_count"
echo "   JS configs: $js_count"
echo "   Pre-commit configs: $precommit_count"
echo "📄 Results saved to: $SURVEY_OUTPUT"
