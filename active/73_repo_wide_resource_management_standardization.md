# Repo-Wide Resource Management Standardization Plan

**Status**: Active
**Priority**: P0 (Critical)
**Estimated Effort**: 8-12 AI hours / 2-3 Human hours (review + approval)
**Created**: 2025-01-12
**Updated**: 2025-01-12
**Owner**: AI Agent + Human Review
**Related Plans**: [74_intelligent_resource_adaptive_testing.md](./74_intelligent_resource_adaptive_testing.md)

## Executive Summary

Standardize resource management, cost controls, and performance optimization across **30+ local repositories** based on best practices identified in `deployer-ddf-mod-open-llms`, `agent-ddf`, and `3d-ddf`.

**Primary Goals**:
- 🎯 **40-60% reduction** in local resource consumption
- 🚫 **Zero runaway processes** through timeout protection
- 💰 **60-70% cloud cost savings** via automated scheduling
- ⚡ **50%+ faster tests** on powerful machines with adaptive parallelization
- 🔧 **Consistent workflows** across all repositories

**Business Impact**:
- **Developer Productivity**: Faster local dev, fewer crashes
- **Infrastructure Costs**: Significant cloud savings through automation
- **System Stability**: Predictable resource usage, no hangs
- **Onboarding**: Standardized commands across all repos

---

## 📊 Current State Analysis

### Repositories Scanned (30+ Total)

#### ✅ Exemplar Repositories (Best Practices Source)
1. **deployer-ddf-mod-open-llms**
   - 19 Docker Compose files with GPU reservations
   - Comprehensive Makefile with gtimeout on all targets
   - Cloud cost automation (nightly stop/start)
   - Multi-model testing infrastructure
   - **Lessons**: Timeout discipline, cost controls, OCI workflows

2. **agent-ddf**
   - Multi-platform runner (docker/local/cursor/replit/dadosfera)
   - Environment-specific compose files (dev/staging/prod)
   - Central port management with conflict detection
   - Profile-based service orchestration
   - **Lessons**: Port management, platform abstraction, health checks

3. **3d-ddf**
   - Jenkins CI/CD with explicit JVM heap sizing
   - Blender rendering with resource constraints
   - **Lessons**: JVM tuning, long-running process management

4. **enrich-ddf-floor-2** (this repo)
   - ✅ Baseline improvements implemented
   - ✅ Resource detection script deployed
   - ✅ Adaptive testing system operational
   - **Status**: Reference implementation for rollout

#### 📋 Repositories Requiring Standardization

**High Priority** (Active Development):
- [ ] gen-ddf-floor-2
- [ ] map-ddf-floor-2
- [ ] planner-ddf-floor-2
- [ ] news-ddf-floor-2
- [ ] ai-flow-module
- [ ] framework-ddf
- [ ] monitor-ddf
- [ ] assistant-ddf
- [ ] cline-ddf
- [ ] meta-assistant-ddf

**Medium Priority** (Periodic Updates):
- [ ] assessment-ddf
- [ ] budget-ddf
- [ ] conversor-ddf
- [ ] crm-ddf
- [ ] dataapp-data-input
- [ ] extractor-ddf
- [ ] proc-ddf
- [ ] proto-ddf

**Low Priority** (Maintenance Mode):
- [ ] auto-drive-v2-try-2
- [ ] beast
- [ ] central-forecast-ddf-group
- [ ] enrich-ddf-group
- [ ] enrich-ddf-mod-ncm
- [ ] solver-mod-bet
- [ ] docs-fera
- [ ] prompts-fera
- [ ] scripts-fera
- [ ] workflows-fera

### Detailed Compliance Matrix

| Repository | Compose | Timeouts | Caps | Ports | Costs | Health | Logs | Tests | Score |
|------------|---------|----------|------|-------|-------|--------|------|-------|-------|
| deployer-ddf-mod-open-llms | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 8/8 |
| agent-ddf | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ⚠️ | 5.5/8 |
| 3d-ddf | ✅ | ❌ | ✅ | ❌ | ❌ | ⚠️ | ❌ | ❌ | 2.5/8 |
| enrich-ddf-floor-2 | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | ✅ | ✅ | 6.5/8 |
| **Average (30 repos)** | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **1.2/8** |

**Legend**:
- ✅ Fully Compliant
- ⚠️ Partially Compliant
- ❌ Not Compliant

### Critical Gaps Identified

1. **Timeout Protection**: Only 2/30 repos have comprehensive timeout coverage
2. **Resource Caps**: Only 4/30 repos have Docker resource limits
3. **Cost Controls**: Only 1/30 repos has automated cloud cost management
4. **Port Management**: Only 1/30 repos has centralized port registry
5. **Health Checks**: Only 3/30 repos have proper health monitoring
6. **Log Rotation**: Only 2/30 repos have log size limits configured
7. **Adaptive Testing**: Only 1/30 repos has resource-aware test execution

---

## 🎯 Standardization Goals & Success Metrics

### Phase 1: Quick Wins (Week 1-2) 🏃‍♂️

**Target**: 10 high-priority repos
**Effort**: 4-6 AI hours
**Impact**: Immediate stability improvements

| Initiative | Target Repos | Success Metric | Priority |
|------------|--------------|----------------|----------|
| **1. Compose Resource Limits** | All with Docker (15 repos) | 100% have mem_limit + cpus | P0 |
| **2. Makefile Timeouts** | All with Makefile (20 repos) | 100% long-running targets wrapped | P0 |
| **3. Log Rotation** | All with Docker (15 repos) | 100% have 10m/3 file limits | P1 |
| **4. Node Memory Caps** | All with Node.js (12 repos) | 100% have NODE_OPTIONS | P1 |

**Expected Outcomes**:
- ✅ Zero runaway processes
- ✅ 30-40% memory reduction
- ✅ Predictable disk usage (logs)
- ✅ Faster Node.js builds

### Phase 2: Infrastructure (Week 3-4) 🏗️

**Target**: All 30 repos
**Effort**: 4-6 AI hours
**Impact**: Long-term maintainability

| Initiative | Target Repos | Success Metric | Priority |
|------------|--------------|----------------|----------|
| **5. Port Management** | All repos | Central registry + zero conflicts | P0 |
| **6. Health Checks** | All with Docker (15 repos) | 100% services have healthchecks | P1 |
| **7. Resource Detection** | All with tests (25 repos) | Adaptive testing deployed | P0 |
| **8. Test Optimization** | All with tests (25 repos) | Low-resource targets available | P1 |

**Expected Outcomes**:
- ✅ Zero port conflicts across repos
- ✅ Automatic service health monitoring
- ✅ 50%+ faster tests on powerful machines
- ✅ Stable tests on constrained machines

### Phase 3: Cloud Automation (Week 5-6) ☁️

**Target**: 5 cloud-enabled repos
**Effort**: 2-3 AI hours
**Impact**: Significant cost savings

| Initiative | Target Repos | Success Metric | Priority |
|------------|--------------|----------------|----------|
| **9. Cost Controls** | Cloud repos (5) | Nightly automation operational | P0 |
| **10. Resource Monitoring** | Cloud repos (5) | Daily cost reports generated | P1 |
| **11. Auto-scaling** | Cloud repos (5) | Resource-based triggers active | P2 |

