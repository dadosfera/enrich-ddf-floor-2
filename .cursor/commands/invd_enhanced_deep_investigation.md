# /invd_enhanced_deep_investigation

Deep investigation with active instrumentation and debugging enhancements. This command modifies code to add comprehensive logging, debugging capabilities, and monitoring before attempting to diagnose root cause. Use when surface-level investigation isn't sufficient or when you need to understand system behavior in detail.

**Local Reference**: `commands/invd_enhanced_deep_investigation.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/invd_enhanced_deep_investigation.md`

Backlinks:

- `mini_prompt/lv2/deep_debugging_instrumentation_mini_prompt.md`
- `commands/invr_investigate_root_cause.md`
- `commands/bdbg_browser_debug.md`
- `commands/exec_execute_plan.md`

## When to use this command

Use `/invd_enhanced_deep_investigation` when:

1. Surface-level investigation (`/invr_investigate_root_cause`) isn't providing enough insight
2. You need to understand detailed system behavior, timing, or state changes
3. Console logs and error messages are insufficient
4. You need to trace execution flow through multiple layers
5. The problem appears intermittent or involves complex interactions
6. Browser-based issues need dev tools inspection
7. File/database state changes need monitoring
8. Async operations or race conditions are suspected

Do **NOT** use when:

- The problem is obvious and well-understood (use `/invr_investigate_root_cause` instead)
- You have direct access to already-detailed logs (use `/invr_investigate_root_cause`)
- The fix is simple and doesn't require understanding system behavior
- You're in production and can't modify code (get approval first)

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Determine problem type and affected systems

The AI should analyze:
- Frontend/UI issues (need browser dev tools, DOM inspection)
- Backend/API issues (need request/response logging)
- Database issues (need query logging, state changes)
- Integration issues (need cross-layer tracing)
- Performance/timing issues (need execution timing, profiling)

```bash
# Create investigation directory
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
REPO_NAME=$(basename "$REPO_ROOT")

if [[ "$REPO_NAME" == *-fera ]]; then
  INVESTIGATION_DIR="_dev/docs/investigations"
else
  INVESTIGATION_DIR="docs/investigations"
fi

gtimeout 5 mkdir -p "$INVESTIGATION_DIR"
```

3. Create instrumentation plan document

```bash
INVESTIGATION_SLUG="$(date +%Y-%m-%d)_deep_investigation_instrumentation"
INVESTIGATION_FILE="$INVESTIGATION_DIR/${INVESTIGATION_SLUG}.md"

cat > "$INVESTIGATION_FILE" << 'EOF'
# Deep Investigation: [Problem Title]

**Status**: INSTRUMENTATION_PHASE
**Date**: [ISO timestamp]
**Problem Type**: [UI/Backend/Database/Integration/Performance/Other]

## Problem Statement

[Clear description of what is broken]

## Phase 1: Instrumentation Planning

### Affected Components

- [Component 1] (location: path/to/file)
- [Component 2] (location: path/to/file)
- [etc.]

### Instrumentation Strategy

#### For Frontend/UI Issues:
- [ ] Enable browser console verbose logging
- [ ] Add DOM inspection logging (element changes, event listeners)
- [ ] Enable Network tab recording
- [ ] Add React DevTools profiling (if applicable)
- [ ] Capture JavaScript stack traces
- [ ] Monitor for errors and warnings
- [ ] Check for memory leaks or performance issues

#### For Backend/API Issues:
- [ ] Add request/response logging with timestamps
- [ ] Log function entry/exit with parameters
- [ ] Add state change logging
- [ ] Enable debug mode for dependencies
- [ ] Log database queries (if applicable)
- [ ] Add execution timing measurements
- [ ] Log all error paths

#### For Database Issues:
- [ ] Enable query logging with timing
- [ ] Log connection state changes
- [ ] Monitor transaction lifecycle
- [ ] Log lock/deadlock situations
- [ ] Track data state changes
- [ ] Log migration/schema changes

#### For Integration Issues:
- [ ] Enable cross-component tracing
- [ ] Log message/event flow
- [ ] Add call stack tracking
- [ ] Monitor data flow between systems
- [ ] Log synchronization points

### Files to Instrument

| File | Current State | Instrumentation Needed | Priority |
|------|---------------|------------------------|----------|
| [File 1] | [Brief current logging] | [What logging to add] | HIGH |
| [File 2] | [Brief current logging] | [What logging to add] | MEDIUM |

## Phase 2: Instrumentation Implementation

### Changes Made

#### File: [path/to/file.js or .py or .md]

**Before**: [Show original code snippet]

**After**: [Show instrumented code with logging]

**Logging added**:
- [What is being logged and when]
- [Format of log output]
- [Expected output examples]

---

#### File: [path/to/file2]

[Same structure as above for each file]

---

### Environment Variables / Configuration

- Enable debug mode: [HOW]
- Logging level: [VERBOSE/DEBUG/INFO]
- Log output location: [stdout/file/both]
- Special flags: [Any special CLI flags or config needed]

## Phase 3: Execution with Enhanced Logging

### Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [etc.]

### Expected Enhanced Logging Output

```
[LOG FORMAT AND EXPECTED OUTPUT]
[Example 1]
[Example 2]
```

### Actual Enhanced Logging Output

[Will be filled after running with instrumentation]

### Analysis of Logging Output

[Observations from the logs]

## Phase 4: Root Cause Analysis (from Enhanced Data)

### Root Cause

[Based on enhanced logging, the root cause is:]

### Supporting Evidence

[Log excerpts and data from instrumentation]

### Why This Happens

[Technical explanation with reference to logged behavior]

## Phase 5: Solution Options

### Option A: [Title]

**Approach**: [How to fix the root cause]

**Impact on Instrumentation**: [Can we remove instrumentation after? Or keep it?]

**Pros/Cons**: [See invr_investigate_root_cause format]

---

### Option B: [Title]

[Same format]

---

## Phase 6: Instrumentation Cleanup Decision

- [ ] Keep instrumentation (for production debugging)
- [ ] Remove instrumentation after investigation
- [ ] Convert to permanent debug flag (environment variable controlled)
- [ ] Move to proper logging framework

### Cleanup Plan

[If instrumentation needs to be removed or converted]

---

**Generated**: [timestamp]
**Investigation by**: [AI model identifier]
EOF
```

