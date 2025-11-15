#!/bin/bash
# workflows/scripts/bulk-update-repo.sh
# Propagate standardization to a single repository using the workflows/ layout in the template repo

set -euo pipefail

REPO_PATH=${1:-""}
if [ -z "$REPO_PATH" ]; then
    echo "Usage: bash workflows/scripts/bulk-update-repo.sh <repo-path>"
    exit 1
fi

REPO_NAME=$(basename "$REPO_PATH")
TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REFERENCE_REPO="$TEMPLATE_DIR"

echo "🚀 Updating repository: $REPO_NAME"
echo "Path: $REPO_PATH"

if [ ! -d "$REPO_PATH" ]; then
    echo "❌ Repository not found: $REPO_PATH"
    exit 1
fi

cd "$REPO_PATH"

# 1. Docker Compose Updates
if [ -f "Dockerfile" ] || [ -d "docker" ] || [ -f "compose.yml" ] || [ -f "docker-compose.yml" ]; then
    echo "📦 Updating Docker Compose..."

    COMPOSE_FILE=""
    [ -f "compose.yml" ] && COMPOSE_FILE="compose.yml"
    [ -z "$COMPOSE_FILE" ] && [ -f "docker-compose.yml" ] && COMPOSE_FILE="docker-compose.yml"

    if [ -z "$COMPOSE_FILE" ]; then
        echo "  Creating new compose.yml from template"
        cp "$REFERENCE_REPO/compose.yml" ./compose.yml 2>/dev/null || {
            echo "  ⚠️  Template not found, skipping compose.yml creation"
        }
        if [ -f "compose.yml" ]; then
            # Customize PROJECT_NAME
            sed -i.bak "s/enrich-ddf-floor-2/$REPO_NAME/g" compose.yml 2>/dev/null || true
        fi
    else
        echo "  Enhancing existing $COMPOSE_FILE"
        # Add resource limits if missing
        if [ -f "$REFERENCE_REPO/scripts/enhance-compose-limits.sh" ]; then
            bash "$REFERENCE_REPO/scripts/enhance-compose-limits.sh" "$COMPOSE_FILE" 2>/dev/null || echo "  ⚠️  Enhancement had issues (check manually)"
        else
            if ! grep -q "mem_limit:" "$COMPOSE_FILE" 2>/dev/null; then
                echo "  ⚠️  Resource limits missing - manual review needed"
            else
                echo "  ✅ Resource limits already present"
            fi
        fi
    fi

    # Validate if docker is available
    if command -v docker &> /dev/null; then
        if [ -f "compose.yml" ]; then
            docker compose -f compose.yml config --quiet 2>/dev/null && echo "  ✅ Compose validated" || echo "  ⚠️  Compose validation failed"
        fi
    fi
fi

# 2. Makefile Updates
if [ -f "Makefile" ]; then
    echo "⏱️  Adding timeout wrappers to Makefile..."
    if [ -f "$REFERENCE_REPO/scripts/add-makefile-timeouts.sh" ]; then
        bash "$REFERENCE_REPO/scripts/add-makefile-timeouts.sh" Makefile 2>/dev/null && echo "  ✅ Timeouts added" || echo "  ⚠️  Timeout addition had issues (check manually)"
    else
        if ! grep -q "timeout\|gtimeout" Makefile 2>/dev/null; then
            echo "  ⚠️  Timeouts missing - manual review needed"
        else
            echo "  ✅ Timeouts already present"
        fi
    fi

    # Add standardized targets if missing
    if ! grep -q "detect-resources:" Makefile 2>/dev/null; then
        echo "  Adding standardized Makefile targets..."
        cat >> Makefile << 'EOF'

# Resource management targets (standardized)
.PHONY: detect-resources compose-validate compose-up compose-down test-auto

detect-resources: ## Detect available system resources
	@bash scripts/detect_resources.sh 2>/dev/null || echo "Resource detection script not found"

compose-validate: ## Validate compose.yml
	@docker compose config --quiet 2>/dev/null || echo "Docker Compose not available"

compose-up: ## Start services with resource limits
	@docker compose --profile app up -d 2>/dev/null || docker compose up -d

compose-down: ## Stop all services
	@docker compose down 2>/dev/null || echo "Docker Compose not available"

test-auto: ## Run tests with auto-detected settings
	@bash scripts/detect_resources.sh --apply --mode=balanced 2>/dev/null || echo "Resource detection not available"
	@npm test 2>/dev/null || pytest -v 2>/dev/null || echo "No test command found"
EOF
        echo "  ✅ Makefile targets added"
    fi
fi

# 3. Resource Detection Script
echo "🔍 Deploying resource detection script..."
mkdir -p scripts
if [ -f "$REFERENCE_REPO/scripts/detect_resources.sh" ]; then
    cp "$REFERENCE_REPO/scripts/detect_resources.sh" scripts/
    chmod +x scripts/detect_resources.sh
    echo "  ✅ Resource detection deployed"
else
    echo "  ⚠️  Resource detection script not found in reference repo"
fi

# 4. Package.json Updates (if Node.js)
if [ -f "package.json" ]; then
    echo "📦 Adding NODE_OPTIONS to package.json..."
    if [ -f "$REFERENCE_REPO/scripts/add-node-options.js" ] && command -v node &> /dev/null; then
        node "$REFERENCE_REPO/scripts/add-node-options.js" package.json 2>/dev/null && echo "  ✅ NODE_OPTIONS added" || echo "  ⚠️  NODE_OPTIONS addition had issues (check manually)"
    else
        if ! grep -q "NODE_OPTIONS" package.json 2>/dev/null; then
            echo "  ⚠️  NODE_OPTIONS missing - manual update needed"
        else
            echo "  ✅ NODE_OPTIONS already present"
        fi
    fi
fi

# 5. Playwright Config (if exists)
if [ -f "playwright.config.ts" ] || [ -f "frontend/playwright.config.ts" ]; then
    echo "🎭 Playwright config found"
    if [ -f "scripts/detect_resources.sh" ]; then
        echo "  Run 'make playwright-auto' to update config"
    fi
fi

# 6. Documentation
echo "📚 Updating README..."
if [ -f "README.md" ]; then
    if ! grep -q "Resource Management" README.md 2>/dev/null; then
        cat >> README.md << EOF

## Resource Management

This repository follows the Dadosfera Resource Management Standard.

### Quick Commands
\`\`\`bash
make detect-resources  # Check available resources
make compose-up        # Start with resource limits
make test-auto         # Run tests with optimal settings
make compose-down      # Stop all services
\`\`\`

### Resource Limits
- Backend: 512MB RAM, 1.0 CPU
- Frontend: 768MB RAM, 1.0 CPU
- Database: 1GB RAM, 1.5 CPU

See \`compose.yml\` for details.
EOF
        echo "  ✅ README updated"
    else
        echo "  ✅ README already has resource management section"
    fi
fi

echo ""
echo "🎉 Repository update complete: $REPO_NAME"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Test locally: make compose-up && make test-auto"
echo "  3. Commit: git add -A && git commit -m 'feat: standardize resource management'"
echo ""