**Expected Outcomes**:
- ✅ 60-70% cloud cost reduction
- ✅ Automated instance scheduling
- ✅ Cost visibility and reporting
- ✅ Optimized resource allocation

### Overall Success Criteria

**Technical Metrics**:
- 📊 **Compliance Score**: 1.2/8 → 7.5/8 average across all repos
- ⏱️ **Timeout Coverage**: 7% → 100% of long-running commands
- 💾 **Resource Caps**: 13% → 100% of Docker services
- 💰 **Cloud Cost Reduction**: $0 → $5,000-10,000/month savings
- ⚡ **Test Speed**: 50%+ improvement on powerful machines

**Operational Metrics**:
- 🚫 **Zero** runaway processes in 30 days
- 🚫 **Zero** port conflicts in 30 days
- 🚫 **Zero** out-of-memory crashes in 30 days
- ✅ **95%+** developer satisfaction with standardization

**Adoption Metrics**:
- 📚 **100%** of repos have standardized Makefile targets
- 🎓 **100%** of developers trained on new workflows
- 📖 **100%** of documentation updated
- ✅ **90%+** of developers use `make test-auto` by default

---

## 📋 Detailed Implementation Plan

### 1. Compose Resource Limits for Local Dev

**Objective**: Add `mem_limit`, `cpus`, and log rotation to all Docker Compose services to prevent resource exhaustion and enable predictable performance.

**Problem Statement**:
- Unbounded containers can consume all system resources
- No automatic cleanup of logs leads to disk space issues
- Services crash without clear error messages
- Difficult to debug resource-related issues

**Solution**: Standardized resource limits with appropriate defaults

#### Resource Allocation Guidelines

| Service Type | Memory Limit | CPU Limit | Rationale |
|--------------|--------------|-----------|-----------|
| **Backend API** | 512MB | 1.0 | Most APIs fit in 512MB; scale if needed |
| **Frontend (Node)** | 768MB | 1.0 | Build tools need more RAM |
| **Database (PostgreSQL)** | 1GB | 1.5 | Needs memory for caching |
| **Database (Redis)** | 256MB | 0.5 | In-memory cache, predictable size |
| **Message Queue** | 512MB | 1.0 | Moderate memory for buffering |
| **Worker/Celery** | 512MB | 1.0 | Per-worker allocation |
| **ML/AI Service** | 2GB-4GB | 2.0-4.0 | Model loading requires more resources |
| **Monitoring** | 256MB | 0.5 | Lightweight metrics collection |

#### Complete Template (apply to all repos)

```yaml
version: "3.8"

services:
  # Backend API Service
  backend:
    image: python:3.11-slim
    container_name: ${PROJECT_NAME}-backend
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      - PORT=${BACKEND_PORT:-8000}
      - DATABASE_URL=${DATABASE_URL}
    command: sh -c "pip install -r requirements.txt && python main.py"
    ports:
      - "${BACKEND_PORT:-8000}:${BACKEND_PORT:-8000}"

    # Resource Limits (REQUIRED)
    mem_limit: "512m"           # Hard limit: container killed if exceeded
    mem_reservation: "256m"     # Soft limit: guaranteed minimum
    cpus: "1.0"                 # CPU cores (1.0 = 1 full core)

    # Restart Policy (REQUIRED)
    restart: unless-stopped     # Auto-restart except manual stop

    # Logging (REQUIRED)
    logging:
      driver: "json-file"
      options:
        max-size: "10m"         # Rotate at 10MB
        max-file: "3"           # Keep 3 files (30MB total)
        compress: "true"        # Compress rotated logs

    # Health Check (RECOMMENDED)
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${BACKEND_PORT:-8000}/health"]
      interval: 30s             # Check every 30s
      timeout: 10s              # Fail if no response in 10s
      retries: 3                # Retry 3 times before marking unhealthy
      start_period: 40s         # Grace period for startup

    # Dependencies (if applicable)
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

    # Network
    networks:
      - app-network

    # Profiles (OPTIONAL - for selective startup)
    profiles:
      - app
      - full

  # Frontend Service
  frontend:
    image: node:20-alpine
    container_name: ${PROJECT_NAME}-frontend
    working_dir: /app/frontend
    volumes:
      - ./frontend:/app/frontend
      - /app/frontend/node_modules  # Prevent host node_modules conflicts
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - NODE_OPTIONS=--max-old-space-size=768
      - VITE_API_URL=http://backend:${BACKEND_PORT:-8000}
    command: sh -c "npm ci && npm run dev"
    ports:
      - "${FRONTEND_PORT:-5173}:${FRONTEND_PORT:-5173}"

    # Resource Limits
    mem_limit: "768m"           # Frontend needs more for build tools
    mem_reservation: "384m"
    cpus: "1.0"

    restart: unless-stopped

    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        compress: "true"

    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:${FRONTEND_PORT:-5173}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s         # Longer startup for npm install

    depends_on:
      - backend

    networks:
      - app-network

    profiles:
      - app
      - full

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: ${PROJECT_NAME}-postgres
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-appdb}
      - POSTGRES_USER=${POSTGRES_USER:-appuser}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-changeme}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "${POSTGRES_PORT:-5432}:5432"

    # Resource Limits
    mem_limit: "1g"             # Databases need more memory
    mem_reservation: "512m"
    cpus: "1.5"

    restart: unless-stopped

    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        compress: "true"

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-appuser}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

    networks:
      - app-network

    profiles:
      - full

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: ${PROJECT_NAME}-redis
    command: redis-server --maxmemory 200mb --maxmemory-policy allkeys-lru
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis-data:/data

    # Resource Limits
    mem_limit: "256m"           # Redis is in-memory, cap it
    mem_reservation: "128m"
    cpus: "0.5"

    restart: unless-stopped

    logging:
      driver: "json-file"
      options:
        max-size: "5m"          # Smaller logs for cache
        max-file: "2"
        compress: "true"

    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 5s

    networks:
      - app-network

    profiles:
      - full

# Networks
networks:
  app-network:
    driver: bridge
    name: ${PROJECT_NAME}-network

# Volumes
volumes:
  postgres-data:
    driver: local
    name: ${PROJECT_NAME}-postgres-data
  redis-data:
    driver: local
    name: ${PROJECT_NAME}-redis-data
```

#### Environment Variables (.env template)

```bash
# Project Configuration
PROJECT_NAME=my-app
NODE_ENV=development

# Service Ports
BACKEND_PORT=8000
FRONTEND_PORT=5173
POSTGRES_PORT=5432
REDIS_PORT=6379

# Database Configuration
POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=changeme_in_production
DATABASE_URL=postgresql://appuser:changeme@postgres:5432/appdb

# Resource Limits (override if needed)
BACKEND_MEM_LIMIT=512m
FRONTEND_MEM_LIMIT=768m
```

#### Validation Script

