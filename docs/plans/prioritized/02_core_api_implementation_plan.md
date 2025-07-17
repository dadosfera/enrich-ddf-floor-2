# Phase 2: Core API Implementation Plan
**Enrich DDF Floor 2 - Unified Data Enrichment Platform**

**Plan Status**: Ready for Implementation  
**Priority**: P1 (Critical - Next Phase)  
**Estimated Duration**: 3-4 weeks  
**Dependencies**: Phase 1 (Foundation) Complete ✅

## 📋 Overview

This plan outlines the implementation of core API functionality for the Enrich DDF Floor 2 platform, building upon the solid foundation established in Phase 1. The implementation will focus on creating production-ready authentication, data enrichment APIs, and external service integrations.

## 🎯 Phase 2 Objectives

### Primary Goals
1. **Authentication System**: Secure JWT-based authentication with role management
2. **Core API Endpoints**: Person and company enrichment functionality  
3. **External Integrations**: Apollo, PeopleDataLabs, ZeroBounce APIs
4. **Data Models**: Comprehensive database schema for enrichment data
5. **Background Jobs**: Asynchronous processing with Celery
6. **Multi-Country Support**: Foundation for Latin American markets

### Success Metrics
- **API Response Time**: < 500ms for standard enrichment requests
- **Authentication**: JWT tokens with 30-minute expiry and refresh capability
- **Data Coverage**: Support for 5+ data sources per enrichment type
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Test Coverage**: 85%+ code coverage for all new endpoints

## 🗓️ Implementation Timeline

### Week 1: Authentication & User Management
**Priority**: P1 (Critical Foundation)

#### Days 1-2: Authentication System
- [ ] **JWT Token Management**
  - JWT token generation and validation
  - Refresh token mechanism
  - Token blacklisting for logout
  - Secure secret key management

- [ ] **User Models & Database Schema**
  - User registration and profile models
  - Role-based access control (RBAC)
  - Password hashing with bcrypt
  - Database migrations with Alembic

#### Days 3-4: Authentication Endpoints
- [ ] **Authentication API Implementation**
  - `POST /api/v1/auth/register` - User registration
  - `POST /api/v1/auth/login` - User authentication
  - `POST /api/v1/auth/refresh` - Token refresh
  - `POST /api/v1/auth/logout` - Secure logout
  - `GET /api/v1/auth/me` - User profile

#### Days 5-7: Security & Middleware
- [ ] **Security Implementation**
  - Authentication middleware
  - Rate limiting with Redis
  - CORS configuration for production
  - Security headers (OWASP recommendations)
  - Input validation and sanitization

### Week 2: Core Data Models & Database
**Priority**: P1 (Data Foundation)

#### Days 1-3: Database Schema Design
- [ ] **Core Entity Models**
  ```python
  # Person enrichment models
  class Person(Base):
      id: UUID
      email: str
      first_name: str
      last_name: str
      phone: str
      company_id: UUID
      # Professional information
      job_title: str
      linkedin_url: str
      # Enrichment metadata
      data_sources: List[str]
      confidence_score: float
      last_enriched: datetime
  
  # Company enrichment models  
  class Company(Base):
      id: UUID
      name: str
      domain: str
      country: str
      # Business information
      industry: str
      employee_count: int
      annual_revenue: str
      # Location data
      address: str
      city: str
      state: str
      postal_code: str
      # Enrichment metadata
      data_sources: List[str]
      confidence_score: float
      last_enriched: datetime
  
  # Enrichment job tracking
  class EnrichmentJob(Base):
      id: UUID
      user_id: UUID
      job_type: str  # 'person', 'company', 'bulk'
      status: str    # 'pending', 'processing', 'completed', 'failed'
      input_data: dict
      results: dict
      error_message: str
      created_at: datetime
      completed_at: datetime
  ```

#### Days 4-5: Data Source Integration Models
- [ ] **External API Integration Models**
  ```python
  class DataSource(Base):
      id: UUID
      name: str  # 'apollo', 'peopledatalabs', 'zerobounce'
      api_key_encrypted: str
      rate_limit: int
      monthly_quota: int
      usage_count: int
      is_active: bool
  
  class EnrichmentResult(Base):
      id: UUID
      job_id: UUID
      data_source: str
      raw_response: dict
      processed_data: dict
      confidence_score: float
      created_at: datetime
  ```

#### Days 6-7: Database Migrations & Seeding
- [ ] **Database Setup**
  - Alembic migration scripts
  - Database constraints and indexes
  - Sample data seeding for development
  - Database backup and restore procedures

### Week 3: API Endpoints Implementation
**Priority**: P1 (Core Functionality)

#### Days 1-3: Person Enrichment API
- [ ] **Person Enrichment Endpoints**
  ```python
  # Single person enrichment
  POST /api/v1/people/enrich
  {
    "email": "john.doe@company.com",
    "sources": ["apollo", "peopledatalabs"],
    "include_company": true
  }
  
  # Bulk person enrichment
  POST /api/v1/people/enrich/bulk
  {
    "people": [
      {"email": "person1@company.com"},
      {"email": "person2@company.com"}
    ],
    "sources": ["apollo"],
    "callback_url": "https://your-app.com/webhook"
  }
  
  # Get enrichment results
  GET /api/v1/people/{person_id}
  GET /api/v1/people/?company_id={company_id}
  ```

