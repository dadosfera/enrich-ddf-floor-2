#!/bin/bash
# Development Server Management Script
# Enrich DDF Floor 2 - Local development server utilities

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
PID_FILE="${PROJECT_ROOT}/.dev-server.pid"
LOG_FILE="${PROJECT_ROOT}/dev-server.log"

cd "${PROJECT_ROOT}"

# Function to display usage
usage() {
    echo -e "${BLUE}Development Server Management${NC}"
    echo "Usage: $0 {start|stop|restart|status|logs|health}"
    echo ""
    echo "Commands:"
    echo "  start   - Start the development server"
    echo "  stop    - Stop the development server"
    echo "  restart - Restart the development server"
    echo "  status  - Show server status"
    echo "  logs    - Show server logs"
    echo "  health  - Check server health"
    echo ""
}

# Function to check if server is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        else
            # Remove stale PID file
            rm -f "$PID_FILE"
            return 1
        fi
    else
        return 1
    fi
}

# Function to start the server
start_server() {
    if is_running; then
        echo -e "${YELLOW}⚠️  Server is already running (PID: $(cat $PID_FILE))${NC}"
        return 1
    fi

    echo -e "${BLUE}🚀 Starting development server...${NC}"
    
    # Check if dependencies are installed
    if ! poetry show > /dev/null 2>&1; then
        echo -e "${RED}❌ Poetry dependencies not found. Run tools/development/setup.sh first${NC}"
        return 1
    fi

    # Start database services if docker-compose is available
    if command -v docker-compose > /dev/null 2>&1 && [ -f "docker-compose.yml" ]; then
        echo -e "${CYAN}📋 Starting database services...${NC}"
        docker-compose up -d db redis
        sleep 5
    fi

    # Start the FastAPI server
    echo -e "${CYAN}📋 Starting FastAPI application...${NC}"
    poetry run uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload \
        --reload-exclude="*.log" \
        --reload-exclude="*.pid" \
        --log-level info \
        > "$LOG_FILE" 2>&1 &
    
    SERVER_PID=$!
    echo $SERVER_PID > "$PID_FILE"
    
    # Wait a moment and check if server started successfully
    sleep 3
    
    if is_running; then
        echo -e "${GREEN}✅ Development server started successfully${NC}"
        echo -e "   PID: $SERVER_PID"
        echo -e "   URL: http://localhost:8000"
        echo -e "   Docs: http://localhost:8000/docs"
        echo -e "   Logs: $LOG_FILE"
    else
        echo -e "${RED}❌ Failed to start development server${NC}"
        echo -e "Check logs: $LOG_FILE"
        return 1
    fi
}

# Function to stop the server
stop_server() {
    if ! is_running; then
        echo -e "${YELLOW}⚠️  Server is not running${NC}"
        return 1
    fi

    PID=$(cat "$PID_FILE")
    echo -e "${BLUE}🛑 Stopping development server (PID: $PID)...${NC}"
    
    # Try graceful shutdown first
    kill "$PID" 2>/dev/null || true
    
    # Wait for graceful shutdown
    sleep 3
    
    # Force kill if still running
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Forcing server shutdown...${NC}"
        kill -9 "$PID" 2>/dev/null || true
    fi
    
    rm -f "$PID_FILE"
    echo -e "${GREEN}✅ Development server stopped${NC}"
}

# Function to restart the server
restart_server() {
    echo -e "${BLUE}🔄 Restarting development server...${NC}"
    stop_server
    sleep 2
    start_server
}

# Function to show server status
show_status() {
    echo -e "${BLUE}📊 Development Server Status${NC}"
    echo "================================"
    
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "Status: ${GREEN}Running${NC}"
        echo -e "PID: $PID"
        echo -e "URL: http://localhost:8000"
        echo -e "Started: $(ps -p $PID -o lstart= 2>/dev/null || echo 'Unknown')"
        
        # Check if server is responding
        if command -v curl > /dev/null 2>&1; then
            if curl -s http://localhost:8000/health > /dev/null 2>&1; then
                echo -e "Health: ${GREEN}Healthy${NC}"
            else
                echo -e "Health: ${YELLOW}Not responding${NC}"
            fi
        fi
    else
        echo -e "Status: ${RED}Not running${NC}"
    fi
    
    # Show docker services status
    if command -v docker-compose > /dev/null 2>&1 && [ -f "docker-compose.yml" ]; then
        echo ""
        echo -e "${BLUE}Docker Services Status${NC}"
        echo "======================"
        docker-compose ps
    fi
}

# Function to show logs
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}📋 Development Server Logs${NC}"
        echo "=========================="
        tail -f "$LOG_FILE"
    else
        echo -e "${YELLOW}⚠️  No log file found${NC}"
    fi
}

# Function to check health
check_health() {
    echo -e "${BLUE}🔍 Health Check${NC}"
    echo "==============="
    
    if ! is_running; then
        echo -e "Server: ${RED}Not running${NC}"
        return 1
    fi
    
    # Check server response
    if command -v curl > /dev/null 2>&1; then
        echo -e "${CYAN}Checking server response...${NC}"
        
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
            echo -e "API Health: ${GREEN}OK${NC}"
        else
            echo -e "API Health: ${RED}Failed${NC}"
        fi
        
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q "200"; then
            echo -e "API Docs: ${GREEN}OK${NC}"
        else
            echo -e "API Docs: ${RED}Failed${NC}"
        fi
    else
        echo -e "${YELLOW}curl not available for health check${NC}"
    fi
    
    # Check database connection (if docker services are running)
    if command -v docker-compose > /dev/null 2>&1; then
        echo -e "${CYAN}Checking database services...${NC}"
        
        if docker-compose ps | grep -q "db.*Up"; then
            echo -e "Database: ${GREEN}Running${NC}"
        else
            echo -e "Database: ${RED}Not running${NC}"
        fi
        
        if docker-compose ps | grep -q "redis.*Up"; then
            echo -e "Redis: ${GREEN}Running${NC}"
        else
            echo -e "Redis: ${RED}Not running${NC}"
        fi
    fi
}

# Main command handling
case "${1:-}" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    health)
        check_health
        ;;
    *)
        usage
        exit 1
        ;;
esac 