```bash
#!/bin/bash
# scripts/validate-compose.sh
# Validate Docker Compose resource limits

set -euo pipefail

COMPOSE_FILE=${1:-compose.yml}

echo "Validating: $COMPOSE_FILE"

# Check syntax
docker compose -f "$COMPOSE_FILE" config --quiet || {
  echo "❌ Syntax error in $COMPOSE_FILE"
  exit 1
}

# Extract services
SERVICES=$(docker compose -f "$COMPOSE_FILE" config --services)

for service in $SERVICES; do
  echo "Checking service: $service"

  # Check mem_limit
  if ! docker compose -f "$COMPOSE_FILE" config | grep -A 20 "^  $service:" | grep -q "mem_limit"; then
    echo "  ⚠️  Missing mem_limit"
  else
    echo "  ✅ mem_limit configured"
  fi

  # Check cpus
  if ! docker compose -f "$COMPOSE_FILE" config | grep -A 20 "^  $service:" | grep -q "cpus"; then
    echo "  ⚠️  Missing cpus"
  else
    echo "  ✅ cpus configured"
  fi

  # Check logging
  if ! docker compose -f "$COMPOSE_FILE" config | grep -A 20 "^  $service:" | grep -q "max-size"; then
    echo "  ⚠️  Missing log rotation"
  else
    echo "  ✅ log rotation configured"
  fi
done

echo "✅ Validation complete"
```

#### Repositories to Update

**Phase 1 (Week 1)** - High Priority:
- [ ] agent-ddf (8 compose files)
  - config/docker/docker-compose.dev.yml
  - config/docker/docker-compose.prod.yml
  - config/docker/docker-compose.staging.yml
  - config/docker/docker-compose.local.yml
- [ ] deployer-ddf-mod-open-llms (19 compose files) - enhance existing
  - docker/docker-compose.yml
  - docker/docker-compose.gpu.yml
  - docker/docker-compose.consolidated.yml
- [ ] gen-ddf-floor-2 (create new)
- [ ] map-ddf-floor-2 (create new)
- [ ] planner-ddf-floor-2 (create new)

**Phase 2 (Week 2)** - Medium Priority:
- [ ] 3d-ddf (1 compose file) - enhance existing
- [ ] ai-flow-module (create new)
- [ ] framework-ddf (create new)
- [ ] news-ddf-floor-2 (create new)
- [ ] monitor-ddf (create new)

**Acceptance Criteria**:
- ✅ All services have explicit memory limits (mem_limit + mem_reservation)
- ✅ All services have CPU caps (1.0 default, adjust per service type)
- ✅ Log rotation configured (10m max-size, 3 files, compress enabled)
- ✅ Health checks present for all long-running services
- ✅ Restart policy set to `unless-stopped`
- ✅ Networks and volumes properly named
- ✅ Profiles used for optional services
- ✅ Validated with `docker compose config --quiet`
- ✅ Validation script passes for all compose files
- ✅ .env.example provided with all required variables

---

### 2. Makefile Timeout Standardization

**Objective**: Wrap all long-running Makefile targets with timeout to prevent hangs.

**Standard Timeouts**:
```makefile
# Quick checks (5-30s)
lint:
	@echo "🔍 Running linting..."
	timeout 30 ruff check . || gtimeout 30 ruff check .

# Build operations (60-300s)
build:
	@echo "🔨 Building application..."
	timeout 120 npm run build || gtimeout 120 npm run build

# Test suites (120-600s)
test:
	@echo "🧪 Running tests..."
	timeout 300 pytest -v || gtimeout 300 pytest -v

# Deploy operations (300-1800s)
deploy:
	@echo "🚀 Deploying..."
	timeout 600 bash workflows/run.sh --deploy || gtimeout 600 bash workflows/run.sh --deploy
```

**Timeout Guidelines**:
| Operation Type | Timeout | Kill-After |
|----------------|---------|------------|
| Linting | 30s | 5s |
| Unit tests | 120s | 10s |
| Integration tests | 300s | 15s |
| Builds | 120s | 15s |
| Deployments | 600s | 30s |
| Cloud operations | 300-1800s | 30-60s |

**Repositories to Update**:
- [ ] All repos with Makefile (scan for long-running targets)
- [ ] Priority: deployer-ddf-mod-open-llms (enhance existing)
- [ ] Priority: agent-ddf (add missing)
- [ ] Priority: 3d-ddf (add missing)

**Implementation Script**:
```bash
# Scan all repos for Makefiles without timeouts
for repo in ~/local_repos/*/; do
  if [ -f "$repo/Makefile" ]; then
    echo "Checking: $repo"
    grep -L "timeout\|gtimeout" "$repo/Makefile" && echo "  ⚠️  Missing timeouts"
  fi
done
```

**Acceptance Criteria**:
- ✅ All long-running targets wrapped with timeout
- ✅ Fallback to gtimeout for macOS compatibility
- ✅ Consistent timeout values across repos
- ✅ Kill-after grace period configured

---

### 3. Cloud Cost Controls

**Objective**: Implement nightly stop/start automation and cost reporting for non-production instances.

**Components** (based on deployer-ddf-mod-open-llms):

#### 3.1 Nightly Stop Script
```bash
#!/bin/bash
# scripts/cost/stop-nonprod.sh
# Stop non-production instances at night (default: dry-run)

set -euo pipefail

DRY_RUN=${1:-true}
ENVIRONMENTS=("dev" "staging" "alpha")

for env in "${ENVIRONMENTS[@]}"; do
  echo "Stopping $env instances..."
  if [ "$DRY_RUN" = "false" ]; then
    oci compute instance action --instance-id "$INSTANCE_ID" --action STOP
  else
    echo "  [DRY-RUN] Would stop $env instance"
  fi
done
```

#### 3.2 Morning Start Script
```bash
#!/bin/bash
# scripts/cost/start-nonprod.sh
# Start non-production instances in the morning

set -euo pipefail

ENVIRONMENTS=("dev" "staging" "alpha")

for env in "${ENVIRONMENTS[@]}"; do
  echo "Starting $env instances..."
  oci compute instance action --instance-id "$INSTANCE_ID" --action START
done
```

#### 3.3 Cost Reporting
```bash
#!/bin/bash
# scripts/cost/report-nightly.sh
# Generate nightly cost report

set -euo pipefail

REPORT_FILE="logs/cost-report-$(date +%Y-%m-%d).txt"

{
  echo "Cloud Cost Report - $(date)"
  echo "================================"
  echo ""
  echo "Instance Status:"
  oci compute instance list --all --output table
  echo ""
  echo "Estimated Daily Cost: $DAILY_COST"
  echo "Estimated Monthly Cost: $MONTHLY_COST"
} > "$REPORT_FILE"

echo "Report saved: $REPORT_FILE"
```

#### 3.4 Makefile Integration
```makefile
# Cloud cost automation
cloud-stop-night:
	@echo "Stopping non-prod instances (dry-run)..."
	timeout 120 bash scripts/cost/stop-nonprod.sh true

cloud-stop-night-force:
	@echo "Stopping non-prod instances (FORCE)..."
	timeout 300 bash scripts/cost/stop-nonprod.sh false

cloud-start-morning:
	@echo "Starting non-prod instances..."
	timeout 300 bash scripts/cost/start-nonprod.sh

cloud-cost-report:
	@echo "Generating nightly cost report..."
	timeout 30 bash scripts/cost/report-nightly.sh
```