4. Identify affected files and add instrumentation

The AI should:

**For Frontend (JavaScript/React/TypeScript)**:
- Add `console.log()` with labeled output for key operations
- Add error boundary logging
- Add performance timing measurements
- Add state change logging
- Use browser DevTools profiling (see `/bdbg_browser_debug`)

```javascript
// Example Frontend Instrumentation
const DEBUG = process.env.DEBUG_INVESTIGATION === 'true';

function myFunction(param) {
  if (DEBUG) console.log(`[myFunction START] param=`, param);
  
  try {
    const result = someOperation(param);
    if (DEBUG) console.log(`[myFunction RESULT]`, result);
    return result;
  } catch (error) {
    if (DEBUG) console.error(`[myFunction ERROR]`, error);
    throw error;
  }
}
```

**For Backend (Python/Node.js)**:
- Add logging with timestamps and execution context
- Add debug-level logging for key operations
- Add request/response logging
- Add execution timing

```python
# Example Backend Instrumentation
import logging
DEBUG = os.getenv('DEBUG_INVESTIGATION', 'false').lower() == 'true'

logger = logging.getLogger(__name__)
if DEBUG:
    logger.setLevel(logging.DEBUG)

def my_function(param):
    if DEBUG:
        logger.debug(f"[ENTRY] my_function param={param}")
    
    try:
        start_time = time.time()
        result = some_operation(param)
        elapsed = time.time() - start_time
        
        if DEBUG:
            logger.debug(f"[EXIT] my_function result={result} elapsed={elapsed}s")
        
        return result
    except Exception as e:
        if DEBUG:
            logger.error(f"[ERROR] my_function error={e}", exc_info=True)
        raise
```

**For File/State Logging**:
- Add logging for file operations (read/write/delete)
- Add state change tracking
- Log before/after states

5. Set up environment and reproduction steps

Create a script or instructions for reproducing the problem with enhanced logging:

```bash
# Set debug flag
export DEBUG_INVESTIGATION=true

# Run application/tests with enhanced logging
npm run dev  # or python app.py or similar

# Capture and save logs
# [logs will show detailed execution flow]
```

6. Execute with enhanced instrumentation

The AI should:
- Run the application or reproduce the problem
- Collect all debug output
- Monitor browser dev tools (if UI-related)
- Log file state changes
- Track timing and performance metrics
- Note any errors or unexpected behavior

7. Analyze enhanced debugging output

Document findings in the investigation file:
- What did the logs reveal?
- What unexpected behavior was observed?
- What timing patterns were visible?
- Where did execution differ from expectations?
- Were there error messages or warnings?

8. Update investigation file with findings

Complete all sections of the investigation file with actual data and analysis.

9. Make implementation-ready diagnosis

Based on enhanced data, create clear root cause analysis and solution options (see `/invr_investigate_root_cause` format).

10. Optional: Convert instrumentation to permanent debug framework

If the instrumentation proves valuable:

