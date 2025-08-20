# People Data Labs Backend Standardization Plan
**Active Plan #72** | Status: **READY TO START** | Priority: **HIGH**

## 📋 Overview
Standardize People Data Labs (PDL) integration to follow the new backend-first architecture pattern, replacing mock endpoints with real proxy calls and integrating into the main enrichment engine.

---

## 🎯 **Current State Analysis**

### **✅ What's Already Implemented**
- Frontend service client: `frontend/src/services/people-data-labs.ts` (comprehensive)
- Mock backend endpoints in `main.py`:
  - `POST /api/v1/integrations/pdl/enrich-person` (mock)
  - `POST /api/v1/integrations/pdl/enrich-company` (mock)
- Configuration: `pdl_api_key` in `config.py`
- UI integration: Full PDL support in `frontend/src/pages/Integrations.tsx`

### **❌ What Needs Standardization**
- No backend service class (`services/third_party/pdl.py`)
- Mock endpoints return fake data instead of proxying to real PDL API
- Not integrated into `RealDataEnrichmentEngine`
- No quota management for PDL in `QuotaManager`

---

## 🚀 **Implementation Plan**

### **Phase 1: Backend Service Creation (30 minutes)**

#### **Step 1.1: Create PDL Backend Service**
**File**: `services/third_party/pdl.py`

**Key Features**:
```python
class PeopleDataLabsService:
    def __init__(self, api_key: Optional[str] = None)
    def enrich_person(self, params: Dict[str, Any]) -> Dict[str, Any]
    def search_people(self, query: Dict[str, Any]) -> Dict[str, Any] 
    def enrich_company(self, params: Dict[str, Any]) -> Dict[str, Any]
    def search_companies(self, query: Dict[str, Any]) -> Dict[str, Any]
    def get_credits(self) -> Dict[str, Any]  # Via headers
    def test_connection(self) -> bool
```

**API Integration**:
- Base URL: `https://api.peopledatalabs.com/v5`
- Authentication: `X-Api-Key` header
- Rate limits: Based on plan (typically 10,000/month free tier)
- Response transformation to standardized format

#### **Step 1.2: Add PDL to Quota Manager**
**File**: `core/enrichment/real_data_enrichment.py`

```python
# Add to QuotaManager.__init__()
"pdl": {"monthly": 10000, "used": 0, "reset_date": None},
```

#### **Step 1.3: Register PDL in Enrichment Engine**
**File**: `core/enrichment/real_data_enrichment.py`

```python
# Add to _initialize_services()
try:
    if settings.pdl_api_key:
        from services.third_party.pdl import PeopleDataLabsService
        self.services["pdl"] = PeopleDataLabsService()
        logger.info("✅ People Data Labs service initialized")
    else:
        logger.warning("❌ PDL API key not found")
except ImportError:
    logger.warning("❌ PDL service not available")
```

### **Phase 2: Replace Mock Endpoints (20 minutes)**

#### **Step 2.1: Replace Person Enrichment Endpoint**
**File**: `main.py`

Replace mock implementation in `enrich_person_pdl()` with:
```python
# Import PDL service
from services.third_party.pdl import PeopleDataLabsService
pdl_service = PeopleDataLabsService(api_key=api_key)

# Real enrichment
result = pdl_service.enrich_person(request_data.get("params", {}))
```

#### **Step 2.2: Replace Company Enrichment Endpoint**
**File**: `main.py`

Replace mock implementation in `enrich_company_pdl()` with real proxy calls.

#### **Step 2.3: Add Missing Endpoints**
Add new endpoints to match frontend capabilities:
- `POST /api/v1/integrations/pdl/search-people`
- `POST /api/v1/integrations/pdl/search-companies`
- `GET /api/v1/integrations/pdl/credits`

### **Phase 3: Enrichment Engine Integration (25 minutes)**

#### **Step 3.1: Add PDL to Person Enrichment Pipeline**
**File**: `core/enrichment/real_data_enrichment.py`

Add PDL enrichment logic to `enrich_person_real()`:
```python
# Try PDL for comprehensive person data
if (
    "pdl" in self.services
    and self.quota_manager.can_make_request("pdl")
    and (email or (first_name and last_name))
):
    try:
        pdl_params = self._build_pdl_person_params(person_data)
        result = self.services["pdl"].enrich_person(pdl_params)
        if result.get("success"):
            self._merge_pdl_person_data(enriched_data, result)
            self.quota_manager.record_request("pdl")
            enriched_data["data_sources"].append("pdl")
            logger.info(f"✅ PDL person enrichment successful")
    except Exception as e:
        logger.error(f"PDL person error: {e!r}")
```

#### **Step 3.2: Add PDL to Company Enrichment Pipeline**
**File**: `core/enrichment/real_data_enrichment.py`

Add PDL company enrichment to `enrich_company_real()`.

#### **Step 3.3: Create PDL Data Merging Methods**
Add helper methods:
- `_build_pdl_person_params()`
- `_merge_pdl_person_data()`
- `_merge_pdl_company_data()`

### **Phase 4: Testing & Validation (15 minutes)**

#### **Step 4.1: API Key Testing**
- Test with real PDL API key
- Verify rate limit handling
- Test error scenarios (invalid key, quota exceeded)

#### **Step 4.2: Integration Testing**
- Test person enrichment pipeline with PDL
- Test company enrichment pipeline with PDL
- Verify data merging and scoring

#### **Step 4.3: Frontend Compatibility**
- Ensure existing frontend client still works
- Test all PDL operations from UI
- Verify credit tracking

---

## 📊 **Technical Specifications**