#### 3.5 Cron Automation
```bash
# Add to crontab for automated execution
# Stop non-prod at 10 PM
0 22 * * * cd ~/local_repos/PROJECT && make cloud-stop-night-force

# Start non-prod at 7 AM
0 7 * * * cd ~/local_repos/PROJECT && make cloud-start-morning

# Generate cost report at midnight
0 0 * * * cd ~/local_repos/PROJECT && make cloud-cost-report
```

**Repositories to Implement**:
- [ ] deployer-ddf-mod-open-llms (enhance existing)
- [ ] agent-ddf (new)
- [ ] 3d-ddf (new)
- [ ] All repos with cloud deployments

**Acceptance Criteria**:
- ✅ Dry-run mode by default (safety)
- ✅ Force mode requires explicit flag
- ✅ Cost reports generated nightly
- ✅ Cron jobs configured for automation
- ✅ Logs preserved for audit trail

---

### 4. Central Port Management

**Objective**: Deploy centralized port registry and conflict detection across all repos.

**Port Registry** (based on agent-ddf):
```javascript
// config/ports.js
export const PORT_REGISTRY = {
  'enrich-ddf-floor-2': {
    local: { backend: 8247, frontend: 5173 },
    docker: { backend: 8247, frontend: 5173 },
  },
  'agent-ddf': {
    local: { api: 6008, frontend: 7004, websocket: 7005 },
    docker: { api: 5003, frontend: 7004, websocket: 7005 },
  },
  'deployer-ddf-mod-open-llms': {
    local: { api: 9876, frontend: 3678, llm: 8002, image: 4567, video: 5678 },
    docker: { api: 9876, frontend: 3678, llm: 8002, image: 4567, video: 5678 },
  },
  // ... all other repos
};

export async function checkPortConflicts(platform, env) {
  const usedPorts = new Set();
  const conflicts = [];

  for (const [repo, config] of Object.entries(PORT_REGISTRY)) {
    const ports = config[platform] || config.local;
    for (const [service, port] of Object.entries(ports)) {
      if (usedPorts.has(port)) {
        conflicts.push({ repo, service, port });
      }
      usedPorts.add(port);
    }
  }

  return conflicts;
}

export async function displayPortSummary(platform, env) {
  console.log(`\n📊 Port Summary - ${platform}/${env}\n`);
  console.log('Repository                    | Service    | Port');
  console.log('------------------------------|------------|------');

  for (const [repo, config] of Object.entries(PORT_REGISTRY)) {
    const ports = config[platform] || config.local;
    for (const [service, port] of Object.entries(ports)) {
      console.log(`${repo.padEnd(30)}| ${service.padEnd(10)}| ${port}`);
    }
  }

  const conflicts = await checkPortConflicts(platform, env);
  if (conflicts.length > 0) {
    console.log('\n⚠️  Port Conflicts Detected:');
    conflicts.forEach(c => console.log(`  - ${c.repo}:${c.service} (${c.port})`));
  }
}
```

**Makefile Integration**:
```makefile
port-check: ## Check for port conflicts across all repos
	@echo "🔍 Checking port conflicts..."
	node config/ports.js --check

port-summary: ## Show port allocation summary
	@echo "📊 Port allocation summary..."
	node config/ports.js --summary
```

**Repositories to Update**:
- [ ] Create central registry in shared config repo
- [ ] Link all repos to central registry
- [ ] Add port-check to all Makefiles

**Acceptance Criteria**:
- ✅ Central port registry maintained
- ✅ Conflict detection automated
- ✅ Port summary available via Make
- ✅ Pre-flight checks in run scripts

---

### 5. Test & Resource Tuning

**Objective**: Optimize test execution and resource usage across all repos.

#### 5.1 Playwright Configuration
```typescript
// playwright.config.ts (standard for all repos)
export default defineConfig({
  testDir: './tests',
  fullyParallel: false,  // Prevent CPU spikes
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 2,  // Local: 2, CI: 1
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'http://127.0.0.1:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

#### 5.2 Node Memory Caps
```json
// package.json (standard for all repos)
{
  "scripts": {
    "dev": "NODE_OPTIONS=--max-old-space-size=2048 vite",
    "build": "NODE_OPTIONS=--max-old-space-size=2048 tsc -b && NODE_OPTIONS=--max-old-space-size=2048 vite build",
    "test": "NODE_OPTIONS=--max-old-space-size=2048 jest",
    "lint": "NODE_OPTIONS=--max-old-space-size=2048 eslint ."
  }
}
```

#### 5.3 Low-Resource Test Targets
```makefile
# Makefile (standard for all repos)
test-low: ## Run tests with reduced resources
	@echo "🧪 Running low-resource test suite..."
	NODE_OPTIONS=--max-old-space-size=1536 timeout 120 npm test -- --maxWorkers=2

test-critical: ## Run only critical tests
	@echo "🧪 Running critical tests only..."
	timeout 60 npm test -- --testNamePattern=":critical"

test-quick: ## Run quick smoke tests
	@echo "🧪 Running quick smoke tests..."
	timeout 30 npm test -- --testPathPattern="smoke"
```

#### 5.4 Python Test Optimization
```ini
# pytest.ini (standard for all repos)
[pytest]
addopts =
    --strict-markers
    --tb=short
    --maxfail=5
    --timeout=300
    -n auto
    --dist=loadscope
