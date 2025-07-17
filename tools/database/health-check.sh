#!/bin/bash
# Database Health Check Script
# Enrich DDF Floor 2 - Database monitoring and health verification

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"

cd "${PROJECT_ROOT}"

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

# Default database configuration
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5433}
DB_NAME=${DB_NAME:-enrich_ddf_floor2}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}

# Redis configuration
REDIS_HOST=${REDIS_HOST:-localhost}
REDIS_PORT=${REDIS_PORT:-6379}

echo -e "${BLUE}🔍 Database Health Check - Enrich DDF Floor 2${NC}"
echo "=============================================="
echo "Timestamp: $(date)"
echo ""

# Function to check command availability
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to log step
log_step() {
    echo -e "${CYAN}📋 $1${NC}"
}

# Function to log success
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to log warning
log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to log error
log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to test PostgreSQL connection
test_postgres_connection() {
    log_step "Testing PostgreSQL connection..."
    
    if command_exists psql; then
        # Test connection using psql
        if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
            log_success "PostgreSQL connection successful"
            return 0
        else
            log_error "PostgreSQL connection failed"
            return 1
        fi
    elif command_exists docker; then
        # Test connection using docker
        if docker run --rm postgres:15-alpine psql "postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
            log_success "PostgreSQL connection successful (via Docker)"
            return 0
        else
            log_error "PostgreSQL connection failed (via Docker)"
            return 1
        fi
    else
        log_warning "No PostgreSQL client available for testing"
        return 1
    fi
}

# Function to test Redis connection
test_redis_connection() {
    log_step "Testing Redis connection..."
    
    if command_exists redis-cli; then
        # Test connection using redis-cli
        if redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping > /dev/null 2>&1; then
            log_success "Redis connection successful"
            return 0
        else
            log_error "Redis connection failed"
            return 1
        fi
    elif command_exists docker; then
        # Test connection using docker
        if docker run --rm redis:7-alpine redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping > /dev/null 2>&1; then
            log_success "Redis connection successful (via Docker)"
            return 0
        else
            log_error "Redis connection failed (via Docker)"
            return 1
        fi
    else
        log_warning "No Redis client available for testing"
        return 1
    fi
}

# Function to check database size and basic stats
check_database_stats() {
    log_step "Checking database statistics..."
    
    if command_exists psql; then
        echo -e "${CYAN}Database Size and Statistics:${NC}"
        
        # Database size
        DB_SIZE=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" 2>/dev/null | tr -d ' ')
        
        if [ -n "$DB_SIZE" ]; then
            echo "  Database Size: $DB_SIZE"
        else
            log_warning "Could not retrieve database size"
        fi
        
        # Connection count
        CONN_COUNT=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null | tr -d ' ')
        
        if [ -n "$CONN_COUNT" ]; then
            echo "  Active Connections: $CONN_COUNT"
        else
            log_warning "Could not retrieve connection count"
        fi
        
        # Table count
        TABLE_COUNT=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ')
        
        if [ -n "$TABLE_COUNT" ]; then
            echo "  Tables: $TABLE_COUNT"
        else
            log_warning "Could not retrieve table count"
        fi
        
        log_success "Database statistics retrieved"
    else
        log_warning "PostgreSQL client not available for statistics"
    fi
}

# Function to check Redis stats
check_redis_stats() {
    log_step "Checking Redis statistics..."
    
    if command_exists redis-cli; then
        echo -e "${CYAN}Redis Statistics:${NC}"
        
        # Redis info
        REDIS_INFO=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" INFO memory 2>/dev/null)
        
        if [ -n "$REDIS_INFO" ]; then
            # Extract memory usage
            USED_MEMORY=$(echo "$REDIS_INFO" | grep "used_memory_human:" | cut -d: -f2 | tr -d '\r')
            if [ -n "$USED_MEMORY" ]; then
                echo "  Memory Used: $USED_MEMORY"
            fi
            
            # Extract key count
            KEY_COUNT=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" DBSIZE 2>/dev/null)
            if [ -n "$KEY_COUNT" ]; then
                echo "  Keys: $KEY_COUNT"
            fi
            
            log_success "Redis statistics retrieved"
        else
            log_warning "Could not retrieve Redis statistics"
        fi
    else
        log_warning "Redis client not available for statistics"
    fi
}

