# /gtag_verify_git_tags

<!-- COMMAND_ID: 097 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: gt_verify_git_tags -->

**Read-only verification.** Verify and audit git tags against the git tag convention standard. Lists all tags, categorizes them, validates compliance, checks health status, and provides recommendations for non-compliant tags.

**Local Reference**: `commands/gtag_verify_git_tags.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/gtag_verify_git_tags.md`

Backlinks:
- `standards/git/git_tag_convention.md` (defines tag naming conventions)
- `mini_prompt/lv1/automated_release_tagging_lv1_mini_prompt.md` (creates tags)
- `mini_prompt/lv1/git_tag_verification_lv1_mini_prompt.md` (detailed verification workflow)

## Purpose

This command provides comprehensive git tag verification and auditing capabilities:
- Lists all tags in the repository
- Validates tag names against the git tag convention standard
- Checks health status compliance
- Categorizes tags (production, pre-release, environment, special purpose, legacy)
- Provides actionable recommendations for non-compliant tags

## When to Use

- Before creating new tags to understand existing tag patterns
- After importing repositories to audit tag compliance
- During repository maintenance to identify non-compliant tags
- When preparing for releases to verify tag consistency
- As part of repository health checks

## Command sequence (run in order)

### 1. Confirm repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

### 2. Fetch latest tags from remote

```bash
gtimeout 30 git fetch --tags origin 2>/dev/null || echo "⚠️  Could not fetch tags from remote"
```

### 3. List all tags

```bash
echo "=== All Git Tags ==="
gtimeout 10 git tag -l | sort -V
TAG_COUNT=$(git tag -l | wc -l | tr -d ' ')
echo "Total tags: $TAG_COUNT"
```

### 4. Categorize tags

```bash
echo ""
echo "=== Tag Categorization ==="

# Production release tags (v*+healthy, v*+degraded)
PROD_TAGS=$(git tag -l "v*+healthy" "v*+degraded" 2>/dev/null | sort -V)
PROD_COUNT=$(echo "$PROD_TAGS" | grep -v '^$' | wc -l | tr -d ' ')
echo "Production releases: $PROD_COUNT"
echo "$PROD_TAGS" | head -10
[ "$PROD_COUNT" -gt 10 ] && echo "... and $((PROD_COUNT - 10)) more"

# Pre-release tags (alpha, beta, rc)
PRE_RELEASE_TAGS=$(git tag -l "v*-alpha*" "v*-beta*" "v*-rc*" 2>/dev/null | sort -V)
PRE_RELEASE_COUNT=$(echo "$PRE_RELEASE_TAGS" | grep -v '^$' | wc -l | tr -d ' ')
echo ""
echo "Pre-releases: $PRE_RELEASE_COUNT"
echo "$PRE_RELEASE_TAGS" | head -10
[ "$PRE_RELEASE_COUNT" -gt 10 ] && echo "... and $((PRE_RELEASE_COUNT - 10)) more"

# Environment tags
ENV_TAGS=$(git tag -l "env/*" 2>/dev/null | sort -V)
ENV_COUNT=$(echo "$ENV_TAGS" | grep -v '^$' | wc -l | tr -d ' ')
echo ""
echo "Environment tags: $ENV_COUNT"
echo "$ENV_TAGS"

# Special purpose tags (backup, checkpoint)
BACKUP_TAGS=$(git tag -l "backup/*" 2>/dev/null | sort -V)
BACKUP_COUNT=$(echo "$BACKUP_TAGS" | grep -v '^$' | wc -l | tr -d ' ')
CHECKPOINT_TAGS=$(git tag -l "checkpoint/*" 2>/dev/null | sort -V)
CHECKPOINT_COUNT=$(echo "$CHECKPOINT_TAGS" | grep -v '^$' | wc -l | tr -d ' ')
echo ""
echo "Special purpose tags:"
echo "  Backup tags: $BACKUP_COUNT"
echo "  Checkpoint tags: $CHECKPOINT_COUNT"
```

### 5. Validate tag compliance

```bash
echo ""
echo "=== Tag Compliance Validation ==="

# Primary format pattern: v{MAJOR}.{MINOR}.{PATCH}[-{stage}.{increment}][+{health}.{build_info}]
VALID_PATTERN="^v[0-9]+\.[0-9]+\.[0-9]+(-[a-z]+(\.[0-9]+)?)?(\+[a-z]+(\..*)?)?$"

COMPLIANT_COUNT=0
NON_COMPLIANT_COUNT=0
NON_COMPLIANT_TAGS=""

for tag in $(git tag -l); do
  # Skip environment and special purpose tags (they have different patterns)
  if [[ "$tag" =~ ^env/ ]] || [[ "$tag" =~ ^backup/ ]] || [[ "$tag" =~ ^checkpoint/ ]]; then
    continue
  fi
  
  if [[ "$tag" =~ $VALID_PATTERN ]]; then
    COMPLIANT_COUNT=$((COMPLIANT_COUNT + 1))
  else
    NON_COMPLIANT_COUNT=$((NON_COMPLIANT_COUNT + 1))
    NON_COMPLIANT_TAGS="$NON_COMPLIANT_TAGS\n$tag"
  fi
done

echo "Compliant tags: $COMPLIANT_COUNT"
echo "Non-compliant tags: $NON_COMPLIANT_COUNT"

if [ "$NON_COMPLIANT_COUNT" -gt 0 ]; then
  echo ""
  echo "⚠️  Non-compliant tags found:"
  echo -e "$NON_COMPLIANT_TAGS" | grep -v '^$'
  echo ""
  echo "📖 See standards/git/git_tag_convention.md for naming rules"
fi
```

