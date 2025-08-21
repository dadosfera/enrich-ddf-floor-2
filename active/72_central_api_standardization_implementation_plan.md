# 🚀 Central API Standardization - Implementation Plan

**Status:** Active Implementation Plan
**Priority:** P1 (Critical)
**Timeline:** 2-3 weeks
**Dependencies:** 4/8 APIs validated and working

## 🎯 **Objective**

Implement a unified API layer that standardizes enrichment requests across multiple data sources, providing consistent request/response formats and intelligent routing to the most appropriate data provider.

## 📊 **Current State Analysis**

### ✅ **Working APIs (Ready for Integration)**
```bash
✅ GitHub API          - Developer profiles & activity data
✅ Hunter.io API       - Email discovery & verification (60 calls remaining)
✅ ZeroBounce API      - Email validation (215,097 credits available)
✅ Apollo.io API       - B2B contact & company enrichment
```

### 🔧 **Pending APIs (Phase 2)**
```bash
⚙️ BigData Corp API    - Brazilian CPF/CNPJ data (needs configuration)
❌ Wiza API           - LinkedIn profile extraction (DNS issues)
❌ Surfe API          - B2B people search (endpoint verification needed)
❌ Coresignal API     - Business profiles (API structure research needed)
```

---

## 🏗️ **Phase 1: Core Unified API Layer (Week 1-2)**

### **1.1 Central API Router Implementation**

**Location:** `core/integrations/central_api/`

```bash
core/integrations/central_api/
├── __init__.py
├── router.py              # Main API routing logic
├── standardizer.py        # Request/response standardization
├── rate_limiter.py        # Cross-API rate limiting
├── fallback_handler.py    # Provider fallback logic
├── cache_manager.py       # Response caching layer
└── providers/
    ├── github_provider.py
    ├── hunter_provider.py
    ├── zerobounce_provider.py
    └── apollo_provider.py
```

### **1.2 Standardized API Endpoints**

**Base URL:** `/api/v1/enrich/`

#### **Company Enrichment**
```http
POST /api/v1/enrich/company
Content-Type: application/json

{
  "identifier": {
    "domain": "example.com",          # Primary identifier
    "company_name": "Example Corp",   # Alternative identifier
    "linkedin_url": "linkedin.com/company/example"  # Social identifier
  },
  "data_sources": ["apollo", "github", "hunter"],  # Optional: specify sources
  "include_fields": [
    "basic_info",
    "contact_info",
    "social_profiles",
    "employee_data",
    "technology_stack"
  ]
}
```

#### **Contact Enrichment**
```http
POST /api/v1/enrich/contact
Content-Type: application/json

{
  "identifier": {
    "email": "john@example.com",      # Primary identifier
    "full_name": "John Doe",          # Alternative identifier
    "linkedin_url": "linkedin.com/in/john-doe",  # Social identifier
    "github_username": "johndoe"      # Developer identifier
  },
  "data_sources": ["github", "apollo", "hunter"],
  "include_fields": [
    "basic_info",
    "professional_info",
    "contact_details",
    "social_profiles",
    "technical_skills"
  ]
}
```

#### **Email Operations**
```http
POST /api/v1/enrich/email/find
{
  "domain": "example.com",
  "first_name": "John",
  "last_name": "Doe",
  "sources": ["hunter", "apollo"]
}

POST /api/v1/enrich/email/validate
{
  "emails": ["john@example.com", "jane@example.com"],
  "sources": ["zerobounce"]
}
```

### **1.3 Standardized Response Format**

```json
{
  "success": true,
  "request_id": "uuid-here",
  "timestamp": "2024-08-21T00:00:00Z",
  "data": {
    "identifier": {...},
    "enriched_data": {
      "basic_info": {...},
      "contact_info": {...},
      "social_profiles": {...}
    },
    "confidence_score": 0.95,
    "data_sources_used": ["github", "apollo"],
    "credits_consumed": {
      "github": 1,
      "apollo": 2,
      "total_cost": 0.03
    }
  },
  "metadata": {
    "processing_time_ms": 1250,
    "cache_hit": false,
    "fallback_used": false
  }
}
```

---

## 🔧 **Technical Implementation Details**

### **2.1 Provider Interface Standard**

**File:** `core/integrations/central_api/base_provider.py`

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class EnrichmentRequest:
    identifier: Dict[str, Any]
    data_sources: List[str]
    include_fields: List[str]
    options: Dict[str, Any] = None

@dataclass
class EnrichmentResponse:
    success: bool
    data: Dict[str, Any]
    confidence_score: float
    credits_used: int
    processing_time_ms: int
    errors: List[str] = None

