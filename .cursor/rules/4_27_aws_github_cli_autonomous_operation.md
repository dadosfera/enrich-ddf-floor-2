# AWS CLI and GitHub CLI Autonomous Operation Rule

## Priority
P1 (Critical): Must always be followed for AWS and GitHub CLI operations

## Core Principle
**AI agents must execute CLI commands autonomously without getting stuck on pagination, interactive prompts, or blocking operations**

## Mandatory AWS CLI Flags

### **Always Required Flags**
```bash
# REQUIRED for all AWS CLI commands
--no-paginate           # Disable pagination
--no-cli-pager          # Disable interactive pager
--output json           # Structured output (unless specific format needed)
--region us-east-1      # Explicit region (or from config)
```

### **Query and Filtering**
```bash
# Use JMESPath queries to limit output
--query 'Items[0:10]'                    # Limit results
--query 'Stacks[?StackStatus!=`DELETE_COMPLETE`]'  # Filter results
--query 'data[0].{id:id,name:name}'      # Select specific fields
```

### **Error Handling**
```bash
# Redirect stderr and handle errors properly
command 2>&1 || echo "Command failed with exit code $?"
```

## Mandatory GitHub CLI Flags

### **Always Required Flags**
```bash
# REQUIRED for all GitHub CLI commands
--json                  # JSON output for parsing
--limit 50              # Limit results to prevent overwhelming output
--repo owner/repo       # Explicit repo when needed
```

### **Non-Interactive Operations**
```bash
# Avoid interactive prompts
gh auth status --hostname github.com 2>/dev/null || echo "Not authenticated"
gh repo create --public --confirm        # Auto-confirm operations
```

## Command Pattern Examples

### **AWS CloudFormation**
```bash
# ✅ CORRECT: Autonomous template validation
aws cloudformation validate-template \
  --template-body file://template.yaml \
  --no-paginate \
  --no-cli-pager \
  --output json 2>&1

# ✅ CORRECT: List stacks with filtering
aws cloudformation list-stacks \
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE \
  --no-paginate \
  --no-cli-pager \
  --query 'StackSummaries[0:20].{Name:StackName,Status:StackStatus}' \
  --output json

# ❌ WRONG: Will get stuck on pagination
aws cloudformation list-stacks
```

### **AWS EC2**
```bash
# ✅ CORRECT: List instances autonomously
aws ec2 describe-instances \
  --no-paginate \
  --no-cli-pager \
  --query 'Reservations[].Instances[?State.Name==`running`].{Id:InstanceId,Type:InstanceType}' \
  --output json

# ✅ CORRECT: Get VPC info with limits
aws ec2 describe-vpcs \
  --no-paginate \
  --no-cli-pager \
  --max-items 10 \
  --output json
```

### **GitHub CLI**
```bash
# ✅ CORRECT: List repos autonomously
gh repo list --json name,visibility --limit 20

# ✅ CORRECT: Create issue non-interactively
gh issue create --title "Bug report" --body "Description" --repo owner/repo

# ❌ WRONG: Will prompt for input
gh repo create
```

## Error Handling Patterns

### **AWS CLI Error Handling**
```bash
# Pattern 1: Capture and handle errors
if ! aws sts get-caller-identity --no-paginate --no-cli-pager --output json >/dev/null 2>&1; then
  echo "AWS authentication failed"
  exit 1
fi

# Pattern 2: Conditional execution
aws cloudformation describe-stacks \
  --stack-name my-stack \
  --no-paginate \
  --no-cli-pager \
  --output json 2>/dev/null || echo "Stack not found"

# Pattern 3: Timeout with error handling
timeout 30s aws cloudformation validate-template \
  --template-body file://template.yaml \
  --no-paginate \
  --no-cli-pager \
  --output json 2>&1 || echo "Validation failed or timed out"
```

### **GitHub CLI Error Handling**
```bash
# Pattern 1: Check authentication
if ! gh auth status --hostname github.com >/dev/null 2>&1; then
  echo "GitHub authentication required"
  exit 1
fi

# Pattern 2: Safe repo operations
gh repo view owner/repo --json name 2>/dev/null || echo "Repository not found"
```

