#!/bin/bash
# scripts/enhance-compose-limits.sh
# Add resource limits to Docker Compose files

set -euo pipefail

COMPOSE_FILE=${1:-compose.yml}

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Compose file not found: $COMPOSE_FILE"
    exit 0
fi

# Create backup
cp "$COMPOSE_FILE" "$COMPOSE_FILE.bak.$(date +%Y%m%d_%H%M%S)"

# Check if resource limits already exist
if grep -q "mem_limit:" "$COMPOSE_FILE" && grep -q "cpus:" "$COMPOSE_FILE"; then
    echo "✅ Resource limits already present in $COMPOSE_FILE"
    exit 0
fi

# Use Python for YAML manipulation (more reliable than sed)
python3 << EOF
import yaml
import sys
import copy

try:
    with open('$COMPOSE_FILE', 'r') as f:
        compose = yaml.safe_load(f) or {}

    if 'services' not in compose:
        print("No services section found")
        sys.exit(0)

    modified = False

    # Default resource limits by service type
    defaults = {
        'backend': {'mem_limit': '512m', 'mem_reservation': '256m', 'cpus': '1.0'},
        'api': {'mem_limit': '512m', 'mem_reservation': '256m', 'cpus': '1.0'},
        'frontend': {'mem_limit': '768m', 'mem_reservation': '384m', 'cpus': '1.0'},
        'postgres': {'mem_limit': '1g', 'mem_reservation': '512m', 'cpus': '1.5'},
        'postgresql': {'mem_limit': '1g', 'mem_reservation': '512m', 'cpus': '1.5'},
        'redis': {'mem_limit': '256m', 'mem_reservation': '128m', 'cpus': '0.5'},
        'db': {'mem_limit': '1g', 'mem_reservation': '512m', 'cpus': '1.5'},
    }

    for service_name, service_config in compose['services'].items():
        if not isinstance(service_config, dict):
            continue

        # Skip if already has limits
        if 'mem_limit' in service_config or 'deploy' in service_config:
            continue

        # Determine service type
        service_type = 'backend'
        if 'frontend' in service_name.lower() or 'web' in service_name.lower():
            service_type = 'frontend'
        elif 'postgres' in service_name.lower() or 'db' in service_name.lower():
            service_type = 'postgres'
        elif 'redis' in service_name.lower():
            service_type = 'redis'
        elif 'api' in service_name.lower():
            service_type = 'api'

        limits = defaults.get(service_type, defaults['backend'])

        # Add resource limits
        service_config['mem_limit'] = limits['mem_limit']
        service_config['mem_reservation'] = limits['mem_reservation']
        service_config['cpus'] = limits['cpus']

        # Add restart policy if missing
        if 'restart' not in service_config:
            service_config['restart'] = 'unless-stopped'

        # Add logging if missing
        if 'logging' not in service_config:
            service_config['logging'] = {
                'driver': 'json-file',
                'options': {
                    'max-size': '10m',
                    'max-file': '3',
                    'compress': 'true'
                }
            }

        modified = True
        print(f"  ✅ Added limits to service: {service_name}")

    if modified:
        with open('$COMPOSE_FILE', 'w') as f:
            yaml.dump(compose, f, default_flow_style=False, sort_keys=False, width=120)
        print("✅ Compose file enhanced with resource limits")
    else:
        print("✅ All services already have resource limits")

except ImportError:
    print("⚠️  PyYAML not installed. Install with: pip install pyyaml")
    print("   Skipping automatic enhancement - manual review needed")
    sys.exit(0)
except Exception as e:
    print(f"⚠️  Error enhancing compose file: {e}")
    print("   Manual review needed")
    sys.exit(0)
EOF