#### Days 4-6: Company Enrichment API
- [ ] **Company Enrichment Endpoints**
  ```python
  # Single company enrichment
  POST /api/v1/companies/enrich
  {
    "domain": "company.com",
    "sources": ["apollo", "serpro"],
    "country": "BR"
  }
  
  # Company search by criteria
  POST /api/v1/companies/search
  {
    "name": "Tech Company",
    "city": "São Paulo",
    "industry": "Technology",
    "limit": 50
  }
  
  # Get company details
  GET /api/v1/companies/{company_id}
  GET /api/v1/companies/?domain={domain}
  ```

#### Day 7: Background Jobs API
- [ ] **Job Management Endpoints**
  ```python
  # Get job status
  GET /api/v1/jobs/{job_id}
  
  # List user jobs
  GET /api/v1/jobs/?status=completed&limit=50
  
  # Cancel job
  DELETE /api/v1/jobs/{job_id}
  ```

### Week 4: External Integrations & Advanced Features
**Priority**: P2 (Enhanced Functionality)

#### Days 1-2: Apollo API Integration
- [ ] **Apollo Integration Service**
  ```python
  class ApolloService:
      async def search_people(self, email: str) -> dict
      async def search_companies(self, domain: str) -> dict
      async def enrich_person(self, person_data: dict) -> dict
      async def bulk_enrich(self, contacts: List[dict]) -> dict
  ```

#### Days 3-4: PeopleDataLabs Integration
- [ ] **PeopleDataLabs Integration Service**
  ```python
  class PeopleDataLabsService:
      async def person_enrichment(self, email: str) -> dict
      async def company_enrichment(self, domain: str) -> dict
      async def search_people(self, criteria: dict) -> dict
      async def bulk_enrichment(self, requests: List[dict]) -> dict
  ```

#### Days 5-6: Latin American Data Sources
- [ ] **Regional API Integrations**
  ```python
  # Brazil - Serpro API
  class SerproService:
      async def cnpj_lookup(self, cnpj: str) -> dict
      async def cpf_validation(self, cpf: str) -> dict
  
  # Argentina - AFIP API  
  class AFIPService:
      async def cuit_lookup(self, cuit: str) -> dict
  
  # Mexico - SAT API
  class SATService:
      async def rfc_lookup(self, rfc: str) -> dict
  ```

#### Day 7: Background Processing
- [ ] **Celery Task Implementation**
  ```python
  @celery_app.task(bind=True)
  def enrich_person_task(self, job_id: str, person_data: dict):
      # Asynchronous person enrichment
      pass
  
  @celery_app.task(bind=True)  
  def bulk_enrichment_task(self, job_id: str, people_list: List[dict]):
      # Bulk processing with progress updates
      pass
  ```

## 🏗️ Technical Architecture

### API Structure
```
/api/v1/
├── auth/           # Authentication endpoints
├── people/         # Person enrichment
├── companies/      # Company enrichment  
├── jobs/           # Background job management
├── sources/        # Data source configuration
└── webhooks/       # Webhook endpoints
```

### Service Layer Architecture
```python
# Service layer for business logic
app/
├── services/
│   ├── auth_service.py
│   ├── enrichment_service.py
│   ├── apollo_service.py
│   ├── peopledatalabs_service.py
│   ├── zerobounce_service.py
│   └── regional_services/
│       ├── serpro_service.py
│       ├── afip_service.py
│       └── sat_service.py
├── models/
│   ├── user.py
│   ├── person.py
│   ├── company.py
│   └── enrichment_job.py
└── api/v1/endpoints/
    ├── auth.py
    ├── people.py
    ├── companies.py
    └── jobs.py
```

### Database Schema
```sql
-- Core tables
users (id, email, password_hash, role, created_at)
people (id, email, name, company_id, enrichment_data, last_enriched)
companies (id, name, domain, country, enrichment_data, last_enriched)
enrichment_jobs (id, user_id, type, status, input_data, results, created_at)

-- Integration tables
data_sources (id, name, api_key_encrypted, rate_limit, quota, usage)
enrichment_results (id, job_id, source, raw_response, processed_data)
```

## 🔐 Security Implementation

### Authentication & Authorization
- **JWT Tokens**: 30-minute access tokens with refresh capability
- **Role-Based Access**: Admin, User, API-only roles
- **Rate Limiting**: Per-user and per-endpoint limits
- **API Key Management**: Encrypted storage of external API keys

### Data Protection
- **Input Validation**: Pydantic models for all requests
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **XSS Prevention**: Automatic input sanitization
- **HTTPS Only**: TLS 1.3 for all communications

## 📊 Monitoring & Observability

