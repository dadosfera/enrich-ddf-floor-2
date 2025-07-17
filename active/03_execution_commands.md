# 🔧 Execution Commands - Enrich DDF Floor 2

## 🚀 Quick Start Commands

### Start the Application
```bash
# Activate virtual environment and start app
source venv/bin/activate && python3 main.py

# Alternative: Run with specific host/port
source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Run All Linters
```bash
# Run all linters in sequence
source venv/bin/activate && \
ruff check . && \
black --check . && \
isort --check-only . && \
flake8 . && \
mypy . && \
pylint main.py
```

### Fix Linting Issues
```bash
# Auto-fix formatting and import issues
source venv/bin/activate && \
black . && \
isort . && \
ruff check --fix .
```

### Run Tests
```bash
# Run all tests with coverage
source venv/bin/activate && pytest -v --cov=. --cov-report=html

# Run specific test file
source venv/bin/activate && pytest tests/unit/test_critical_endpoints.py -v

# Run tests with verbose output
source venv/bin/activate && pytest -v -s --tb=short
```

## 📊 Health Check Commands

### Check Application Status
```bash
# Health check endpoint
curl -X GET "http://localhost:8000/health"

# Root endpoint
curl -X GET "http://localhost:8000/"

# API documentation
curl -X GET "http://localhost:8000/docs"
```

### Database Health
```bash
# Check database connection
source venv/bin/activate && python3 -c "
from database.connection import get_db
from sqlalchemy import text
db = next(get_db())
result = db.execute(text('SELECT 1'))
print('Database connection: OK' if result else 'Database connection: FAILED')
"
```

## 🗄️ Database Commands

### Migration Operations
```bash
# Create new migration
source venv/bin/activate && alembic revision --autogenerate -m "Description of changes"

# Apply migrations
source venv/bin/activate && alembic upgrade head

# Rollback migration
source venv/bin/activate && alembic downgrade -1

# Check migration status
source venv/bin/activate && alembic current

# Show migration history
source venv/bin/activate && alembic history
```

### Database Reset
```bash
# Reset database (WARNING: Destructive)
rm -f app.db
source venv/bin/activate && alembic upgrade head
```

## 🧪 Testing Commands

### Test Categories
```bash
# Unit tests only
source venv/bin/activate && pytest tests/unit/ -v

# Integration tests only
source venv/bin/activate && pytest tests/integration/ -v

# End-to-end tests only
source venv/bin/activate && pytest tests/e2e/ -v

# Run tests with specific markers
source venv/bin/activate && pytest -m "critical" -v
```

### Test Coverage
```bash
# Generate coverage report
source venv/bin/activate && pytest --cov=. --cov-report=html --cov-report=term

# View coverage in browser
open htmlcov/index.html

# Generate coverage badge
source venv/bin/activate && coverage-badge -o coverage-badge.svg
```

### Performance Testing
```bash
# Load test with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Load test with wrk
wrk -t12 -c400 -d30s http://localhost:8000/health
```

## 🔍 Debugging Commands

### Application Debug
```bash
# Run with debug logging
source venv/bin/activate && python3 main.py --log-level debug

# Check application logs
tail -f logs/app.log

# Monitor application processes
ps aux | grep python
```

### Database Debug
```bash
# Connect to SQLite database
sqlite3 app.db

# List all tables
.tables

# Show table schema
.schema companies
.schema contacts
.schema products

# Query data
SELECT * FROM companies LIMIT 5;
```

### Network Debug
```bash
# Check if port is in use
lsof -i :8000

# Kill process on port
kill -9 $(lsof -t -i:8000)

# Check network connectivity
curl -v http://localhost:8000/health
```

## 🛠️ Development Commands

### Environment Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Quality
```bash
# Format code
source venv/bin/activate && black .

# Sort imports
source venv/bin/activate && isort .

# Check types
source venv/bin/activate && mypy .