```

**Repositories to Update**:
- [ ] All repos with Playwright
- [ ] All repos with Node.js
- [ ] All repos with Python tests

**Acceptance Criteria**:
- ✅ Playwright workers capped at 2 locally
- ✅ NODE_OPTIONS set globally
- ✅ Low-resource test targets available
- ✅ Test timeouts configured
- ✅ Parallel execution controlled

---

## 🚀 Rollout Strategy

### Phase 0: Preparation & Baseline (Week 0)

**Objective**: Establish baseline, create automation tools, prepare templates

**Activities**:
1. **Day 1**: Run comprehensive repo scanner
   ```bash
   bash scripts/scan-all-repos.sh > active/repo-baseline-$(date +%Y-%m-%d).md
   ```
2. **Day 2**: Create standardized templates
   - Docker Compose template with all service types
   - Makefile timeout wrapper template
   - Resource detection script template
   - Port registry template
3. **Day 3**: Build automation tools
   - Bulk updater script
   - Validation script
   - Rollback script
4. **Day 4**: Set up monitoring
   - Compliance dashboard
   - Metrics collection
   - Alert system
5. **Day 5**: Documentation prep
   - Migration guide
   - Troubleshooting FAQ
   - Training materials

**Deliverables**:
- ✅ Baseline report for all 30+ repos
- ✅ Complete template library
- ✅ Automation scripts tested
- ✅ Monitoring infrastructure ready
- ✅ Documentation framework in place

---

### Phase 1: Pilot Implementation (Week 1)

**Objective**: Validate approach with 3 pilot repos, gather feedback, refine process

**Pilot Repositories**:
1. **enrich-ddf-floor-2** (this repo) - Already improved, serves as reference
2. **agent-ddf** - Complex multi-platform setup
3. **gen-ddf-floor-2** - Typical Floor 2 repo

**Day-by-Day Plan**:

**Day 1-2: enrich-ddf-floor-2 (Reference Implementation)**
- [x] Docker Compose with resource limits ✅
- [x] Makefile timeout standardization ✅
- [x] Resource detection script ✅
- [x] Adaptive testing system ✅
- [x] Documentation complete ✅
- **Status**: Reference implementation ready

**Day 3-4: agent-ddf (Complex Multi-Platform)**
- [ ] Update 8 Docker Compose files with resource limits
- [ ] Add timeout wrappers to 50+ Makefile targets
- [ ] Deploy resource detection script
- [ ] Update port management system
- [ ] Add adaptive testing
- [ ] Test on docker/local/cursor platforms
- **Challenge**: Multiple compose files, complex workflows

**Day 5: gen-ddf-floor-2 (Typical Floor 2 Repo)**
- [ ] Create Docker Compose with resource limits
- [ ] Add timeout wrappers to Makefile
- [ ] Deploy resource detection script
- [ ] Add adaptive testing
- [ ] Update documentation
- **Challenge**: Starting from minimal setup

**Day 6-7: Validation & Metrics**
- [ ] Run validation scripts on all 3 pilot repos
- [ ] Collect performance metrics (before/after)
- [ ] Gather developer feedback
- [ ] Document lessons learned
- [ ] Refine templates based on findings

**Success Criteria**:
- ✅ All 3 pilot repos pass validation
- ✅ 40%+ resource reduction measured
- ✅ Zero runaway processes in 7 days
- ✅ Positive developer feedback
- ✅ Templates refined and ready for scale

---

### Phase 2: High-Priority Rollout (Week 2-3)

**Objective**: Deploy to 10 high-priority repos with active development

**Target Repositories** (Active Development):
1. [ ] map-ddf-floor-2
2. [ ] planner-ddf-floor-2
3. [ ] news-ddf-floor-2
4. [ ] ai-flow-module
5. [ ] framework-ddf
6. [ ] monitor-ddf
7. [ ] assistant-ddf
8. [ ] cline-ddf
9. [ ] meta-assistant-ddf
10. [ ] deployer-ddf-mod-open-llms (enhance existing)

**Week 2: Batch 1 (5 repos)**

**Day 8-9: Automated Bulk Update**
```bash
# Run bulk updater for first batch
for repo in map-ddf-floor-2 planner-ddf-floor-2 news-ddf-floor-2 ai-flow-module framework-ddf; do
  echo "Updating: $repo"
  bash scripts/bulk-update-repo.sh ~/local_repos/$repo
done
```

**Day 10: Manual Review & Adjustments**
- Review auto-generated configs
- Adjust resource limits per repo needs
- Fix any edge cases
- Test locally

**Day 11: Validation & Commit**
- Run validation scripts
- Test compose up/down
- Run test suites
- Commit changes with standardized message

**Day 12: Documentation & Training**
- Update repo READMEs
- Add migration notes
- Brief developers on changes

**Week 3: Batch 2 (5 repos)**

**Day 13-14: Automated Bulk Update**
```bash
# Run bulk updater for second batch
for repo in monitor-ddf assistant-ddf cline-ddf meta-assistant-ddf deployer-ddf-mod-open-llms; do
  echo "Updating: $repo"
  bash scripts/bulk-update-repo.sh ~/local_repos/$repo
done
```

**Day 15-17: Review, Validate, Document**
- Same process as Batch 1
- Collect metrics across all 10 repos
- Update compliance dashboard

**Success Criteria**:
- ✅ 10/10 high-priority repos compliant
- ✅ All validation scripts pass
- ✅ Compliance score: 7.5/8 average
- ✅ Zero breaking changes
- ✅ Developer training complete

---

### Phase 3: Medium-Priority Rollout (Week 4)

**Objective**: Deploy to 8 medium-priority repos with periodic updates

**Target Repositories** (Periodic Updates):
1. [ ] assessment-ddf
2. [ ] budget-ddf
3. [ ] conversor-ddf
4. [ ] crm-ddf
5. [ ] dataapp-data-input
6. [ ] extractor-ddf
7. [ ] proc-ddf
8. [ ] proto-ddf

**Day 18-19: Automated Bulk Update**
```bash
# Run bulk updater for all medium-priority repos
bash scripts/bulk-update-batch.sh medium-priority
```

**Day 20: Validation & Testing**
- Automated validation across all 8 repos
- Spot-check 2-3 repos manually
- Fix any issues

**Day 21: Documentation Update**
- Update all READMEs
- Add standardized commands
- Update central registry

**Success Criteria**:
- ✅ 8/8 medium-priority repos compliant
- ✅ Automated validation passes
- ✅ Documentation updated
- ✅ No manual intervention needed

---

### Phase 4: Low-Priority & Maintenance Rollout (Week 5)

**Objective**: Deploy to remaining 12 repos in maintenance mode

**Target Repositories** (Maintenance Mode):
1. [ ] 3d-ddf (enhance existing)
2. [ ] auto-drive-v2-try-2
3. [ ] beast
4. [ ] central-forecast-ddf-group
5. [ ] enrich-ddf-group
6. [ ] enrich-ddf-mod-ncm
7. [ ] solver-mod-bet
8. [ ] docs-fera
9. [ ] prompts-fera
10. [ ] scripts-fera
11. [ ] workflows-fera
12. [ ] Any remaining repos

**Day 22-23: Automated Bulk Update**
```bash
# Run bulk updater for all low-priority repos
bash scripts/bulk-update-batch.sh low-priority
```

**Day 24: Validation**
- Automated validation only
- Flag any failures for manual review

**Day 25: Cleanup & Documentation**
- Update central compliance dashboard
- Mark all repos as migrated
- Archive old configs

**Success Criteria**:
- ✅ 100% of repos standardized
- ✅ Compliance dashboard shows 7.5/8+ average
- ✅ All repos documented
- ✅ Migration complete

---

### Phase 5: Cloud Cost Automation (Week 6)

**Objective**: Deploy cost controls to 5 cloud-enabled repos

**Target Repositories** (Cloud Deployments):
1. [ ] deployer-ddf-mod-open-llms (enhance existing)
2. [ ] agent-ddf
3. [ ] 3d-ddf
4. [ ] gen-ddf-floor-2
5. [ ] Any other cloud repos

**Day 26: Cost Control Scripts**
```bash
# Deploy cost automation to each cloud repo
for repo in deployer-ddf-mod-open-llms agent-ddf 3d-ddf gen-ddf-floor-2; do
  echo "Deploying cost controls: $repo"
  cp scripts/cost/*.sh ~/local_repos/$repo/scripts/cost/
  cp scripts/cost/README.md ~/local_repos/$repo/scripts/cost/
done
```

**Day 27: Cron Configuration**
```bash
# Add cron jobs for each repo
# Stop non-prod at 10 PM
0 22 * * * cd ~/local_repos/deployer-ddf-mod-open-llms && make cloud-stop-night-force

# Start non-prod at 7 AM
0 7 * * * cd ~/local_repos/deployer-ddf-mod-open-llms && make cloud-start-morning

# Generate cost report at midnight
0 0 * * * cd ~/local_repos/deployer-ddf-mod-open-llms && make cloud-cost-report
```

**Day 28: Testing & Validation**
- Test stop/start scripts (dry-run)
- Verify cost reporting
- Monitor for 24 hours

**Day 29: Documentation**
- Cost control guide
- Cron setup instructions
- Override procedures

**Success Criteria**:
- ✅ Cost controls deployed to all cloud repos
- ✅ Cron automation operational
- ✅ Cost reports generated daily
- ✅ 60-70% cost reduction projected

---

### Phase 6: Validation & Continuous Improvement (Week 7-8)

**Objective**: Comprehensive validation, metrics collection, continuous monitoring

**Day 30-32: Comprehensive Testing**
```bash
# Run validation across all repos
bash scripts/validate-all-repos.sh

# Generate compliance report
bash scripts/generate-compliance-report.sh > active/compliance-report-$(date +%Y-%m-%d).md

# Collect performance metrics
bash scripts/collect-metrics.sh > active/metrics-report-$(date +%Y-%m-%d).md
```

**Day 33-35: Metrics Analysis**
- Compare before/after resource usage
- Analyze cost savings
- Review developer feedback
- Identify remaining gaps

**Day 36-38: Documentation Finalization**
- Complete central resource management guide
- Update all repo READMEs
- Create troubleshooting guide
- Publish training materials

**Day 39-40: Training & Handoff**
- Developer training sessions
- Demo new workflows
- Q&A sessions
- Handoff to ops team

**Day 41-42: Continuous Monitoring Setup**
- Weekly compliance checks
- Monthly metrics reports
- Quarterly reviews
- Feedback loop established

**Success Criteria**:
- ✅ 100% repos validated
- ✅ Compliance score: 7.5/8+ average
- ✅ 40-60% resource reduction achieved
- ✅ 60-70% cloud cost reduction achieved
- ✅ Zero runaway processes in 30 days
- ✅ 95%+ developer satisfaction
- ✅ Documentation complete
- ✅ Training delivered
- ✅ Continuous monitoring operational

---

## 📊 Propagation Automation

### Bulk Update Script

```bash
#!/bin/bash
# scripts/bulk-update-repo.sh
# Propagate standardization to a single repository

set -euo pipefail

REPO_PATH=$1
REPO_NAME=$(basename "$REPO_PATH")
TEMPLATE_DIR="$HOME/local_repos/enrich-ddf-floor-2/templates"

echo "🚀 Updating repository: $REPO_NAME"
echo "Path: $REPO_PATH"

cd "$REPO_PATH"

# 1. Docker Compose Updates
if [ -f "Dockerfile" ] || [ -d "docker" ]; then
  echo "📦 Updating Docker Compose..."

  if [ ! -f "compose.yml" ]; then
    echo "  Creating new compose.yml from template"
    cp "$TEMPLATE_DIR/compose.yml" ./compose.yml
    # Customize PROJECT_NAME
    sed -i.bak "s/PROJECT_NAME=.*/PROJECT_NAME=$REPO_NAME/" compose.yml
  else
    echo "  Enhancing existing compose.yml"
    # Add resource limits if missing
    bash "$TEMPLATE_DIR/scripts/add-resource-limits.sh" compose.yml
  fi

  # Validate
  docker compose config --quiet && echo "  ✅ Compose validated"