### API Metrics
- **Response Times**: P95 latency tracking
- **Error Rates**: 4xx/5xx error monitoring
- **Rate Limit Usage**: Per-user consumption tracking
- **External API Status**: Integration health monitoring

### Business Metrics
- **Enrichment Success Rates**: By data source and type
- **API Usage**: Endpoint popularity and user behavior
- **Data Quality**: Confidence scores and accuracy metrics
- **Cost Tracking**: External API usage and costs

## 🧪 Testing Strategy

### Test Coverage Requirements
- **Unit Tests**: 90%+ coverage for services and models
- **Integration Tests**: API endpoint testing with test database
- **External API Tests**: Mocked responses for reliable testing
- **Security Tests**: Authentication and authorization testing

### Test Implementation
```python
# Unit tests
tests/unit/
├── test_auth_service.py
├── test_enrichment_service.py
├── test_apollo_service.py
└── test_models.py

# Integration tests
tests/integration/
├── test_auth_endpoints.py
├── test_people_endpoints.py
├── test_companies_endpoints.py
└── test_background_jobs.py

# API tests
tests/api/
├── test_authentication_flow.py
├── test_enrichment_workflows.py
└── test_error_handling.py
```

## 🚀 Deployment Strategy

### Environment Configuration
```python
# Production settings
class ProductionSettings(Settings):
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    
    # External API keys (encrypted in environment)
    APOLLO_API_KEY: str = Field(..., env="APOLLO_API_KEY")
    PDL_API_KEY: str = Field(..., env="PDL_API_KEY")
    ZEROBOUNCE_API_KEY: str = Field(..., env="ZEROBOUNCE_API_KEY")
```

### Infrastructure Requirements
- **Application Server**: FastAPI with Uvicorn (4 workers minimum)
- **Database**: PostgreSQL 15+ with connection pooling
- **Cache**: Redis 7+ for sessions and rate limiting
- **Background Jobs**: Celery with Redis broker
- **Monitoring**: Prometheus + Grafana dashboards

## 📋 Definition of Done

### API Endpoints
- [ ] All endpoints implemented with proper HTTP methods and status codes
- [ ] Request/response models validated with Pydantic
- [ ] OpenAPI/Swagger documentation auto-generated
- [ ] Error handling with detailed error messages
- [ ] Rate limiting implemented and tested

### Authentication
- [ ] JWT authentication working end-to-end
- [ ] User registration and login flows complete
- [ ] Role-based access control implemented
- [ ] Token refresh mechanism working
- [ ] Secure logout functionality

### Data Integration
- [ ] Person enrichment working with 2+ external APIs
- [ ] Company enrichment working with 2+ external APIs
- [ ] Database models storing enrichment results
- [ ] Background job processing implemented
- [ ] Error handling for external API failures

### Quality Assurance
- [ ] 85%+ test coverage achieved
- [ ] All linting and security checks passing
- [ ] Performance benchmarks met (< 500ms response time)
- [ ] Documentation complete and up-to-date
- [ ] Production deployment successful

## 📈 Success Metrics

### Technical Metrics
- **API Response Time**: P95 < 500ms, P99 < 1s
- **Error Rate**: < 1% for all endpoints
- **Test Coverage**: > 85% code coverage
- **Uptime**: 99.9% availability

### Business Metrics
- **Enrichment Accuracy**: > 90% data quality score
- **API Adoption**: 100+ enrichment requests per day
- **User Satisfaction**: Positive feedback on API usability
- **Cost Efficiency**: Optimized external API usage

## 🔄 Risk Mitigation

### Technical Risks
- **External API Rate Limits**: Implement queue management and fallback strategies
- **Database Performance**: Use connection pooling and query optimization
- **Security Vulnerabilities**: Regular security audits and dependency updates
- **Scalability**: Design for horizontal scaling from day one

### Business Risks
- **Data Source Availability**: Multiple fallback sources for each enrichment type
- **API Key Management**: Secure rotation and monitoring procedures
- **Compliance**: Ensure GDPR and local privacy law compliance
- **Cost Overruns**: Implement usage monitoring and alerts

## 📚 Documentation Deliverables

### API Documentation
- [ ] OpenAPI/Swagger specification
- [ ] Postman collection with examples
- [ ] Authentication flow diagrams
- [ ] Error code reference guide

### Developer Documentation
- [ ] Service architecture overview
- [ ] Database schema documentation
- [ ] External API integration guides
- [ ] Local development setup guide

### Operational Documentation
- [ ] Deployment procedures
- [ ] Monitoring and alerting setup
- [ ] Backup and recovery procedures
- [ ] Troubleshooting guide

---

**Next Steps**: Upon completion of Phase 1 foundation, this plan will be activated for immediate implementation. All prerequisites are met, and the development team is ready to begin Phase 2 core API development.

**Estimated Completion**: 4 weeks from start date  
**Resource Requirements**: 1-2 senior developers, 1 DevOps engineer  
**Budget Considerations**: External API costs and infrastructure scaling 