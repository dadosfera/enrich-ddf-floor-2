# Architecture Documentation

This document describes the architecture and design decisions of Enrich DDF Floor 2.

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  React + TypeScript + Vite (Port 5173)                     │
│  - Material-UI Components                                   │
│  - React Router for Navigation                              │
│  - React Query for Data Fetching                            │
│  - React Hook Form for Forms                                │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────────┐
│                      Backend Layer                          │
│  FastAPI (Python) (Port 8247)                                │
│  - RESTful API Endpoints                                    │
│  - Request Validation                                        │
│  - Error Handling                                           │
│  - CORS Middleware                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌─────────▼──────────┐
│  Database      │      │  External APIs     │
│  SQLAlchemy    │      │  - Hunter.io        │
│  SQLite (dev)  │      │  - ZeroBounce      │
│  PostgreSQL    │      │  - People Data Labs │
│  (prod)        │      │  - Wiza            │
│                │      │  - Surfe           │
│                │      │  - BigData Corp    │
└────────────────┘      └────────────────────┘
```

---

## 🔧 Technology Stack

### Frontend

- **React 19**: Modern React with latest features
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **Material-UI (MUI)**: Component library
- **React Router**: Client-side routing
- **React Query**: Data fetching and caching
- **React Hook Form**: Form management
- **Zustand**: State management (if needed)

### Backend

- **FastAPI**: Modern Python web framework
- **Python 3.11+**: Programming language
- **SQLAlchemy**: ORM for database access
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Database

- **SQLite**: Development database
- **PostgreSQL**: Production database (ready)

### DevOps & Tools

- **Docker & Docker Compose**: Containerization
- **Pre-commit**: Git hooks for code quality
- **Ruff**: Python linting and formatting
- **ESLint**: JavaScript linting
- **Playwright**: End-to-end testing
- **Pytest**: Python testing

---

## 📦 Component Architecture

### Backend Components

#### 1. Application Entry Point (`main.py`)

- FastAPI application initialization
- Middleware configuration (CORS, logging)
- Route registration
- Lifespan management (startup/shutdown)

#### 2. Configuration (`config.py`)

- Environment-based configuration
- Pydantic Settings for validation
- API key management
- Feature flags

#### 3. Database Layer (`database/`)

```
database/
├── connection.py      # Database connection and session management
├── models.py          # SQLAlchemy models
└── utils/             # Database utilities
```

**Models**:
- `Company`: Company information
- `Contact`: Contact/people information
- `Product`: Product information

#### 4. Core Business Logic (`core/`)

```
core/
├── enrichment/        # Enrichment services
│   ├── company/       # Company enrichment logic
│   ├── contact/       # Contact enrichment logic
│   └── product/       # Product enrichment logic
└── integrations/      # External API integrations
```

#### 5. Services (`services/`)

```
services/
├── third_party/       # Third-party API clients
└── government_apis/   # Government API integrations
```

### Frontend Components

#### 1. Application Structure (`frontend/src/`)

```
src/
├── App.tsx            # Main application component
├── main.tsx           # Application entry point
├── pages/             # Page components
│   ├── Dashboard.tsx
│   ├── Companies.tsx
│   ├── Contacts.tsx
│   ├── Products.tsx
│   └── Integrations.tsx
├── components/        # Reusable components
│   └── common/        # Common UI components
├── services/          # API service clients
└── types/             # TypeScript type definitions
```

#### 2. API Integration (`frontend/src/services/`)

- Service wrappers for backend API
- Type-safe API clients
- Error handling
- Request/response types

---

## 🔄 Data Flow

### Request Flow

1. **User Action** → Frontend component
2. **API Call** → Service layer (React Query)
3. **HTTP Request** → Backend API endpoint
4. **Validation** → Pydantic models
5. **Business Logic** → Core services
6. **Database** → SQLAlchemy ORM
7. **Response** → JSON serialization
8. **Frontend** → React Query cache update
9. **UI Update** → Component re-render

### Enrichment Flow

1. **User Input** → Company/Contact/Product data
2. **Validation** → Input validation
3. **Enrichment Request** → Core enrichment service
4. **External API Calls** → Multiple enrichment providers
5. **Data Aggregation** → Merge results
6. **Database Storage** → Save enriched data
7. **Response** → Return enriched data
8. **UI Display** → Show enriched information

---

## 🗄️ Database Schema

### Company Model

```python
- id: Integer (Primary Key)
- name: String
- domain: String (Unique)
- industry: String
- size: String
- location: String
- description: Text
- website: String
- phone: String
- email: String
- enrichment_data: JSON
- is_verified: Boolean
- is_active: Boolean
- created_at: DateTime
- updated_at: DateTime
```

### Contact Model

```python
- id: Integer (Primary Key)
- first_name: String
- last_name: String
- email: String (Unique)
- phone: String
- job_title: String
- department: String
- company_id: Integer (Foreign Key → Company)
- linkedin_url: String
- twitter_url: String
- enrichment_data: JSON
- is_verified: Boolean
- is_active: Boolean
- created_at: DateTime
- updated_at: DateTime
```

### Product Model

```python
- id: Integer (Primary Key)
- name: String
- sku: String (Unique)
- category: String
- subcategory: String
- brand: String
- description: Text
- price: Decimal
- currency: String
- weight: Decimal
- dimensions: String
- stock_quantity: Integer
- product_url: String
- image_url: String
- classification_data: JSON
- enrichment_data: JSON
- is_active: Boolean
- is_featured: Boolean
- created_at: DateTime
- updated_at: DateTime
```

---

## 🔌 API Design

### RESTful Endpoints

#### Companies

- `GET /api/v1/companies` - List companies
- `POST /api/v1/companies` - Create company
- `GET /api/v1/companies/{id}` - Get company (planned)
- `PUT /api/v1/companies/{id}` - Update company (planned)
- `DELETE /api/v1/companies/{id}` - Delete company (planned)

#### Contacts

- `GET /api/v1/contacts` - List contacts
- `POST /api/v1/contacts` - Create contact
- `GET /api/v1/contacts/{id}` - Get contact (planned)
- `PUT /api/v1/contacts/{id}` - Update contact (planned)
- `DELETE /api/v1/contacts/{id}` - Delete contact (planned)

#### Products

- `GET /api/v1/products` - List products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products/{id}` - Get product (planned)
- `PUT /api/v1/products/{id}` - Update product (planned)
- `DELETE /api/v1/products/{id}` - Delete product (planned)