### 6. Validate health status

```bash
echo ""
echo "=== Health Status Validation ==="

HEALTHY_COUNT=0
DEGRADED_COUNT=0
FAILING_COUNT=0
MISSING_HEALTH_COUNT=0
INVALID_HEALTH_COUNT=0

for tag in $(git tag -l "v*"); do
  if [[ "$tag" =~ \+healthy ]]; then
    HEALTHY_COUNT=$((HEALTHY_COUNT + 1))
  elif [[ "$tag" =~ \+degraded ]]; then
    DEGRADED_COUNT=$((DEGRADED_COUNT + 1))
  elif [[ "$tag" =~ \+failing ]]; then
    FAILING_COUNT=$((FAILING_COUNT + 1))
    # Check if failing is only on alpha releases
    if [[ ! "$tag" =~ -alpha ]]; then
      INVALID_HEALTH_COUNT=$((INVALID_HEALTH_COUNT + 1))
      echo "⚠️  Invalid: $tag has +failing but is not an alpha release"
    fi
  else
    # Check if it's a production release (no stage suffix)
    if [[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || [[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+\+ ]]; then
      MISSING_HEALTH_COUNT=$((MISSING_HEALTH_COUNT + 1))
    fi
  fi
done

echo "Tags with +healthy: $HEALTHY_COUNT"
echo "Tags with +degraded: $DEGRADED_COUNT"
echo "Tags with +failing: $FAILING_COUNT"
echo "Production tags missing health status: $MISSING_HEALTH_COUNT"
echo "Invalid health status usage: $INVALID_HEALTH_COUNT"

if [ "$MISSING_HEALTH_COUNT" -gt 0 ]; then
  echo ""
  echo "⚠️  Production tags should include health status (+healthy, +degraded, or +failing)"
fi
```

### 7. Generate summary report

```bash
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "📊 Git Tag Verification Summary"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Total tags: $TAG_COUNT"
echo "  Production releases: $PROD_COUNT"
echo "  Pre-releases: $PRE_RELEASE_COUNT"
echo "  Environment tags: $ENV_COUNT"
echo "  Special purpose: $((BACKUP_COUNT + CHECKPOINT_COUNT))"
echo ""
echo "Compliance:"
echo "  ✅ Compliant: $COMPLIANT_COUNT"
echo "  ❌ Non-compliant: $NON_COMPLIANT_COUNT"
echo ""
echo "Health Status:"
echo "  ✅ Healthy: $HEALTHY_COUNT"
echo "  ⚠️  Degraded: $DEGRADED_COUNT"
echo "  ❌ Failing: $FAILING_COUNT"
echo "  ⚪ Missing: $MISSING_HEALTH_COUNT"
echo ""
if [ "$NON_COMPLIANT_COUNT" -gt 0 ] || [ "$MISSING_HEALTH_COUNT" -gt 0 ] || [ "$INVALID_HEALTH_COUNT" -gt 0 ]; then
  echo "⚠️  Issues found - see details above"
  echo "📖 Reference: standards/git/git_tag_convention.md"
else
  echo "✅ All tags are compliant"
fi
echo "═══════════════════════════════════════════════════════════"
```

## Validation Rules

Based on `standards/git/git_tag_convention.md`:

### Primary Format
- Must start with `v` followed by semantic version (MAJOR.MINOR.PATCH)
- Optional stage suffix: `-alpha`, `-beta`, `-rc` followed by increment number
- Optional metadata: `+{health}` where health is `healthy`, `degraded`, or `failing`
- Build info can follow health: `+healthy.g1a2b3c4`

### Health Status Rules
- `+failing` is only allowed for `-alpha` releases
- Production releases (no stage) should include health status
- Valid health values: `healthy`, `degraded`, `failing`

### Special Purpose Tags
- Environment tags: `env/{env_code}-{tag_name}`
- Backup tags: `backup/{operation}/{timestamp}`
- Checkpoint tags: `checkpoint/{type}/{identifier}`

## Examples

### Compliant Tags
```bash
v1.0.0+healthy
v2.1.3+healthy.g1a2b3c4
v1.0.0-alpha.1+healthy
v1.0.0-beta.2+degraded
v1.0.0-rc.1+healthy
env/dev-v1.0.0+healthy
backup/release/20250115-143022
```

### Non-Compliant Tags
```bash
1.0.0              # Missing 'v' prefix
v1.0               # Missing PATCH version
v1.0.0             # Missing health status (production release)
v1.0.0+failing     # Failing health on non-alpha release
v1.0.0+unknown     # Invalid health status
```

## Integration

This command complements:
- `/automated_release_tagging` mini prompt - creates compliant tags
- `standards/git/git_tag_convention.md` - defines conventions
- Git hooks - can use validation patterns for pre-tag validation

## Notes

- This is a read-only command - it does not modify tags
- For tag creation, use the `automated_release_tagging` mini prompt
- For tag cleanup, manually review non-compliant tags and migrate as needed
- Environment and special purpose tags are validated separately from version tags