# Function to check Docker services
check_docker_services() {
    log_step "Checking Docker services..."
    
    if command_exists docker-compose && [ -f "docker-compose.yml" ]; then
        echo -e "${CYAN}Docker Services Status:${NC}"
        
        # Check database service
        if docker-compose ps db | grep -q "Up"; then
            log_success "Database container is running"
        else
            log_error "Database container is not running"
        fi
        
        # Check Redis service
        if docker-compose ps redis | grep -q "Up"; then
            log_success "Redis container is running"
        else
            log_error "Redis container is not running"
        fi
        
        # Show full status
        echo ""
        docker-compose ps
    else
        log_warning "Docker Compose not available or docker-compose.yml not found"
    fi
}

# Function to test application database connectivity
test_app_connection() {
    log_step "Testing application database connectivity..."
    
    if [ -f "pyproject.toml" ] && command_exists poetry; then
        # Test using the application's database models
        if poetry run python -c "
import asyncio
from app.core.config import settings
from app.models.base import Base
from sqlalchemy.ext.asyncio import create_async_engine

async def test_connection():
    try:
        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.begin() as conn:
            await conn.execute('SELECT 1')
        await engine.dispose()
        print('SUCCESS')
    except Exception as e:
        print(f'ERROR: {e}')

asyncio.run(test_connection())
" 2>/dev/null | grep -q "SUCCESS"; then
            log_success "Application database connection successful"
        else
            log_error "Application database connection failed"
        fi
    else
        log_warning "Cannot test application connection (Poetry/pyproject.toml not available)"
    fi
}

# Function to run performance tests
run_performance_tests() {
    log_step "Running basic performance tests..."
    
    if command_exists psql; then
        echo -e "${CYAN}Database Performance:${NC}"
        
        # Simple query performance test
        START_TIME=$(date +%s.%N)
        PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT count(*) FROM information_schema.tables;" > /dev/null 2>&1
        END_TIME=$(date +%s.%N)
        
        QUERY_TIME=$(echo "$END_TIME - $START_TIME" | bc 2>/dev/null || echo "N/A")
        if [ "$QUERY_TIME" != "N/A" ]; then
            echo "  Simple Query Time: ${QUERY_TIME}s"
        fi
        
        log_success "Performance tests completed"
    else
        log_warning "Cannot run performance tests (PostgreSQL client not available)"
    fi
}

# Main health check execution
HEALTH_STATUS=0

echo -e "${BLUE}1. Database Connection Tests${NC}"
echo "============================="
if ! test_postgres_connection; then
    HEALTH_STATUS=1
fi

if ! test_redis_connection; then
    HEALTH_STATUS=1
fi

echo ""
echo -e "${BLUE}2. Database Statistics${NC}"
echo "======================"
check_database_stats
check_redis_stats

echo ""
echo -e "${BLUE}3. Service Status${NC}"
echo "================="
check_docker_services

echo ""
echo -e "${BLUE}4. Application Integration${NC}"
echo "=========================="
test_app_connection

echo ""
echo -e "${BLUE}5. Performance Tests${NC}"
echo "===================="
run_performance_tests

# Summary
echo ""
echo -e "${BLUE}📊 Health Check Summary${NC}"
echo "======================="
echo "Timestamp: $(date)"

if [ $HEALTH_STATUS -eq 0 ]; then
    echo -e "Overall Status: ${GREEN}HEALTHY${NC}"
    echo -e "All database services are functioning properly"
else
    echo -e "Overall Status: ${RED}UNHEALTHY${NC}"
    echo -e "Some database services have issues - check logs above"
fi

echo ""
echo -e "${BLUE}Configuration${NC}"
echo "============="
echo "Database Host: $DB_HOST:$DB_PORT"
echo "Database Name: $DB_NAME"
echo "Redis Host: $REDIS_HOST:$REDIS_PORT"

exit $HEALTH_STATUS 