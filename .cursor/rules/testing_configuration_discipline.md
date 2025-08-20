# Testing Configuration Discipline

## Rule Priority: P0 (Always Applied)

## Purpose

This rule prevents endless testing configuration loops and technical debt accumulation by enforcing strict discipline around testing framework selection and configuration management.

## Core Principles

### 1. Tool Alignment Over Configuration Complexity

**ALWAYS**: Choose testing tools that natively support your technology stack
**NEVER**: Try to force incompatible tools to work through complex configuration

```typescript
// ✅ GOOD: Tool aligns with stack and constraints
// Webpack + TypeScript + ESM + No tinypool issues → Use Jest (optimized)
module.exports = {
  preset: "ts-jest/presets/default-esm",
  testEnvironment: "jsdom",
  extensionsToTreatAsEsm: [".ts", ".tsx"],
  globals: { "ts-jest": { useESM: true } },
  setupFilesAfterEnv: ["<rootDir>/jest.setup.cjs"],
  moduleNameMapper: { "^@/(.*)$": "<rootDir>/src/$1" },
  // Total: 8 lines (under 30-line limit)
};

// ❌ BAD: Ignoring critical constraints
// Webpack + TypeScript + ESM + Tinypool bug → Forcing Vitest
export default defineConfig({
  test: {
    environment: "jsdom",
    // Looks simple but breaks due to tinypool file resolution bug
  },
});

// ❌ BAD: Configuration explosion
module.exports = {
  preset: "ts-jest/presets/default-esm",
  extensionsToTreatAsEsm: [".ts"],
  globals: { "ts-jest": { useESM: true } },
  // ... 100+ more lines of workarounds
};
```

### 2. Configuration Complexity Limits

**MANDATORY LIMITS**:

- Configuration file: **MAX 30 lines**
- Transform steps: **MAX 2**
- Module mappers: **MAX 5**
- Setup files: **MAX 1**
- Testing dependencies: **MAX 8**

**VIOLATION RESPONSE**: If limits exceeded, evaluate tool choice before adding complexity.

### 3. Single Module System Rule

**ENFORCE**: Consistent module system across entire codebase
**PROHIBITED**: Mixing CommonJS and ESM in testing setup

```typescript
// ✅ GOOD: Consistent ESM
import { test, expect } from "vitest";
import component from "./component";

// ❌ BAD: Mixed module systems
import { test } from "@jest/globals"; // ESM
const config = require("./config"); // CommonJS
```

## Mandatory Decision Framework

### Before Adopting Any Testing Framework:

#### 1. Stack Compatibility Check

```
Current Stack:
□ Build Tool: ___________
□ Module System: _______
□ TypeScript: __________
□ Node Version: ________

Framework Compatibility:
□ Native ES Module support?
□ Native TypeScript support?
□ Integrates with build tool?
□ Minimal configuration required?

RULE: Must answer YES to all compatibility questions
```

#### 2. Configuration Complexity Assessment

```
Estimated Configuration:
□ Lines of config: _____ (must be <30)
□ Transform steps: _____ (must be <3)
□ Module mappers: ______ (must be <5)
□ Dependencies: ________ (must be <8)

RULE: Must meet all complexity limits
```

#### 3. Performance Requirements

```
Current Performance:
□ Test execution time: _____ seconds
□ CI/CD test phase: _____ minutes

Target Performance:
□ Max test time: _____ seconds
□ Max CI time: _____ minutes

RULE: New framework must meet or exceed performance targets
```

## Framework Selection Rules

### Rule 1: Stack Compatibility + Constraint Analysis

```
IF: TypeScript + ESM + Vite + Node 18+ + No critical bugs
THEN: Consider Vitest
RATIONALE: Native compatibility, minimal config, superior performance

IF: TypeScript + ESM + Webpack + Complex config needs + Tinypool issues
THEN: Use Jest (optimized)
RATIONALE: Webpack compatibility, config flexibility, avoids critical bugs

IF: Legacy Stack + CommonJS + Webpack + Node <18
THEN: Use Jest (with modernization plan)
RATIONALE: Established compatibility, but plan modernization
```

### Rule 2: Configuration Complexity Threshold

```
IF: Configuration exceeds 30 lines
THEN: Evaluate different tool
RATIONALE: Complex config indicates tool mismatch

IF: Multiple transform pipelines required
THEN: Wrong tool for stack
RATIONALE: Modern tools handle transforms natively
```

### Rule 3: Performance Degradation Prevention

```
IF: Test execution time >30 seconds
THEN: Investigate tool performance characteristics
RATIONALE: Slow tests reduce developer productivity

IF: CI/CD test phase >5 minutes
THEN: Evaluate faster alternatives
RATIONALE: Slow CI impacts delivery velocity
```

## Prohibited Patterns

### ❌ NEVER DO THESE:

#### 1. Configuration Band-Aids

```javascript
// PROHIBITED: Adding complexity to fix compatibility
module.exports = {
  preset: "ts-jest/presets/default-esm",
  extensionsToTreatAsEsm: [".ts", ".tsx"],
  globals: { "ts-jest": { useESM: true } },
  transform: {
    /* complex transforms */
  },
  moduleNameMapper: {
    /* 20+ mappings */
  },
};
```

#### 2. Multiple Setup Files

```
// PROHIBITED: Multiple setup files
jest.setup.js
jest.setup.cjs
jest.setup.ts
setupTests.js
```

#### 3. Module System Mixing

