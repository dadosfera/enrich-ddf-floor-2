# Getting Started Guide

**Welcome to Enrich DDF Floor 2!** This guide will help you get up and running quickly.

## 🚀 Quick Start (5 minutes)

### Prerequisites

- **Python 3.11+** (check with `python3 --version`)
- **Node.js 20+** (check with `node --version`)
- **npm** (comes with Node.js)
- **Git**

### Step 1: Clone the Repository

```bash
git clone https://github.com/dadosfera/enrich-ddf-floor-2.git
cd enrich-ddf-floor-2
```

### Step 2: Install Dependencies

```bash
# Install all dependencies (backend + frontend)
make install
```

This will:
- Create a Python virtual environment (`venv/`)
- Install Python dependencies from `requirements-minimal.txt`
- Install Node.js dependencies for the frontend

### Step 3: Set Up Pre-commit Hooks

```bash
pre-commit install
```

This ensures code quality checks run automatically before commits.

### Step 4: Run the Application

```bash
# Start both backend and frontend
make run
```

**That's it!** The application is now running:
- **Frontend**: http://127.0.0.1:5173 (or random port > 15000 in dev mode)
- **Backend API**: http://127.0.0.1:8247 (or random port > 15000 in dev mode)
- **API Documentation**: http://127.0.0.1:{PORT}/docs (check console output for actual port)

**Note**: Port configuration is centralized and environment-aware. In development mode, random ports > 15000 are used to prevent conflicts. See [Port Configuration](../../README.md#-port-configuration) for details.

---

## 📚 Understanding the Application

### What is Enrich DDF Floor 2?

A **unified data enrichment platform** that aggregates features from multiple DDF enrichment services:

- **Company Data**: Enrich company information from multiple sources
- **Contact Data**: Find and enrich contact information
- **Product Data**: Classify and enrich product information
- **People Data**: Enrich people profiles and professional data

### Architecture Overview

```
┌─────────────┐
│  Frontend   │  React + TypeScript + Vite
│  (Dynamic)  │  Material-UI components
│             │  Port: 5173 (prod), 5174 (staging), random >15000 (dev)
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│   Backend   │  FastAPI (Python)
│  (Dynamic)  │  SQLAlchemy + SQLite
│             │  Port: 8247 (prod), 8248 (staging), random >15000 (dev)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Database   │  SQLite (dev) / PostgreSQL (prod)
│  + External │  Third-party enrichment APIs
│   APIs      │
└─────────────┘
```

---

## 🛠️ Common Commands

### Development

| Command | Description |
|---------|-------------|
| `make run` | Start both frontend and backend |
| `make backend` | Start only backend server |
| `make frontend` | Start only frontend server |
| `make dev` | Start development environment |
| `make install` | Install all dependencies |

### Testing & Quality

| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make lint` | Run linting checks |
| `make format` | Format code automatically |
| `make check` | Run lint + test |

### Building

| Command | Description |
|---------|-------------|
| `make build` | Build frontend for production |
| `make clean` | Clean build artifacts |

### Docker (Optional)

| Command | Description |
|---------|-------------|
| `make compose-up` | Start with Docker Compose |
| `make compose-down` | Stop Docker Compose services |
| `make compose-validate` | Validate compose.yml |

---

## 📁 Project Structure

```
enrich-ddf-floor-2/
├── frontend/          # React frontend application
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── package.json  # Frontend dependencies
│
├── backend/          # Python backend (root level)
│   ├── main.py       # FastAPI application entry point
│   ├── config.py     # Configuration settings
│   ├── database/     # Database models and connection
│   ├── core/         # Core business logic
│   │   ├── enrichment/  # Enrichment services
│   │   └── integrations/ # External API integrations
│   └── services/     # Service layer
│
├── workflows/        # Execution scripts
│   └── run.sh        # Main application runner
│
├── scripts/          # Utility scripts
│   ├── detect_resources.sh  # Resource detection
│   └── validate_taxonomy.py  # Structure validation
│
├── tests/            # Test files
│   ├── unit/         # Unit tests
│   ├── integration/  # Integration tests
│   └── e2e/          # End-to-end tests
│
├── docs/             # Documentation
│   ├── guides/       # How-to guides
│   ├── plans/        # Project plans
│   └── troubleshooting/ # Troubleshooting guides
│
└── Makefile          # Common commands
```

For detailed structure explanation, see [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md).

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (optional):

```bash
# Server Configuration
PORT=8247
HOST=0.0.0.0
DEBUG=false

# Database
DATABASE_URL=sqlite:///./app.db

# API Keys (optional - for real data enrichment)
HUNTER_API_KEY=your_key_here
ZEROBOUNCE_API_KEY=your_key_here
PDL_API_KEY=your_key_here
# ... more API keys
```

### Backend Configuration

Main configuration is in `config.py` using Pydantic Settings:
- Reads from environment variables
- Falls back to defaults
- Supports `.env` file

### Frontend Configuration

Frontend configuration is in `frontend/vite.config.ts`:
- Development server on port 5173
- Proxy to backend API (if needed)

---

## 🧪 Running Tests

### Backend Tests

```bash
# Run all backend tests
make test

# Run with coverage
source venv/bin/activate
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

### Frontend Tests

```bash
# Run linting
cd frontend && npm run lint

# Run Playwright tests (if configured)
cd frontend && npm test
```

---

## 🐛 Troubleshooting

### Backend Won't Start

1. **Check Python version**: `python3 --version` (need 3.11+)
2. **Check virtual environment**: `source venv/bin/activate`
3. **Reinstall dependencies**: `pip install -r requirements-minimal.txt`
4. **Check port availability**: Port 8247 might be in use

### Frontend Won't Start

1. **Check Node version**: `node --version` (need 20+)
2. **Reinstall dependencies**: `cd frontend && npm install`
3. **Check port availability**: Port 5173 might be in use
4. **Clear cache**: `rm -rf frontend/node_modules frontend/package-lock.json && npm install`

### Port Conflicts

If ports are already in use:

```bash
# Find process using port
lsof -i :8247  # Backend
lsof -i :5173  # Frontend

# Kill process (replace PID)
kill -9 <PID>

# Or use different ports via environment variables
PORT=8248 make backend
```

### Database Issues

```bash
# Reset database (development only!)
rm app.db
source venv/bin/activate
python -c "from database.connection import Base, engine; Base.metadata.create_all(engine)"
```

---

## 📖 Next Steps

1. **Explore the API**: Visit http://localhost:8247/docs
2. **Read Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)
3. **Check Project Structure**: See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)
4. **Review Completed Tasks**: See [TASKS_EXECUTED.md](./TASKS_EXECUTED.md)
5. **Contribute**: See [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 🆘 Getting Help

- **Documentation**: Check `docs/` directory
- **Troubleshooting**: See `docs/troubleshooting/`
- **Guides**: See `docs/guides/`
- **Issues**: Check GitHub issues

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] `make install` completes without errors
- [ ] `pre-commit install` succeeds
- [ ] `make run` starts both services
- [ ] Frontend accessible at http://localhost:5173
- [ ] Backend accessible at http://localhost:8247
- [ ] API docs accessible at http://localhost:8247/docs
- [ ] Health check works: http://localhost:8247/health
- [ ] `make test` passes

---

**Welcome aboard! 🎉**