#### System

- `GET /` - Root endpoint (API info)
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)

---

## 🔐 Security Considerations

### Authentication & Authorization

- **Current**: Not implemented (planned)
- **Planned**: JWT-based authentication
- **Planned**: Role-based access control (RBAC)

### API Security

- **CORS**: Configured for development (needs production config)
- **Input Validation**: Pydantic models validate all inputs
- **SQL Injection**: Protected by SQLAlchemy ORM
- **Rate Limiting**: Planned (configured in settings)

### Data Protection

- **API Keys**: Stored in environment variables
- **Secrets**: Never committed to repository
- **Database**: Connection strings in environment variables

---

## 🚀 Deployment Architecture

### Development

```
Local Machine
├── Frontend: Vite dev server (Port 5173)
├── Backend: Uvicorn (Port 8247)
└── Database: SQLite file
```

### Production (Planned)

```
Docker Compose / Kubernetes
├── Frontend Container: Nginx + Built React app
├── Backend Container: Uvicorn + FastAPI
├── Database Container: PostgreSQL
└── Redis Container: Caching (planned)
```

---

## 📈 Scalability Considerations

### Current Limitations

- **Single Process**: Backend runs in single process
- **SQLite**: Not suitable for high concurrency
- **No Caching**: All requests hit database

### Planned Improvements

- **Horizontal Scaling**: Multiple backend instances
- **PostgreSQL**: Production database
- **Redis Caching**: Reduce database load
- **Celery**: Background task processing
- **Load Balancing**: Nginx or cloud load balancer

---

## 🔍 Monitoring & Observability

### Current

- **Logging**: Python logging module
- **Health Checks**: `/health` endpoint

### Planned

- **Structured Logging**: JSON logs
- **Metrics**: Prometheus metrics
- **Tracing**: OpenTelemetry
- **Error Tracking**: Sentry integration
- **APM**: Application Performance Monitoring

---

## 📚 Design Decisions

### Why FastAPI?

- **Performance**: Fast, comparable to Node.js
- **Type Safety**: Python type hints + Pydantic
- **Auto Documentation**: OpenAPI/Swagger generation
- **Modern**: Async/await support
- **Developer Experience**: Great tooling

### Why React + TypeScript?

- **Type Safety**: Catch errors at compile time
- **Component Reusability**: Modular UI components
- **Ecosystem**: Rich library ecosystem
- **Performance**: Virtual DOM optimization
- **Developer Experience**: Great tooling and debugging

### Why SQLAlchemy?

- **ORM Benefits**: Type-safe database access
- **Migrations**: Alembic integration
- **Database Agnostic**: Easy to switch databases
- **Mature**: Battle-tested in production

---

## 🔄 Future Architecture Considerations

### Microservices (Long-term)

- Split into domain-specific services
- API Gateway for routing
- Service mesh for communication
- Event-driven architecture

### Real-time Features

- WebSocket support for real-time updates
- Server-Sent Events (SSE) for streaming
- WebRTC for peer-to-peer (if needed)

### Data Pipeline

- ETL pipeline for bulk enrichment
- Queue system for async processing
- Data warehouse integration
- Analytics and reporting

---

## 📖 Related Documentation

- [Getting Started Guide](./GETTING_STARTED.md)
- [Project Structure](./PROJECT_STRUCTURE.md)
- [Tasks Executed](./TASKS_EXECUTED.md)
- [Contributing Guide](./CONTRIBUTING.md)

---

**Last Updated**: 2025-11-13