class BaseProvider(ABC):
    """Base class for all data enrichment providers"""

    @abstractmethod
    def enrich_company(self, request: EnrichmentRequest) -> EnrichmentResponse:
        pass

    @abstractmethod
    def enrich_contact(self, request: EnrichmentRequest) -> EnrichmentResponse:
        pass

    @abstractmethod
    def validate_email(self, emails: List[str]) -> EnrichmentResponse:
        pass

    @abstractmethod
    def find_email(self, domain: str, first_name: str, last_name: str) -> EnrichmentResponse:
        pass
```

### **2.2 Intelligent Provider Selection**

**File:** `core/integrations/central_api/provider_selector.py`

```python
class ProviderSelector:
    """Smart provider selection based on data type, availability, and cost"""

    PROVIDER_CAPABILITIES = {
        'github': {
            'contact': ['technical_skills', 'open_source_activity', 'developer_profile'],
            'company': ['technology_stack', 'developer_count', 'repository_data'],
            'cost_per_request': 0.001,
            'rate_limit': 5000  # per hour
        },
        'hunter': {
            'contact': ['email_finding', 'email_verification'],
            'company': ['email_patterns', 'contact_discovery'],
            'cost_per_request': 0.01,
            'rate_limit': 75  # per month (current account)
        },
        'zerobounce': {
            'contact': ['email_validation', 'deliverability_score'],
            'company': [],
            'cost_per_request': 0.0001,
            'rate_limit': 215097  # credits available
        },
        'apollo': {
            'contact': ['professional_info', 'contact_details', 'job_history'],
            'company': ['company_info', 'employee_data', 'revenue_data'],
            'cost_per_request': 0.02,
            'rate_limit': 1000  # estimated per hour
        }
    }

    def select_providers(self, request: EnrichmentRequest) -> List[str]:
        """Select optimal providers based on request requirements"""
        # Implementation logic for smart provider selection
        pass
```

### **2.3 Rate Limiting & Quotas**

**File:** `core/integrations/central_api/rate_limiter.py`

```python
from redis import Redis
from datetime import datetime, timedelta
import json

class RateLimiter:
    """Cross-provider rate limiting and quota management"""

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def check_rate_limit(self, provider: str, user_id: str) -> bool:
        """Check if request is within rate limits"""
        pass

    def consume_credits(self, provider: str, credits: int) -> bool:
        """Consume credits from provider quota"""
        pass

    def get_quota_status(self) -> Dict[str, Any]:
        """Get current quota status for all providers"""
        return {
            'github': {'remaining': 4850, 'reset_time': '2024-08-21T01:00:00Z'},
            'hunter': {'remaining': 60, 'reset_time': '2024-09-01T00:00:00Z'},
            'zerobounce': {'remaining': 215097, 'reset_time': 'N/A'},
            'apollo': {'remaining': 950, 'reset_time': '2024-08-21T01:00:00Z'}
        }
```

---

## 📋 **Implementation Tasks - Week by Week**

### **Week 1: Foundation & Core APIs**

#### **Day 1-2: Project Setup**
- [ ] Create `core/integrations/central_api/` directory structure
- [ ] Implement `BaseProvider` abstract class
- [ ] Set up provider configuration management
- [ ] Create standardized request/response models

#### **Day 3-4: Provider Implementations**
- [ ] Implement `GitHubProvider` class
  - [ ] Developer profile enrichment
  - [ ] Repository analysis
  - [ ] Contribution history
- [ ] Implement `HunterProvider` class
  - [ ] Email finding functionality
  - [ ] Domain search capabilities
  - [ ] Email verification

#### **Day 5-7: Core Router**
- [ ] Implement `CentralAPIRouter`
- [ ] Add request validation & sanitization
- [ ] Implement `ProviderSelector` logic
- [ ] Create fallback handling system

### **Week 2: Advanced Features & Integration**

#### **Day 8-10: Additional Providers**
- [ ] Implement `ZeroBounceProvider`
  - [ ] Bulk email validation
  - [ ] Deliverability scoring
  - [ ] Bounce detection
- [ ] Implement `ApolloProvider`
  - [ ] Contact enrichment
  - [ ] Company data extraction
  - [ ] Professional history

#### **Day 11-12: Advanced Features**
- [ ] Implement caching layer (Redis)
- [ ] Add rate limiting across all providers
- [ ] Create response merging logic
- [ ] Add confidence scoring algorithm

#### **Day 13-14: API Endpoints**
- [ ] Implement FastAPI endpoints
  - [ ] `/api/v1/enrich/company`
  - [ ] `/api/v1/enrich/contact`
  - [ ] `/api/v1/enrich/email/find`
  - [ ] `/api/v1/enrich/email/validate`
- [ ] Add OpenAPI documentation
- [ ] Implement authentication & authorization

### **Week 3: Testing & Deployment**

#### **Day 15-17: Testing**
- [ ] Unit tests for all providers
- [ ] Integration tests for API endpoints
- [ ] Load testing with rate limits
- [ ] Error handling validation

#### **Day 18-19: Documentation & Monitoring**
- [ ] Complete API documentation
- [ ] Add usage analytics
- [ ] Implement health checks
- [ ] Create monitoring dashboards

#### **Day 20-21: Deployment**
- [ ] Deploy to staging environment
- [ ] Performance optimization
- [ ] Production deployment
- [ ] User acceptance testing

---

## 🧪 **Testing Strategy**

### **3.1 Unit Tests**

**Location:** `tests/integration/central_api/`

```python
# Example test structure
def test_github_provider_contact_enrichment():
    """Test GitHub provider for developer profile enrichment"""
    provider = GitHubProvider()
    request = EnrichmentRequest(
        identifier={"github_username": "ddf-otsm"},
        data_sources=["github"],
        include_fields=["technical_skills", "repository_data"]
    )
    response = provider.enrich_contact(request)
    assert response.success is True
    assert response.confidence_score > 0.8