```bash
# Instead of removing, make it configurable
# - Replace console.log with proper logging framework
# - Add DEBUG environment variable flag
# - Document in README.md how to enable debug mode
# - Commit with instrumentation (for future debugging)
```

11. Commit investigation work

```bash
gtimeout 10 git add "$INVESTIGATION_FILE"
```

```bash
gtimeout 5 git status --short | head -20
```

```bash
gtimeout 10 git commit -m "Deep investigation: enhanced instrumentation and root cause analysis for [problem]"
```

```bash
gtimeout 15 git push
```

## Instrumentation Techniques by Problem Type

### Frontend/Browser Issues

Use `/bdbg_browser_debug` for detailed browser inspection:
- Console log capture
- Network request inspection
- DOM element inspection
- Performance profiling
- Error stack traces

```javascript
// Add to your React/Vue/etc components
if (window.DEBUG_INVESTIGATION) {
  console.log(`[Component Render] name=${this.constructor.name}`);
  console.log(`[Props]`, this.props);
  console.log(`[State]`, this.state);
}
```

### Backend/API Issues

```python
import logging
import time
from functools import wraps

def debug_trace(func):
    """Decorator for tracing function calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.getenv('DEBUG_INVESTIGATION'):
            logger.debug(f"[CALL] {func.__name__} args={args} kwargs={kwargs}")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            if os.getenv('DEBUG_INVESTIGATION'):
                logger.debug(f"[RETURN] {func.__name__} result={result} elapsed={elapsed}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            if os.getenv('DEBUG_INVESTIGATION'):
                logger.error(f"[ERROR] {func.__name__} error={e} elapsed={elapsed}s", exc_info=True)
            raise
    return wrapper
```

### Database Issues

```python
# Enable query logging
if os.getenv('DEBUG_INVESTIGATION'):
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    # or for MongoDB:
    logging.getLogger('pymongo').setLevel(logging.DEBUG)
```

### Performance Issues

```javascript
// JavaScript performance profiling
if (window.DEBUG_INVESTIGATION) {
  const start = performance.now();
  // ... operation ...
  const end = performance.now();
  console.log(`[PERF] Operation took ${end - start}ms`);
}
```

## Checklist

- [ ] Problem type correctly identified
- [ ] All affected components identified
- [ ] Instrumentation added without breaking functionality
- [ ] Debug flag properly configured (environment variable)
- [ ] Problem successfully reproduced with enhanced logging
- [ ] Enhanced logs provide new insights
- [ ] Root cause identified from instrumentation data
- [ ] Solution options documented with supporting evidence
- [ ] Decision made: Keep, convert, or remove instrumentation
- [ ] Investigation file completely filled out
- [ ] Changes committed to version control

## Sequential Workflow

After deep investigation is complete:

### If Root Cause is Clear

```
/invd_enhanced_deep_investigation [completes]
↓
/exec_execute_plan [execute the identified fix]
```

### If More Investigation Needed

```
/invd_enhanced_deep_investigation [completes with partial findings]
↓
/hlp_escalation [request help from higher-model]
```

### If Creating a Formal Plan

```
/invd_enhanced_deep_investigation [completes with clear diagnosis]
↓
/pfac_plan_from_active_tasks_conversation [create detailed plan]
```

## Comparison with Other Investigation Commands

| Command | Focus | Code Changes | Output |
|---------|-------|--------------|--------|
| `/invr_investigate_root_cause` | Quick diagnosis | No | Analysis + proposal |
| **`/invd_enhanced_deep_investigation`** | **Deep understanding** | **Yes (instrumentation)** | **Instrumentation + rich analysis + proposal** |
| `/bdbg_browser_debug` | Browser-specific | No | Network/console/DOM data |
| `/rerr_recurrent_errors` | Known issues | Yes (fixes) | Fix + prevention |

## Best Practices

1. **Non-destructive first** - Add logging, don't delete or change core logic
2. **Environment-based** - Use flags to enable/disable debug output
3. **Reversible** - Make sure instrumentation can be easily removed or toggled
4. **Structured logging** - Use consistent format for all log output
5. **Targeted** - Only instrument the paths that matter for your problem
6. **Performance conscious** - Avoid excessive logging that slows down execution
7. **Document everything** - Record what was changed and why
8. **Clean up or keep** - Decide early if instrumentation stays permanently

## Related Commands

- `/invr_investigate_root_cause` - Quick diagnosis without instrumentation
- `/bdbg_browser_debug` - Browser dev tools inspection
- `/exec_execute_plan` - Execute the identified fix
- `/pfac_plan_from_active_tasks_conversation` - Create formal plan from diagnosis
- `/hlp_escalation` - Request help if investigation is inconclusive

---

**Last updated**: 2025-11-29
