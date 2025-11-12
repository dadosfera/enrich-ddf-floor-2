# Cloud Cost Control Scripts

Automated scripts for managing cloud infrastructure costs by stopping/starting non-production instances.

## Scripts

- **stop-nonprod.sh** - Stop non-production instances (dry-run by default)
- **start-nonprod.sh** - Start non-production instances
- **report-nightly.sh** - Generate nightly cost reports

## Usage

### Stop Non-Production Instances

```bash
# Dry-run (default - safe)
bash scripts/cost/stop-nonprod.sh

# Actually stop instances (requires explicit false flag)
bash scripts/cost/stop-nonprod.sh false
```

### Start Non-Production Instances

```bash
bash scripts/cost/start-nonprod.sh
```

### Generate Cost Report

```bash
bash scripts/cost/report-nightly.sh
```

## Makefile Targets

```bash
make cloud-stop-night          # Dry-run stop
make cloud-stop-night-force    # Actually stop instances
make cloud-start-morning       # Start instances
make cloud-cost-report         # Generate cost report
```

## Cron Automation

Add to crontab for automated execution:

```bash
# Stop non-prod at 10 PM
0 22 * * * cd ~/local_repos/<repo> && make cloud-stop-night-force

# Start non-prod at 7 AM
0 7 * * * cd ~/local_repos/<repo> && make cloud-start-morning

# Generate cost report at midnight
0 0 * * * cd ~/local_repos/<repo> && make cloud-cost-report
```

## Prerequisites

- OCI CLI installed and configured
- OCI_ACTIVE_TENANCY or OCI_CONFIG_FILE environment variable set
- OCI_COMPARTMENT_ID environment variable set (for instance queries)
- Appropriate OCI permissions (compute.instance.manage)

## Safety Features

- **Dry-run by default** - Prevents accidental stops
- **Logging** - All actions logged to `logs/cost-control.log`
- **Error handling** - Continues processing even if individual instances fail
- **Status checks** - Only processes instances in appropriate states

## Environment Variables

- `OCI_ACTIVE_TENANCY` - OCI tenancy OCID
- `OCI_CONFIG_FILE` - Path to OCI config file
- `OCI_COMPARTMENT_ID` - Compartment OCID for instance queries
- `LOG_DIR` - Log directory (default: `logs`)