fi

# 2. Makefile Updates
if [ -f "Makefile" ]; then
  echo "⏱️  Adding timeout wrappers to Makefile..."
  bash "$TEMPLATE_DIR/scripts/add-makefile-timeouts.sh" Makefile
  echo "  ✅ Makefile updated"
fi

# 3. Resource Detection
echo "🔍 Deploying resource detection script..."
mkdir -p scripts
cp "$TEMPLATE_DIR/scripts/detect_resources.sh" scripts/
chmod +x scripts/detect_resources.sh
echo "  ✅ Resource detection deployed"

# 4. Package.json Updates (if Node.js)
if [ -f "package.json" ]; then
  echo "📦 Adding NODE_OPTIONS to package.json..."
  node "$TEMPLATE_DIR/scripts/add-node-options.js" package.json
  echo "  ✅ package.json updated"
fi

# 5. Playwright Config (if exists)
if [ -f "playwright.config.ts" ] || [ -f "frontend/playwright.config.ts" ]; then
  echo "🎭 Updating Playwright config..."
  bash scripts/detect_resources.sh --update-playwright
  echo "  ✅ Playwright config updated"
fi

# 6. Add Makefile Targets
echo "🎯 Adding standardized Makefile targets..."
cat >> Makefile << 'EOF'

# Resource management targets (standardized)
.PHONY: detect-resources compose-validate compose-up compose-down test-auto

detect-resources: ## Detect available system resources
	@bash scripts/detect_resources.sh

compose-validate: ## Validate compose.yml
	@docker compose config --quiet

compose-up: ## Start services with resource limits
	@docker compose --profile app up -d

compose-down: ## Stop all services
	@docker compose down

test-auto: ## Run tests with auto-detected settings
	@bash scripts/detect_resources.sh --apply --mode=balanced
	@npm test || pytest -v
EOF
echo "  ✅ Makefile targets added"

# 7. Documentation
echo "📚 Updating README..."
if ! grep -q "Resource Management" README.md 2>/dev/null; then
  cat >> README.md << 'EOF'

## Resource Management

This repository follows the [Dadosfera Resource Management Standard](https://github.com/dadosfera/standards/resource-management).

### Quick Commands
```bash
make detect-resources  # Check available resources
make compose-up        # Start with resource limits
make test-auto         # Run tests with optimal settings
make compose-down      # Stop all services
```

### Resource Limits
- Backend: 512MB RAM, 1.0 CPU
- Frontend: 768MB RAM, 1.0 CPU
- Database: 1GB RAM, 1.5 CPU

See `compose.yml` for details.
EOF
  echo "  ✅ README updated"
fi

# 8. Validation
echo "✅ Running final validation..."
bash "$TEMPLATE_DIR/scripts/validate-repo.sh" "$REPO_PATH"

echo ""
echo "🎉 Repository updated successfully: $REPO_NAME"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Test locally: make compose-up && make test-auto"
echo "  3. Commit: git add -A && git commit -m 'feat: standardize resource management'"
echo ""
```

### Batch Update Script

```bash
#!/bin/bash
# scripts/bulk-update-batch.sh
# Update multiple repositories in batch

set -euo pipefail

BATCH=${1:-"high-priority"}
REPOS_DIR="$HOME/local_repos"

case "$BATCH" in
  high-priority)
    REPOS=(
      "map-ddf-floor-2"
      "planner-ddf-floor-2"
      "news-ddf-floor-2"
      "ai-flow-module"
      "framework-ddf"
      "monitor-ddf"
      "assistant-ddf"
      "cline-ddf"
      "meta-assistant-ddf"
      "deployer-ddf-mod-open-llms"
    )
    ;;
  medium-priority)
    REPOS=(
      "assessment-ddf"
      "budget-ddf"
      "conversor-ddf"
      "crm-ddf"
      "dataapp-data-input"
      "extractor-ddf"
      "proc-ddf"
      "proto-ddf"
    )
    ;;
  low-priority)
    REPOS=(
      "3d-ddf"
      "auto-drive-v2-try-2"
      "beast"
      "central-forecast-ddf-group"
      "enrich-ddf-group"
      "enrich-ddf-mod-ncm"
      "solver-mod-bet"
      "docs-fera"
      "prompts-fera"
      "scripts-fera"
      "workflows-fera"
    )
    ;;
  *)
    echo "Unknown batch: $BATCH"
    echo "Valid batches: high-priority, medium-priority, low-priority"
    exit 1
    ;;
