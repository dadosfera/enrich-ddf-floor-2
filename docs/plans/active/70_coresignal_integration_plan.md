# Coresignal Business Profile API Integration Plan

**Status**: Planned
**Priority**: Medium
**Estimated Effort**: 8-12 hours
**Integration Type**: Company Data Enrichment

## Overview

Integration plan for adding [Coresignal's Business Profile API](https://coresignal.com/solutions/company-data-api/) to the existing enrichment platform. This will be the 5th major data provider, following the established patterns used for BigData Corp, Wiza, Surfe, and People Data Labs.

## API Details

- **Base URL**: `https://api.coresignal.com/cdapi/v1/`
- **Authentication**: API Key in header (`Authorization: Bearer {key}`)
- **Rate Limits**: 5 requests/second (default)
- **Credit System**: Search credits + Collect credits
- **Free Trial**: 200 credits available

### Available APIs
1. **Base Company API**: 74M+ records, 70+ data points
2. **Clean Company API**: 40M+ records, 80+ data points, enriched
3. **Multi-Source Company API**: 40M+ records, 500+ data points, AI-enriched

## Implementation Plan

### 1. Prerequisites & Discovery
- [ ] Review official documentation & playground
- [ ] Test authentication with trial API key
- [ ] Understand credit system and rate limits
- [ ] Map response structures to our data models

**Key Endpoints**:
- `POST /company/search` - Search companies with filters
- `GET /company` - Retrieve company profiles by IDs
- Credit tracking via headers: `X-Credits-Remaining`, `X-Credits-Used`

### 2. Backend Enhancements (FastAPI)

**Create Router**: `/api/v1/integrations/coresignal/`

**Endpoints to Implement**:
- [ ] `POST /search-companies` - Proxy to Coresignal Search API
- [ ] `POST /enrich-companies` - Enrich companies by IDs/domains
- [ ] `GET /credits` - Return credit information
- [ ] `POST /test-connection` - Validate API key

**Configuration**:
- [ ] Add `CORESIGNAL_API_KEY` environment variable
- [ ] Support user-specific keys via request headers
- [ ] Add error handling for Coresignal 4xx/5xx responses
- [ ] Implement logging at INFO level

### 3. Frontend Service (TypeScript)

**Create**: `frontend/src/services/coresignal.ts`

**Interfaces**:
```typescript
interface CoresignalCredentials {
  apiKey: string;
}

interface CompanySearchRequest {
  filters: {
    name?: string[];
    domain?: string[];
    industry?: string[];
    country?: string[];
    employee_count_min?: number;
    employee_count_max?: number;
    annual_revenue_min?: number;
    annual_revenue_max?: number;
  };
  limit?: number;
  offset?: number;
}

interface CoresignalCompanyData {
  id: string;
  name: string;
  domain?: string;
  industry?: string;
  employee_count?: number;
  annual_revenue?: number;
  founded?: number;
  location?: {
    country?: string;
    city?: string;
    address?: string;
  };
  funding?: {
    total_funding?: number;
    funding_rounds_count?: number;
    last_funding_date?: string;
  };
  growth_metrics?: {
    employee_count_change_monthly?: number;
    employee_count_change_quarterly?: number;
  };
  // ... additional fields
}

interface CoresignalResponse<T> {
  status: number;
  data?: T;
  error?: {
    type: string;
    message: string;
  };
  credits_remaining?: number;
  credits_used?: number;
}
```

**Methods**:
- [ ] `setCredentials(credentials: CoresignalCredentials)`
- [ ] `testConnection(): Promise<boolean>`
- [ ] `getCredits(): Promise<CoresignalResponse<CoresignalCreditsData>>`
- [ ] `searchCompanies(request: CompanySearchRequest): Promise<CoresignalResponse<CoresignalCompanyData[]>>`
- [ ] `enrichCompanies(ids: string[]): Promise<CoresignalResponse<CoresignalCompanyData[]>>`
- [ ] Backend proxy methods for server-side requests

### 4. UI / React Components

**Integration Card**:
- [ ] Add Coresignal card to main Integrations page
- [ ] Use `CorporateFare` icon from Material-UI
- [ ] Status indicator (connected/disconnected/error)
- [ ] Configure button opens credential dialog

**Configuration Dialog**:
- [ ] API key input field
- [ ] Connection test functionality
- [ ] Credits display after successful connection
- [ ] Save to `credentialsService`

**Enrichment Tools**:
- [ ] **Company Search Dialog**:
  - Filters: name, domain, industry, country, employee range, revenue range
  - Advanced search with multiple criteria
  - Results displayed in cards with key metrics
- [ ] **Company Enrich Dialog**:
  - Input: company IDs or domains
  - Bulk enrichment capabilities
  - Detailed company profiles with growth metrics

**Results Display**:
- [ ] Company cards showing:
  - Name, domain, industry
  - Employee count and growth trends
  - Revenue information
  - Funding details
  - Location data
  - Growth metrics (monthly/quarterly changes)

### 5. Credentials Management

**Extend Credentials Service**:
- [ ] Add `coresignal` to `IntegrationName` type
- [ ] Update `IntegrationKeys` page to include Coresignal
- [ ] Ensure key persistence in localStorage
- [ ] Support backend proxy via custom headers

### 6. Testing

**Playwright Tests**:
- [ ] Update navigation tests to include Coresignal card
- [ ] Test configuration dialog opening and form validation
- [ ] Mock API responses with MSW for deterministic testing
- [ ] Test enrichment workflow end-to-end

**Unit Tests**:
- [ ] Service layer validation and error handling
- [ ] Data transformation functions
- [ ] Credit tracking and rate limiting

### 7. Performance & Rate Limiting

**Rate Limit Handling**:
- [ ] Implement request queue (≤4 req/s to stay under limit)
- [ ] Exponential backoff on HTTP 429 responses
- [ ] Display rate limit status in UI

**Credit Management**:
- [ ] Real-time credit display after each request
- [ ] Warning alerts when credits are low
- [ ] Credit usage analytics

### 8. Documentation & Configuration

**Environment Setup**:
- [ ] Add `CORESIGNAL_API_KEY=` to `.env.example`
- [ ] Update `README.md` with Coresignal integration instructions
- [ ] Document free trial setup process

**API Documentation**:
- [ ] Add Coresignal link to API Documentation accordion
- [ ] Include usage examples and best practices
- [ ] Document data mapping and transformation logic

### 9. Deployment & Validation

**Pre-deployment Checklist**:
- [ ] All tests passing (`npm run test`, `pytest`, Playwright)
- [ ] Linter passing with no new warnings
- [ ] Manual smoke testing with trial API key
- [ ] Code coverage maintains existing baseline

**Integration Testing**:
- [ ] Test with real Coresignal trial account
- [ ] Verify credit tracking accuracy
- [ ] Test rate limiting behavior
- [ ] Validate data transformation correctness

## Technical Considerations

### API Tiers
Coresignal offers three API tiers with different data richness:
1. **Base API**: Basic company information (70+ fields)
2. **Clean API**: Enhanced and standardized data (80+ fields)
3. **Multi-Source API**: Premium with AI enrichment (500+ fields)

Implementation will target the Multi-Source API for maximum data value.

### Data Mapping
Map Coresignal fields to our standardized `CompanyData` interface:
- Basic info: name, domain, industry, employee_count
- Location: address, city, country
- Financial: revenue, funding rounds, valuation
- Growth: employee changes, hiring trends
- Technology: tech stack, software usage

### Credit Optimization
- Implement search-first workflow (cheaper search credits vs collect credits)
- Batch requests where possible
- Cache frequently accessed company data
- Provide credit usage estimates before operations

## Success Criteria

- [ ] Successful API integration with all CRUD operations
- [ ] Smooth user experience matching existing integrations
- [ ] Comprehensive test coverage (>90%)
- [ ] Rate limiting and error handling working correctly
- [ ] Credit tracking accurate and informative
- [ ] Documentation complete and clear

## Risk Mitigation

**API Changes**: Follow established patterns from other integrations to minimize custom code
**Rate Limits**: Implement conservative rate limiting with user feedback
**Credit Management**: Clear usage display and warnings to prevent surprise costs
**Data Quality**: Validate and transform all API responses consistently

## Timeline

- **Week 1**: Backend router, service layer, basic API integration
- **Week 2**: Frontend components, UI integration, credential management
- **Week 3**: Testing, documentation, polish and deployment

## Post-Implementation

- Monitor API usage and performance
- Gather user feedback on data quality and usefulness
- Consider implementing data caching for frequently accessed companies
- Evaluate upgrade to higher API tiers based on usage patterns

---

**References**:
- [Coresignal Company Data API](https://coresignal.com/solutions/company-data-api/)
- [API Documentation](https://docs.coresignal.com/)
- [Pricing Plans](https://coresignal.com/pricing/)