# Security check
source venv/bin/activate && bandit -r .
```

### Documentation
```bash
# Generate API documentation
source venv/bin/activate && python3 -c "
import uvicorn
from main import app
import json
openapi_schema = app.openapi()
with open('openapi.json', 'w') as f:
    json.dump(openapi_schema, f, indent=2)
print('OpenAPI schema generated: openapi.json')
"

# View API docs
open http://localhost:8000/docs
```

## 🚀 Production Commands

### Docker Operations
```bash
# Build Docker image
docker build -t enrich-ddf-floor-2 .

# Run Docker container
docker run -p 8000:8000 enrich-ddf-floor-2

# Run with environment variables
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:pass@host/db enrich-ddf-floor-2

# Stop all containers
docker stop $(docker ps -q)
```

### Deployment
```bash
# Deploy with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Scale application
docker-compose up -d --scale app=3
```

## 📈 Monitoring Commands

### Application Metrics
```bash
# Check application metrics
curl http://localhost:8000/metrics

# Monitor memory usage
ps aux | grep python | awk '{print $6}' | awk '{sum+=$1} END {print "Memory usage:", sum/1024, "MB"}'

# Monitor CPU usage
top -p $(pgrep -f "python.*main.py")
```

### Log Analysis
```bash
# View recent logs
tail -n 100 logs/app.log

# Search for errors
grep -i error logs/app.log

# Count requests by endpoint
grep "GET\|POST\|PUT\|DELETE" logs/app.log | awk '{print $7}' | sort | uniq -c
```

## 🔧 Maintenance Commands

### Backup Database
```bash
# Backup SQLite database
cp app.db app.db.backup.$(date +%Y%m%d_%H%M%S)

# Backup with compression
sqlite3 app.db ".backup 'backup_$(date +%Y%m%d_%H%M%S).db'"
```

### Cleanup
```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove test cache
rm -rf .pytest_cache/

# Remove coverage reports
rm -rf htmlcov/
rm -f .coverage

# Remove temporary files
find . -name "*.tmp" -delete
find . -name "*.log" -delete
```

### Update Dependencies
```bash
# Update all packages
source venv/bin/activate && pip install --upgrade -r requirements.txt

# Check for outdated packages
source venv/bin/activate && pip list --outdated

# Update specific package
source venv/bin/activate && pip install --upgrade fastapi
```

## 🚨 Emergency Commands

### Application Recovery
```bash
# Kill all Python processes
pkill -f python

# Restart application
source venv/bin/activate && python3 main.py

# Reset database and restart
rm -f app.db && source venv/bin/activate && alembic upgrade head && python3 main.py
```

### System Recovery
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check system load
uptime

# Restart system services
sudo systemctl restart nginx
```

## 📋 One-Liner Commands

### Quick Health Check
```bash
# Complete health check
source venv/bin/activate && \
echo "=== LINTERS ===" && ruff check . && \
echo "=== TESTS ===" && pytest --tb=short -q && \
echo "=== APP ===" && timeout 10s python3 main.py &
```

### Development Workflow
```bash
# Complete development cycle
source venv/bin/activate && \
black . && isort . && ruff check --fix . && \
pytest -v --cov=. && \
python3 main.py
```

### Production Deployment
```bash
# Complete production deployment
docker build -t enrich-ddf-floor-2 . && \
docker stop enrich-ddf-floor-2 || true && \
docker rm enrich-ddf-floor-2 || true && \
docker run -d --name enrich-ddf-floor-2 -p 8000:8000 enrich-ddf-floor-2
```

## 📝 Notes

### Environment Variables
```bash
# Set environment variables
export DATABASE_URL="sqlite:///./app.db"
export DEBUG="True"
export LOG_LEVEL="INFO"
export SECRET_KEY="your-secret-key-here"
```

### Common Issues
- **Port already in use**: `lsof -ti:8000 | xargs kill -9`
- **Database locked**: Restart application
- **Import errors**: Check virtual environment activation
- **Test failures**: Check database state and test data

### Performance Tips
- Use `uvicorn` with `--workers` for production
- Enable database connection pooling
- Use async operations where possible
- Monitor memory usage regularly 