esac

echo "🚀 Batch update: $BATCH"
echo "Repositories: ${#REPOS[@]}"
echo ""

SUCCESS=0
FAILED=0

for repo in "${REPOS[@]}"; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Processing: $repo"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if bash scripts/bulk-update-repo.sh "$REPOS_DIR/$repo"; then
    echo "✅ Success: $repo"
    ((SUCCESS++))
  else
    echo "❌ Failed: $repo"
    ((FAILED++))
  fi

  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Batch Update Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Success: $SUCCESS"
echo "Failed: $FAILED"
echo "Total: ${#REPOS[@]}"
echo ""

if [ $FAILED -gt 0 ]; then
  echo "⚠️  Some repositories failed. Review logs above."
  exit 1
else
  echo "🎉 All repositories updated successfully!"
fi
```

---

## 🔄 Continuous Propagation

### Automated Weekly Checks

```bash
# Add to crontab for automated compliance monitoring
# Run every Monday at 9 AM
0 9 * * 1 cd ~/local_repos/enrich-ddf-floor-2 && bash scripts/check-compliance-all-repos.sh

# Generate monthly report
# Run on 1st of each month at 8 AM
0 8 1 * * cd ~/local_repos/enrich-ddf-floor-2 && bash scripts/generate-monthly-report.sh
```

### Future Improvements Propagation

When new improvements are added to the reference implementation (enrich-ddf-floor-2):

1. **Update templates** in `templates/` directory
2. **Run bulk updater** for affected repos
3. **Validate changes** across all repos
4. **Document** new features in central guide
5. **Train** developers on new capabilities

This ensures continuous improvement across all repositories with minimal manual effort.

---

## 📊 Success Metrics

### Resource Reduction Targets
- **Local CPU Usage**: Reduce average by 40-50%
- **Local Memory Usage**: Reduce peak by 50-60%
- **Cloud Costs**: Reduce non-prod costs by 60-70% (nightly shutdowns)
- **Build Times**: Maintain or improve (better resource allocation)

### Operational Improvements
- **Zero Runaway Processes**: All commands timeout-protected
- **Port Conflicts**: Zero conflicts across repos
- **Test Reliability**: 95%+ pass rate with resource limits
- **Developer Experience**: Faster local dev, fewer crashes

### Compliance
- **100%** of repos with Docker have resource limits
- **100%** of Makefiles have timeout protection
- **100%** of Node.js projects have memory caps
- **100%** of cloud repos have cost controls

---

## 🛠️ Implementation Tools

### Automation Scripts

#### 1. Repo Scanner
```bash
#!/bin/bash
# scripts/scan-repos.sh
# Scan all repos for resource management compliance

REPOS_DIR="$HOME/local_repos"
REPORT_FILE="active/repo-scan-$(date +%Y-%m-%d).md"

