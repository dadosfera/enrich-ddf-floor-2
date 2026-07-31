---
category: quality
criticality: medium
scope: all
---
# /matp_product_components_maturity
<!-- COMMAND_ID: 060 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: maturity_assessment -->

**Shortcut**: `matp`

**Local Reference**: `commands/matp_product_components_maturity.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/matp_product_components_maturity.md`

## Command sequence (run in order)

### 1. Confirm Repository Context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

### 2. Scan for Documented API

```bash
# Check for API documentation files
find . -maxdepth 2 -type f \( -name "swagger.json" -o -name "openapi.yaml" -o -name "openapi.yml" -o -name "*.swagger.yaml" \) 2>/dev/null | head -5

# Check for API documentation in docs/
ls -la docs/ 2>/dev/null | grep -i -E "api|swagger|openapi" | head -10

# Check package.json/pyproject.toml for API doc tools
grep -E "swagger|openapi|redoc|spectacle" package.json pyproject.toml 2>/dev/null | head -5
```

### 3. Scan Authentication & Authorization

```bash
# Check for authentication middleware/libraries
grep -r "session\|passport\|jwt\|keycloak\|auth0\|firebase" package.json pyproject.toml requirements.txt 2>/dev/null | head -10

# Check for Keycloak integration (Floor 3+)
find . -maxdepth 3 -type f -name "*keycloak*" 2>/dev/null

# Check for auth configuration
find . -maxdepth 2 -type f \( -name "*auth*" -o -name "*session*" \) 2>/dev/null | grep -E "\.(ts|js|py|go)$" | head -5
```

### 4. Scan API Gateway & Token Management

```bash
# Check for OAuth2 Proxy (Floor 1)
grep -r "oauth2-proxy\|oauth2_proxy" docker-compose.yml Dockerfile .env* config/ 2>/dev/null

# Check for KrakenD (Floor 2)
find . -maxdepth 2 -type f -name "*krakend*" 2>/dev/null
ls -la krakend/ 2>/dev/null

# Check for Kong (Floor 3+)
find . -maxdepth 2 -type f -name "*kong*" 2>/dev/null
grep -r "kong\|admin.kong" docker-compose.yml 2>/dev/null

# Check for API token/key management
grep -r "api.key\|api_key\|token_expir\|token_rotation" src/ app/ 2>/dev/null | head -5
```

### 5. Scan for Databases

```bash
# Transactional database (all floors)
grep -r "postgresql\|postgres\|mysql\|mariadb\|mongodb" docker-compose.yml Dockerfile package.json pyproject.toml 2>/dev/null

# Check for database migrations
find . -maxdepth 3 -type d -name "*migrat*" 2>/dev/null
ls -la db/migrations/ schema/ 2>/dev/null

# Analytics database (Floor 3+ only)
grep -r "bigquery\|snowflake\|redshift\|duckdb" package.json pyproject.toml src/ 2>/dev/null | head -5
```

### 6. Scan for Landing Page & Marketing Site

```bash
# Check for landing page / marketing site
ls -la marketing/ landing/ website/ public/ 2>/dev/null
find . -maxdepth 2 -type f -name "next.config.js" -o -name "gatsby-config.js" 2>/dev/null

# Check for static site generators
grep -r "next\|gatsby\|hugo\|jekyll" package.json 2>/dev/null | head -5
```

### 7. Scan for User Metering/Analytics

```bash
# Check for analytics tracking
grep -r "mixpanel\|posthog\|segment\|analytics\|tracking" package.json pyproject.toml src/ 2>/dev/null | head -5

# Check for custom analytics
find . -maxdepth 3 -type f -name "*analytics*" -o -name "*metrics*" 2>/dev/null
```

### 8. Scan for Chat/Bot/AI Components (Floor 3+ Only)

```bash
# Check for OpenAI integration
grep -r "openai\|langchain\|anthropic\|gpt" package.json pyproject.toml src/ 2>/dev/null | head -5

# Check for chat endpoints
find . -maxdepth 3 -type f -name "*chat*" -o -name "*bot*" -o -name "*assistant*" 2>/dev/null | grep -E "\.(ts|js|py)$" | head -5
```

### 9. Scan for Billing System (Floor 3+ Only)

```bash
# Check for Stripe integration
grep -r "stripe\|paddle\|payment\|billing" package.json pyproject.toml src/ 2>/dev/null | head -5

# Check for subscription logic
find . -maxdepth 3 -type f -name "*billing*" -o -name "*subscription*" 2>/dev/null | grep -E "\.(ts|js|py)$" | head -5

# Check for payment webhooks
grep -r "webhook\|stripe_event\|payment.*callback" src/ 2>/dev/null | head -5
```

### 10. Scan for Multi-Tenancy (Floor 3+ Only)

```bash
# Check for tenant/org isolation
grep -r "tenant_id\|org_id\|workspace_id\|customer_id" src/ db/migrations/ 2>/dev/null | head -10

# Check for RLS policies (Postgres)
grep -r "CREATE POLICY\|ROW LEVEL SECURITY\|RLS" db/ 2>/dev/null | head -5

# Check for multi-org support
grep -r "multi.*tenant\|multi.*org\|tenant.*isolation" docs/ README.md 2>/dev/null | head -5
```