```

### **3.2 Integration Tests**

```python
def test_unified_company_enrichment():
    """Test complete company enrichment workflow"""
    client = TestClient(app)
    response = client.post("/api/v1/enrich/company", json={
        "identifier": {"domain": "github.com"},
        "data_sources": ["github", "apollo", "hunter"],
        "include_fields": ["basic_info", "employee_data", "contact_info"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["data_sources_used"]) >= 2
```

### **3.3 Load Tests**

```python
# Simulate high load across multiple providers
async def load_test_rate_limits():
    """Test rate limiting under load"""
    # Test concurrent requests
    # Validate rate limit enforcement
    # Check fallback provider activation
    pass
```

---

## 📊 **Monitoring & Analytics**

### **4.1 Key Metrics**
- **Request Volume:** Requests per provider per hour
- **Success Rate:** % successful enrichments by provider
- **Response Time:** Average processing time per endpoint
- **Credit Usage:** API costs per provider
- **Cache Hit Rate:** % requests served from cache

### **4.2 Dashboards**
- **Real-time:** Current API health & rate limits
- **Daily:** Usage patterns & cost analysis
- **Weekly:** Provider performance comparison

### **4.3 Alerting**
- Rate limit approaching (80% threshold)
- Provider API failures (3+ consecutive failures)
- High response times (>5 seconds)
- Credit exhaustion warnings

---

## 🔐 **Security & Compliance**

### **5.1 API Security**
- [ ] JWT authentication for all endpoints
- [ ] Rate limiting per user/organization
- [ ] Request sanitization & validation
- [ ] HTTPS enforcement

### **5.2 Data Privacy**
- [ ] GDPR compliance for EU data
- [ ] Data retention policies
- [ ] PII encryption in cache
- [ ] Audit logging

### **5.3 API Key Management**
- [ ] Secure key rotation (90-day cycle)
- [ ] Key usage monitoring
- [ ] Automatic key validation
- [ ] Backup key configuration

---

## 🚀 **Deployment & Scaling**

### **6.1 Infrastructure**
```yaml
# docker-compose.yml
version: '3.8'
services:
  central-api:
    build: .
    ports:
      - "8247:8247"
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://...
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: enrichment_api
```

### **6.2 Scaling Strategy**
- **Horizontal:** Multiple API instances behind load balancer
- **Caching:** Redis cluster for response caching
- **Database:** Read replicas for analytics queries
- **CDN:** Static content delivery optimization

---

## 📈 **Success Metrics**

### **Technical Success**
- [ ] 4/8 providers integrated and functional
- [ ] <2 second average response time
- [ ] >99% uptime
- [ ] >95% cache hit rate for repeated requests

### **Business Success**
- [ ] 50% reduction in individual API management overhead
- [ ] Unified billing and cost tracking
- [ ] Improved data quality through provider fallbacks
- [ ] Standardized enrichment across all applications

---

## 🔄 **Phase 2 Roadmap (Month 2)**

### **Additional Provider Integration**
- [ ] Fix and integrate Wiza (LinkedIn extraction)
- [ ] Research and integrate Surfe (B2B search)
- [ ] Configure Coresignal (Business profiles)
- [ ] Add BigData Corp (Brazilian market)

### **Advanced Features**
- [ ] ML-based confidence scoring
- [ ] Automated data quality validation
- [ ] Provider cost optimization
- [ ] Real-time data synchronization

---

## 🎯 **Immediate Next Steps**

1. **Start Week 1 Implementation** - Set up project structure
2. **Configure Development Environment** - Redis, PostgreSQL, testing frameworks
3. **Implement GitHub Provider First** - Lowest complexity, highest confidence
4. **Create Basic Router** - Simple request routing to GitHub
5. **Test End-to-End Flow** - Single provider enrichment working

**Ready to begin implementation immediately with clear technical specifications and working API foundation!** 🚀