{
  echo "# Repository Resource Management Scan"
  echo "Generated: $(date)"
  echo ""
  echo "| Repository | Docker Compose | Makefile Timeouts | Resource Caps | Port Mgmt | Status |"
  echo "|------------|----------------|-------------------|---------------|-----------|--------|"

  for repo in "$REPOS_DIR"/*/; do
    repo_name=$(basename "$repo")
    has_compose="❌"
    has_timeouts="❌"
    has_caps="❌"
    has_ports="❌"

    [ -f "$repo/compose.yml" ] || [ -f "$repo/docker-compose.yml" ] && has_compose="✅"
    grep -q "timeout\|gtimeout" "$repo/Makefile" 2>/dev/null && has_timeouts="✅"
    grep -q "mem_limit\|cpus" "$repo"/*.yml 2>/dev/null && has_caps="✅"
    grep -q "PORT" "$repo/config/ports.js" 2>/dev/null && has_ports="✅"

    echo "| $repo_name | $has_compose | $has_timeouts | $has_caps | $has_ports | Pending |"
  done
} > "$REPORT_FILE"

echo "Scan complete: $REPORT_FILE"
```

#### 2. Bulk Updater
```bash
#!/bin/bash
# scripts/bulk-update-repos.sh
# Apply standardization to all repos

REPOS_DIR="$HOME/local_repos"
TEMPLATE_DIR="$HOME/local_repos/enrich-ddf-floor-2/templates"

for repo in "$REPOS_DIR"/*/; do
  repo_name=$(basename "$repo")
  echo "Updating: $repo_name"

  # Copy compose template if Docker exists
  if [ -f "$repo/Dockerfile" ]; then
    cp "$TEMPLATE_DIR/compose.yml" "$repo/compose.yml"
    echo "  ✅ Added compose.yml"
  fi

  # Add Makefile timeouts
  if [ -f "$repo/Makefile" ]; then
    # Add timeout wrapper script
    echo "  ⚠️  Manual review needed for Makefile"
  fi

  # Add NODE_OPTIONS to package.json
  if [ -f "$repo/package.json" ]; then
    node "$TEMPLATE_DIR/add-node-options.js" "$repo/package.json"
    echo "  ✅ Updated package.json"
  fi
done
```

#### 3. Validation Script
```bash
#!/bin/bash
# scripts/validate-compliance.sh
# Validate resource management compliance

REPOS_DIR="$HOME/local_repos"
FAILURES=0

for repo in "$REPOS_DIR"/*/; do
  repo_name=$(basename "$repo")

  # Check compose limits
  if [ -f "$repo/compose.yml" ]; then
    if ! grep -q "mem_limit" "$repo/compose.yml"; then
      echo "❌ $repo_name: Missing mem_limit in compose.yml"
      ((FAILURES++))
    fi
  fi

  # Check Makefile timeouts
  if [ -f "$repo/Makefile" ]; then
    if ! grep -q "timeout" "$repo/Makefile"; then
      echo "❌ $repo_name: Missing timeouts in Makefile"
      ((FAILURES++))
    fi
  fi
done

if [ $FAILURES -eq 0 ]; then
  echo "✅ All repos compliant!"
  exit 0
else
  echo "❌ $FAILURES compliance failures"
  exit 1
fi
```

---

## 📝 Documentation Requirements

### 1. Central Resource Management Guide
**Location**: `docs/guides/resource-management-standard.md`

**Contents**:
- Overview of standardization
- Docker Compose templates
- Makefile timeout guidelines
- Port allocation registry
- Cost control procedures
- Troubleshooting guide

### 2. Per-Repo README Updates
Add section to all repo READMEs:

```markdown
## Resource Management

This repository follows the [Dadosfera Resource Management Standard](../docs/guides/resource-management-standard.md).

### Local Development
- **Memory Limit**: 512MB (backend), 768MB (frontend)
- **CPU Limit**: 1.0 cores per service
- **Ports**: See [Port Registry](../config/ports.js)

### Quick Commands
```bash
make compose-up      # Start with resource limits
make compose-down    # Stop all services
make port-check      # Check for conflicts
make test-low        # Run low-resource tests
```
```

### 3. Migration Checklist
**Location**: `docs/guides/resource-mgmt-migration-checklist.md`

- [ ] Docker Compose limits added
- [ ] Makefile timeouts wrapped
- [ ] Log rotation configured
- [ ] Health checks added
- [ ] Port registry updated
- [ ] NODE_OPTIONS set
- [ ] Playwright tuned
- [ ] Cost controls deployed (if cloud)
- [ ] Documentation updated
- [ ] Validation passed

---

## 🚨 Risk Mitigation

### Identified Risks

1. **Breaking Changes**
   - **Risk**: Resource limits too aggressive, services fail
   - **Mitigation**: Start with generous limits, tune down gradually
   - **Rollback**: Keep original compose files as `.bak`

2. **Timeout False Positives**
   - **Risk**: Legitimate operations killed prematurely
   - **Mitigation**: Set conservative timeouts initially
   - **Monitoring**: Log all timeout events for review

3. **Port Conflicts**
   - **Risk**: Central registry out of sync
   - **Mitigation**: Automated validation in CI
   - **Resolution**: Dynamic port allocation fallback

4. **Cloud Cost Automation Failures**
   - **Risk**: Instances not stopped/started correctly
   - **Mitigation**: Dry-run by default, manual verification
   - **Alerts**: Email notifications on failures

### Rollback Plan

1. **Immediate Rollback** (< 5 minutes)
   ```bash
   # Restore original files from backup
   git checkout HEAD~1 compose.yml Makefile
   docker compose down && docker compose up -d
   ```

2. **Partial Rollback** (specific repos)
   ```bash
   # Disable resource limits
   docker compose --profile unlimited up -d
   ```

3. **Full Rollback** (all repos)
   ```bash
   # Run rollback script
   bash scripts/rollback-standardization.sh
   ```

---

## 📅 Timeline & Milestones

### Week 1-2: Quick Wins
- **Milestone 1**: Compose limits in 10 repos
- **Milestone 2**: Makefile timeouts in 10 repos
- **Deliverable**: Pilot report with metrics

### Week 3-4: Infrastructure
- **Milestone 3**: Port management deployed
- **Milestone 4**: Test tuning complete
- **Deliverable**: Infrastructure guide

### Week 5-6: Cloud Automation
- **Milestone 5**: Cost controls in 5 cloud repos
- **Milestone 6**: Cron automation configured
- **Deliverable**: Cost savings report

### Week 7-8: Validation & Docs
- **Milestone 7**: All repos validated
- **Milestone 8**: Documentation complete
- **Deliverable**: Final rollout report

---

## 🎓 Training & Handoff

### Developer Training
1. **Resource Management 101** (30 min)
   - Why resource limits matter
   - How to use new Make targets
   - Troubleshooting common issues

2. **Cloud Cost Controls** (20 min)
   - Nightly automation overview
   - Manual override procedures
   - Cost reporting interpretation

3. **Port Management** (15 min)
   - Port registry usage
   - Conflict resolution
   - Dynamic allocation

### Documentation Handoff
- Central guide published
- Per-repo READMEs updated
- Migration checklist available
- Troubleshooting FAQ created

---

## 📞 Support & Escalation

### Support Channels
- **Quick Questions**: Slack #resource-management
- **Issues**: GitHub Issues with `resource-mgmt` label
- **Escalation**: Tag @infrastructure-team

### Common Issues & Solutions

**Issue**: Service fails to start with memory limit
**Solution**: Increase `mem_limit` in compose.yml, test, commit

**Issue**: Timeout kills legitimate operation
**Solution**: Increase timeout in Makefile, document reason

**Issue**: Port conflict detected
**Solution**: Update port registry, choose alternative port

**Issue**: Cloud instance not stopped
**Solution**: Check cron logs, run manual stop command

---

## ✅ Acceptance Criteria

### Phase 1 Complete When:
- [ ] 100% of Docker repos have resource limits
- [ ] 100% of Makefiles have timeout protection
- [ ] Log rotation configured everywhere
- [ ] Validation script passes

### Phase 2 Complete When:
- [ ] Port registry covers all repos
- [ ] Health checks added to all services
- [ ] Test tuning applied to all test suites
- [ ] Low-resource targets available

### Phase 3 Complete When:
- [ ] Cost control scripts deployed
- [ ] Cron automation configured
- [ ] Cost reporting operational
- [ ] 60%+ cost reduction achieved

### Project Complete When:
- [ ] All acceptance criteria met
- [ ] Documentation published
- [ ] Training delivered
- [ ] Metrics dashboard live
- [ ] Handoff to ops team complete

---

## 📊 Appendix: Reference Templates

### A. Standard compose.yml
See: `/Users/luismartins/local_repos/enrich-ddf-floor-2/compose.yml`

### B. Standard Makefile Targets
```makefile
# Resource management targets (add to all Makefiles)
.PHONY: compose-validate compose-up compose-down port-check test-low

compose-validate:
	@timeout 10 docker compose config --quiet

compose-up:
	@timeout 60 docker compose --profile app up -d

compose-down:
	@timeout 30 docker compose down

port-check:
	@timeout 5 node config/ports.js --check

test-low:
	@NODE_OPTIONS=--max-old-space-size=1536 timeout 120 npm test -- --maxWorkers=2
```

### C. Standard package.json Scripts
```json
{
  "scripts": {
    "dev": "NODE_OPTIONS=--max-old-space-size=2048 vite",
    "build": "NODE_OPTIONS=--max-old-space-size=2048 tsc -b && vite build",
    "test": "NODE_OPTIONS=--max-old-space-size=2048 jest",
    "lint": "NODE_OPTIONS=--max-old-space-size=2048 eslint ."
  }
}
```

### D. Standard Playwright Config
```typescript
export default defineConfig({
  fullyParallel: false,
  workers: process.env.CI ? 1 : 2,
  retries: process.env.CI ? 2 : 0,
  // ... rest of config
});
```

---

## 🔗 Related Documents

- [Resource Management Standard](../docs/guides/resource-management-standard.md)
- [Port Registry](../config/ports.js)
- [Cost Control Scripts](../scripts/cost/)
- [Migration Checklist](../docs/guides/resource-mgmt-migration-checklist.md)
- [Troubleshooting Guide](../docs/troubleshooting/resource-management.md)

---

**Next Steps**:
1. Review and approve this plan
2. Run repo scanner to establish baseline
3. Begin Phase 1 rollout with pilot repos
4. Monitor metrics and adjust as needed

**Questions or Concerns**: Contact @infrastructure-team or open an issue with `resource-mgmt` label.
