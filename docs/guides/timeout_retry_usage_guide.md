# Timeout & Retry Usage Guide

## Overview
This enhanced linting system includes robust timeout and retry functionality to ensure reliable operation even when dealing with large codebases or temporary network issues.

## Features

### ⏱️ Timeout Protection
- **Default Timeout**: 120 seconds per operation
- **Configurable**: Can be adjusted via `TIMEOUT_DURATION` variable
- **Prevents Hanging**: Automatically kills long-running processes
- **Clean Exit**: Provides clear error messages on timeout

### 🔄 Retry Logic
- **Max Retries**: 3 attempts per operation (configurable)
- **Smart Delays**: 5-second delays between retry attempts
- **Exponential Backoff**: Optional exponential delay increase
- **Graceful Degradation**: Continues with remaining operations

### 🛡️ Error Handling
- **Comprehensive Logging**: Color-coded output for easy monitoring
- **Detailed Error Messages**: Clear indication of timeout vs. failure
- **Partial Success**: Continues processing even if some operations fail
- **Cleanup**: Automatic cleanup of temporary files

## Usage

### Basic Usage
```bash
./lint_with_timeout_retry.sh
```

### Configuration
Edit the script to modify these variables:
```bash
MAX_RETRIES=3          # Number of retry attempts
TIMEOUT_DURATION=120   # Timeout in seconds
RETRY_DELAY=5          # Delay between retries
```

### Expected Output
```
========================================
🔍 Robust Linting with Timeout & Retry
========================================
[INFO] Configuration: Max Retries=3, Timeout=120s
[INFO] Attempt 1/3: Python import sorting
[INFO] Executing: Python import sorting (timeout: 120s)
[SUCCESS] Python import sorting completed
[INFO] Attempt 1/3: Python formatting
[SUCCESS] Python formatting completed
========================================
[SUCCESS] Linting completed with timeout and retry protection
========================================
```

## Integration with Existing Pipeline

### Replace Existing Commands
Replace individual linting commands with the robust version:

**Before:**
```bash
ruff check --select I --fix .
ruff format .
```

**After:**
```bash
./lint_with_timeout_retry.sh
```

### CI/CD Integration
Add to your CI/CD pipeline for reliable automated linting:

```yaml
# GitHub Actions example
- name: Run Linting with Timeout & Retry
  run: |
    chmod +x lint_with_timeout_retry.sh
    ./lint_with_timeout_retry.sh
  timeout-minutes: 10
```

## Benefits

### Reliability
- **Handles Network Issues**: Automatic retry for network-dependent operations
- **Prevents Build Failures**: Timeout protection prevents hanging builds
- **Graceful Degradation**: Continues processing even with partial failures

### Performance
- **Optimized Timeouts**: Prevents unnecessary waiting
- **Smart Retries**: Only retries operations that are likely to succeed
- **Parallel Processing**: Can be extended to run operations in parallel

### Maintainability
- **Centralized Configuration**: All timeout/retry settings in one place
- **Comprehensive Logging**: Easy to debug and monitor
- **Modular Design**: Easy to extend with additional operations

## Troubleshooting

### Common Issues

**1. Timeout Too Short**
```bash
# Increase timeout duration
TIMEOUT_DURATION=300  # 5 minutes
```

**2. Too Many Retries**
```bash
# Reduce retry attempts for faster failure
MAX_RETRIES=2
```

**3. Network Connectivity Issues**
```bash
# Increase retry delay for network recovery
RETRY_DELAY=10
```

### Debug Mode
Add debug logging by modifying the script:
```bash
# Add this line after set -euo pipefail
set -x  # Enable debug mode
```

## Advanced Configuration

### Custom Timeout per Operation
```bash
# Different timeouts for different operations
run_with_retry "ruff check ." 3 60 "Quick check"     # 1 minute
run_with_retry "ruff format ." 3 300 "Full format"  # 5 minutes
```

### Conditional Retry
```bash
# Only retry on specific error codes
run_with_retry "npm run lint" 3 120 "NPM lint" || {
    if [ $? -eq 137 ]; then  # OOM killed
        log_error "Process killed due to memory issues"
        exit 1
    fi
}
```

## Best Practices

1. **Monitor Resource Usage**: Adjust timeouts based on system resources
2. **Log Analysis**: Regularly review logs to identify problematic operations
3. **Progressive Timeouts**: Use shorter timeouts for quick operations
4. **Alert on Failures**: Set up notifications for repeated failures
5. **Regular Updates**: Keep retry logic updated with new operation types

## Comparison with Original Pipeline

| Feature | Original | With Timeout & Retry |
|---------|----------|---------------------|
| **Reliability** | Moderate | High |
| **Network Issues** | Fails | Auto-retry |
| **Hanging Commands** | Manual intervention | Auto-timeout |
| **Error Recovery** | Limited | Comprehensive |
| **Logging** | Basic | Detailed |
| **CI/CD Ready** | Partial | Full |

This enhanced system provides enterprise-grade reliability for automated linting operations while maintaining the simplicity and effectiveness of the original pipeline.