```javascript
// PROHIBITED: Mixed module systems
import { test } from "@jest/globals"; // ESM
const config = require("./config"); // CommonJS
module.exports = {
  /* exports */
}; // CommonJS
export default something; // ESM
```

#### 4. Dependency Explosion

```json
// PROHIBITED: Too many testing dependencies
{
  "devDependencies": {
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0",
    "ts-jest": "^29.0.0",
    "babel-jest": "^29.0.0",
    "@babel/preset-env": "^7.0.0",
    "@babel/preset-react": "^7.0.0",
    "@babel/preset-typescript": "^7.0.0",
    "jest-environment-jsdom": "^29.0.0"
    // ... 10+ more jest-related dependencies
  }
}
```

## Mandatory Practices

### ✅ ALWAYS DO THESE:

#### 1. Minimal Configuration

```typescript
// REQUIRED: Start with minimal config
export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
  },
});
```

#### 2. Single Setup File

```typescript
// REQUIRED: One setup file per framework
// src/test/setup.ts
import "@testing-library/jest-dom";
```

#### 3. Consistent Module System

```typescript
// REQUIRED: Consistent ESM usage
import { test, expect } from "vitest";
import { render } from "@testing-library/react";
import Component from "./Component";
```

#### 4. Performance Monitoring

```typescript
// REQUIRED: Monitor test performance
const PERFORMANCE_LIMITS = {
  maxTestTime: 30000, // 30 seconds
  maxConfigLines: 30, // 30 lines
  maxDependencies: 8, // 8 test deps
};
```

## Enforcement Mechanisms

### 1. Pre-Commit Checks

```javascript
// Automated configuration validation
const validateTestConfig = () => {
  const issues = [];

  // Check configuration size
  const configLines = getConfigFileLineCount();
  if (configLines > 30) {
    issues.push(`❌ Configuration too large: ${configLines} lines (max: 30)`);
  }

  // Check dependency count
  const testDeps = getTestingDependencies();
  if (testDeps.length > 8) {
    issues.push(`❌ Too many test dependencies: ${testDeps.length} (max: 8)`);
  }

  // Check setup file count
  const setupFiles = getSetupFiles();
  if (setupFiles.length > 1) {
    issues.push(`❌ Multiple setup files found: ${setupFiles.length} (max: 1)`);
  }

  return issues;
};
```

### 2. Code Review Requirements

```markdown
Testing Configuration PR Checklist:

- [ ] Configuration file is <30 lines
- [ ] Only one setup file exists
- [ ] Module system is consistent
- [ ] Transform steps are <3
- [ ] Module mappers are <5
- [ ] All dependencies are necessary
- [ ] Performance impact measured
- [ ] Rationale documented
```

### 3. Performance Monitoring

```javascript
// CI/CD performance checks
const checkTestPerformance = () => {
  const testTime = getTestExecutionTime();
  const ciTime = getCITestPhaseTime();

  if (testTime > 30000) {
    throw new Error(`❌ Tests too slow: ${testTime}ms (max: 30000ms)`);
  }

  if (ciTime > 300000) {
    throw new Error(`❌ CI test phase too slow: ${ciTime}ms (max: 300000ms)`);
  }
};
```

## Emergency Procedures

### When Configuration Limits Are Exceeded:

#### 1. Immediate Response

```markdown
1. STOP adding more configuration complexity
2. Document current pain points
3. Evaluate alternative tools
4. Create proof-of-concept with simpler tool
5. Plan migration if alternative is better
```

#### 2. Tool Evaluation Process

```markdown
1. Assess current stack compatibility
2. Research modern alternatives
3. Create comparison matrix
4. Test with small subset of tests
5. Measure performance impact
6. Get team buy-in for migration
```

#### 3. Migration Execution

```markdown
1. Run frameworks in parallel
2. Migrate simple tests first
3. Update CI/CD gradually
4. Remove old framework dependencies
5. Update team documentation
```

## Success Metrics

### Configuration Health Indicators

```javascript
const healthMetrics = {
  configComplexity: configLines < 30,
  dependencyCount: testDeps.length < 8,
  testPerformance: testTime < 30000,
  setupSimplicity: setupFiles.length === 1,
  moduleConsistency: !hasMixedModuleSystems(),
};
```

### Team Productivity Indicators

```javascript
const productivityMetrics = {
  timeOnConfig: configTime < totalDevTime * 0.05, // <5%
  testWritingVelocity: testsPerWeek > baseline,
  developerSatisfaction: satisfaction > 8.0,
  onboardingTime: newDevTestTime < 1, // <1 day
};
```

## Documentation Requirements

### Decision Documentation

```markdown
Testing Framework Decision:

- Date: ****\_\_\_****
- Framework: ****\_\_\_****
- Rationale: ****\_\_\_****
- Complexity Score: \_\_\_/30 lines
- Performance Impact: ****\_\_\_****
- Migration Plan: ****\_\_\_****
```

### Configuration Documentation

```typescript
// REQUIRED: Document all configuration decisions
export default defineConfig({
  test: {
    // Environment needed for DOM testing
    environment: "jsdom",

    // Global test functions for convenience
    globals: true,

    // Single setup file for test utilities
    setupFiles: ["./src/test/setup.ts"],
  },
});
```

## Conclusion

This rule enforces discipline around testing configuration to prevent:

- Endless configuration loops
- Technical debt accumulation
- Developer frustration
- Performance degradation
- Team productivity loss

**Key Principle**: Choose tools that align with your stack naturally. If you're fighting your tools, the tools are wrong for your use case.

**Enforcement**: This rule is automatically applied to all testing-related code changes and configuration modifications.
