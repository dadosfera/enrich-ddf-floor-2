#!/bin/bash

# Start development environment for Enrich DDF Floor 2

echo "🚀 Starting Enrich DDF Floor 2 Development Environment"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first."
    echo "   https://python-poetry.org/docs/#installation"
    exit 1
fi

# Create directories if they don't exist
mkdir -p logs
mkdir -p config

# Create basic prometheus config if it doesn't exist
if [ ! -f "config/prometheus.yml" ]; then
    echo "📊 Creating basic Prometheus configuration..."
    cat > config/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'enrich-ddf-floor2'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
EOF
fi

# Create basic database init script if it doesn't exist
if [ ! -f "scripts/init-db.sql" ]; then
    echo "🗄️ Creating database initialization script..."
    cat > scripts/init-db.sql << EOF
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create basic tables will be handled by Alembic migrations
-- This file is for any additional database setup

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE enrich_ddf_floor2 TO postgres;
EOF
fi

echo "🐳 Starting Docker services..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are healthy
echo "🔍 Checking service health..."

# Check database
if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database not ready"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis not ready"
fi

echo ""
echo "🎉 Development environment is starting up!"
echo ""
echo "📋 Available services:"
echo "   • FastAPI App:    http://localhost:8000"
echo "   • API Docs:       http://localhost:8000/docs"
echo "   • Health Check:   http://localhost:8000/health"
echo "   • Flower UI:      http://localhost:5555"
echo "   • Prometheus:     http://localhost:9090"
echo "   • PostgreSQL:     localhost:5432"
echo "   • Redis:          localhost:6379"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f app"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"
echo ""
echo "✨ Happy coding!" 