## Autonomous Operation Checklist

### **Pre-Command Validation**
- [ ] Add `--no-paginate` and `--no-cli-pager` to AWS commands
- [ ] Add `--json` and `--limit` to GitHub commands
- [ ] Include timeout for long-running operations
- [ ] Add error handling with `2>&1` or `2>/dev/null`
- [ ] Use `--query` to limit AWS output size

### **During Execution**
- [ ] Monitor for hanging commands (use timeouts)
- [ ] Capture both stdout and stderr
- [ ] Provide meaningful error messages
- [ ] Continue execution even if non-critical commands fail

### **Post-Command Processing**
- [ ] Parse JSON output programmatically
- [ ] Log command results for debugging
- [ ] Validate expected outcomes
- [ ] Clean up temporary resources if needed

## Common Failure Patterns to Avoid

### **❌ Blocking Operations**
```bash
# These will hang or prompt for input
aws cloudformation list-stacks                    # Pagination
gh repo create                                    # Interactive prompts
aws logs tail /aws/lambda/function                # Streaming output
```

### **✅ Autonomous Alternatives**
```bash
# Non-blocking equivalents
aws cloudformation list-stacks --no-paginate --no-cli-pager --max-items 20
gh repo create --public --confirm
aws logs describe-log-streams --log-group-name /aws/lambda/function --no-paginate
```

## Integration with Async Command Pattern

### **Long-Running Operations**
```bash
# Start deployment in background
nohup aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-stack \
  --no-paginate \
  --no-cli-pager \
  --capabilities CAPABILITY_IAM > deployment.log 2>&1 &

DEPLOY_PID=$!
echo "Deployment started with PID: $DEPLOY_PID"

# Check status periodically
while kill -0 $DEPLOY_PID 2>/dev/null; do
  echo "Deployment still running..."
  sleep 30
done
```

## Configuration Management

### **AWS CLI Configuration**
```bash
# Set default configuration to avoid interactive prompts
aws configure set default.region us-east-1
aws configure set default.output json
aws configure set default.cli_pager ""
aws configure set default.cli_auto_prompt off
```

### **GitHub CLI Configuration**
```bash
# Set non-interactive defaults
gh config set editor ""
gh config set prompt disabled
gh config set pager cat
```

## Testing and Validation

### **Autonomous Testing Pattern**
```bash
# Test AWS connectivity
echo "Testing AWS connectivity..."
if aws sts get-caller-identity --no-paginate --no-cli-pager --output json >/dev/null 2>&1; then
  echo "✅ AWS authentication successful"
else
  echo "❌ AWS authentication failed"
fi

# Test GitHub connectivity
echo "Testing GitHub connectivity..."
if gh auth status --hostname github.com >/dev/null 2>&1; then
  echo "✅ GitHub authentication successful"
else
  echo "❌ GitHub authentication failed"
fi
```

## Emergency Recovery

### **When Commands Get Stuck**
```bash
# Kill hanging processes
pkill -f "aws cloudformation"
pkill -f "gh "

# Reset CLI state
unset AWS_PAGER
unset GH_PAGER
```

## Enforcement

### **Pre-Execution Checklist**
Before executing any AWS or GitHub CLI command, AI agents must:
1. Verify all required flags are present
2. Confirm timeout is set for long operations
3. Ensure error handling is in place
4. Test command syntax with `--help` if uncertain

### **Monitoring Requirements**
- Log all CLI commands executed
- Track command execution time
- Monitor for hanging processes
- Report failures with context

---

## Summary

**NEVER execute AWS or GitHub CLI commands without:**
- `--no-paginate --no-cli-pager` (AWS)
- `--json --limit N` (GitHub)
- Proper error handling (`2>&1` or `2>/dev/null`)
- Timeouts for potentially long operations
- Autonomous operation without user interaction

This rule ensures AI agents can operate CLI tools reliably without getting stuck or requiring user intervention.