### **PDL API Integration Details**
```python
# Person Enrichment
GET /v5/person/enrich?email=john@example.com&min_likelihood=6

# Person Search  
POST /v5/person/search
{
  "query": {
    "job_title": ["software engineer"],
    "location": ["san francisco"]
  },
  "size": 10
}

# Company Enrichment
GET /v5/company/enrich?website=example.com&min_likelihood=6

# Company Search
POST /v5/company/search
{
  "query": {
    "industry": ["technology"],
    "size": ["51-200"]
  },
  "size": 10
}
```

### **Response Transformation**
Standardize PDL responses to match our enrichment format:
```python
def _transform_pdl_person(self, pdl_data: Dict) -> Dict:
    return {
        "full_name": pdl_data.get("full_name"),
        "email": pdl_data.get("work_email"),
        "job_title": pdl_data.get("job_title"),
        "company": pdl_data.get("job_company_name"),
        "location": pdl_data.get("location_name"),
        "linkedin": pdl_data.get("linkedin_url"),
        "skills": pdl_data.get("skills", []),
        "experience": pdl_data.get("experience", []),
        "education": pdl_data.get("education", []),
        # ... map all relevant fields
    }
```

### **Error Handling Strategy**
```python
# Rate limit handling
if response.status_code == 429:
    return {"success": False, "error": "Rate limit exceeded", "retry_after": 3600}

# Invalid API key
if response.status_code == 401:
    return {"success": False, "error": "Invalid API key"}

# No data found (404 is normal for PDL)
if response.status_code == 404:
    return {"success": True, "data": None, "message": "No data found"}
```

---

## 🔧 **Configuration Requirements**

### **Environment Variables**
```bash
# Required for PDL integration
PDL_API_KEY=your_pdl_api_key_here

# Optional: Custom rate limits
PDL_MONTHLY_LIMIT=10000  # Default for free tier
PDL_DAILY_LIMIT=1000     # Optional daily limit
```

### **Quota Management**
```python
# Add to QuotaManager
"pdl": {
    "monthly": 10000,     # Free tier limit
    "daily": 1000,        # Optional daily limit
    "used": 0,
    "reset_date": None
}
```

---

## 📋 **Acceptance Criteria**

### **✅ Backend Service**
- [ ] `services/third_party/pdl.py` created with full API coverage
- [ ] All PDL API endpoints properly integrated
- [ ] Error handling and rate limiting implemented
- [ ] Response transformation to standardized format

### **✅ Endpoint Replacement**
- [ ] Mock endpoints replaced with real proxy calls
- [ ] All existing endpoints maintain backward compatibility
- [ ] New endpoints added for search functionality
- [ ] Credits endpoint implemented

### **✅ Enrichment Engine Integration**
- [ ] PDL added to `RealDataEnrichmentEngine`
- [ ] Person enrichment pipeline includes PDL
- [ ] Company enrichment pipeline includes PDL
- [ ] Data merging and scoring updated

### **✅ Testing & Validation**
- [ ] Real API integration tested
- [ ] Frontend compatibility verified
- [ ] Error scenarios handled gracefully
- [ ] Performance acceptable (< 2s response time)

---

## ⚠️ **Risk Mitigation**

### **API Key Security**
- Never expose PDL API key to frontend
- Use backend proxy for all PDL calls
- Implement proper error messages without exposing internals

### **Rate Limiting**
- Respect PDL rate limits (typically 10 requests/second)
- Implement exponential backoff for rate limit errors
- Track quota usage to prevent overages

### **Data Quality**
- Validate PDL responses before merging
- Handle missing or incomplete data gracefully  
- Maintain data source attribution

### **Performance**
- Cache frequently requested data
- Implement timeout handling (30s max)
- Use async operations where possible

---

## 🚀 **Success Metrics**

### **Technical Metrics**
- [ ] 100% of mock endpoints replaced with real proxy calls
- [ ] < 2 second average response time for PDL enrichment
- [ ] 99%+ uptime for PDL integration
- [ ] Zero API key exposures to frontend

### **Functional Metrics**  
- [ ] PDL data successfully merged into enrichment pipeline
- [ ] Frontend PDL operations work without changes
- [ ] Credit tracking accurate and real-time
- [ ] Error handling provides useful feedback

### **Quality Metrics**
- [ ] PDL enrichment improves overall enrichment scores
- [ ] Data consistency across all PDL operations
- [ ] Proper logging for debugging and monitoring
- [ ] Documentation updated and accurate

---

## 📅 **Timeline**

### **Day 1 (90 minutes total)**
- **Phase 1**: Backend service creation (30 min)
- **Phase 2**: Replace mock endpoints (20 min) 
- **Phase 3**: Enrichment engine integration (25 min)
- **Phase 4**: Testing & validation (15 min)

### **Immediate Next Steps**
1. Create `services/third_party/pdl.py` with full PDL API integration
2. Add PDL to quota manager and enrichment engine initialization
3. Replace mock endpoints in `main.py` with real proxy calls
4. Test with real PDL API key and validate functionality

---

## 🎯 **Post-Completion Benefits**

### **Consistency**
- PDL follows same backend-first pattern as other providers
- Unified error handling and response formats
- Consistent API key management

### **Functionality**
- Real PDL data instead of mock responses
- Full PDL API coverage (person/company search + enrichment)
- Integrated into main enrichment pipeline for automatic use

### **Security & Performance**
- API keys protected on backend
- Proper rate limiting and quota management
- Optimized for production use

**🚀 Ready to execute! This plan will complete the PDL standardization and bring it in line with the new backend-first architecture.**
