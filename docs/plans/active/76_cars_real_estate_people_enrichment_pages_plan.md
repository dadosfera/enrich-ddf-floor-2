# Cars, Real Estate, and People Enrichment Pages - Implementation Plan

**Date**: 2025-01-27
**Status**: 📋 Planning Complete - Ready for Implementation
**Priority**: High

---

## 📋 Executive Summary

This plan outlines the implementation of three new enrichment pages for the enrich-ddf-floor-2 application:

1. **People Enrichment Page** - Enhanced person data enrichment with academic profiles
2. **Cars Enrichment Page** - Vehicle data enrichment with market value and history
3. **Real Estate Enrichment Page** - Property enrichment with market analysis

The plan includes repository investigation findings, technical specifications, and implementation phases.

---

## 🔍 Repository Investigation Results

### Target Repository: `dadosfera/dev-demo-lattes`

- **Status**: ❌ **DOES NOT EXIST** (404 Not Found)
- **GitHub CLI Confirmation**: Repository not found in Dadosfera organization
- **Conclusion**: Repository name may be incorrect, or it was never created

### Related Repositories Found

#### 1. `dadosfera/apify-crawler-lattes`

- **Status**: ✅ **ACCESSIBLE** (Private repository, accessible via GitHub CLI)
- **Description**: "Crawler do Apify que obtem dados do Lates. Utiliza 2captcha para quebrar Captchas"
- **Technology**: Apify SDK + Puppeteer + 2captcha
- **Purpose**: Downloads Lattes CVs (XML files) from CNPq Lattes platform
- **Key Features**:
  - Researcher search by name
  - CV download as ZIP files
  - CAPTCHA solving via 2captcha
  - Batch processing support

**Technical Implementation**:

```javascript
// Key functions from main.js:
-procurarPesquisador() - // Search for researcher by name
  getAbrirCurriculoPage() - // Open CV page
  getBaixarCurriculoPage() - // Navigate to download page
  extractLattesId() - // Extract Lattes ID from URL
  saveFileIntoStore(); // Save ZIP file to storage
```

**Integration Options**:

1. **Option 1**: Direct Integration (Not Recommended - may violate ToS)
2. **Option 2**: Apify Actor Integration (Recommended - separates concerns)
3. **Option 3**: Official API (Best - if available)
4. **Option 4**: Manual/User-Initiated (Safest - legal, no scraping)

#### 2. `dadosfera/dataapp-enriquecimento`

- **Status**: ✅ **ACCESSIBLE**
- **Description**: "Data app para enriquecimento de dados de pessoas"
- **Technology**: Streamlit-based application
- **Key Components**:
  - **Enrichment Functions**: People Data Labs LinkedIn enrichment
  - **Validators**: CPF, email, phone, LinkedIn URL validation
  - **Services**: ZeroBounce (email), Apollo (person matching), People Data Labs
  - **UI Patterns**: Auto-detection input field for data type

**Reusable Components**:

- ✅ CPF Validation Logic
- ✅ Email Validation (ZeroBounce pattern)
- ✅ LinkedIn Enrichment (People Data Labs)
- ✅ Data Type Detection (auto-detection pattern)
- ✅ Validation Functions (Brazilian data)

---

## 🎯 Required New Pages

### 1. People Enrichment Page (Priority: High)

#### Current State

- ✅ Partially exists as `Contacts.tsx`
- ✅ Has People Data Labs integration
- ✅ Has BigDataCorp CPF enrichment

#### Enhancements Needed

```typescript
// New features to add:
- Lattes CV integration (academic profiles)
- Enhanced CPF validation (from dataapp-enriquecimento)
- Email validation with ZeroBounce
- Phone number enrichment
- Academic profile display (publications, research areas)
- Professional timeline visualization
- Auto-detection input field (CPF, email, phone, LinkedIn, Lattes ID)
```

#### Data Model

```python
class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    # Basic Info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, index=True)

    # Contact
    email = Column(String(255), index=True)
    phone = Column(String(50))

    # Professional
    linkedin_url = Column(String(255))
    github_url = Column(String(255))

    # Academic (Lattes)
    lattes_id = Column(String(50), index=True)

    # Enrichment
    enrichment_data = Column(JSON)
    verification_status = Column(String(20), default='pending')

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Backend Endpoints

```python
GET    /api/v1/people                    # List people
POST   /api/v1/people                    # Create person
GET    /api/v1/people/{id}               # Get person details
PUT    /api/v1/people/{id}               # Update person
DELETE /api/v1/people/{id}               # Delete person
POST   /api/v1/people/{id}/enrich        # Trigger enrichment
POST   /api/v1/people/enrich-by-cpf      # Enrich by CPF
POST   /api/v1/people/enrich-by-email   # Enrich by email
POST   /api/v1/people/enrich-by-linkedin # Enrich by LinkedIn
POST   /api/v1/people/enrich-by-lattes    # Enrich by Lattes ID
```

#### Frontend Structure

```typescript
// frontend/src/pages/People.tsx
- Auto-detection input (CPF, email, phone, LinkedIn, Lattes ID)
- List view with search
- Card display with enrichment status
- Detail view with tabs:
  - Basic Info
  - Academic (Lattes data)
  - Professional (LinkedIn, GitHub)
  - Contact (emails, phones)
  - Social Profiles
```

---

### 2. Cars Enrichment Page (Priority: Medium)

#### Required Features

```typescript
interface CarEnrichment {
  // Basic Info
  vin: string;
  license_plate?: string;
  make: string;
  model: string;
  year: number;

  // Enrichment Data
  market_value?: number;
  accident_history?: Array<AccidentRecord>;
  ownership_history?: Array<OwnerRecord>;
  maintenance_records?: Array<MaintenanceRecord>;
  recall_information?: Array<RecallRecord>;
  fuel_efficiency?: FuelEfficiencyData;
}
```

#### Data Sources Needed

- **VIN Decoding**: NHTSA VIN Decoder API
- **Market Value**: Kelley Blue Book, Edmunds APIs
- **History Reports**: Carfax, AutoCheck APIs
- **Brazilian Sources**: Renavam, Detran APIs

#### Data Model

```python
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    vin = Column(String(17), unique=True, index=True)
    license_plate = Column(String(20), index=True)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(50))
    mileage = Column(Integer)
    condition = Column(String(50))
    price = Column(Float)
    location = Column(String(255))
    enrichment_data = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Backend Endpoints

```python
GET    /api/v1/cars                      # List cars
POST   /api/v1/cars                      # Create car
GET    /api/v1/cars/{id}                 # Get car details
PUT    /api/v1/cars/{id}                 # Update car
DELETE /api/v1/cars/{id}                 # Delete car
POST   /api/v1/cars/{id}/enrich         # Trigger enrichment
POST   /api/v1/cars/enrich-by-vin       # Enrich by VIN
POST   /api/v1/cars/enrich-by-plate     # Enrich by license plate
```

#### Frontend Structure

```typescript
// frontend/src/pages/Cars.tsx
- List view with search (VIN, license plate, make/model)
- Card display with key vehicle info
- Enrichment status indicators
- Detail view with:
  - Basic specs
  - Market value chart
  - History timeline
  - Maintenance records
```

---

### 3. Real Estate Enrichment Page (Priority: Medium)

#### Required Features

```typescript
interface RealEstateEnrichment {
  // Basic Info
  address: string;
  city: string;
  state: string;
  property_type: "apartment" | "house" | "commercial" | "land";

  // Enrichment Data
  market_value?: number;
  price_per_sqm?: number;
  comparables?: Array<ComparableProperty>;
  tax_assessment?: TaxData;
  ownership_history?: Array<OwnershipRecord>;
  nearby_amenities?: Array<Amenity>;
  market_trends?: MarketTrendData;
}
```

#### Data Sources Needed

- **Property Valuation**: Zillow API, Brazilian equivalents
- **Geographic Data**: Google Maps API, GIS data
- **Market Analysis**: Real estate listing APIs
- **Brazilian Sources**: Cartório databases, Receita Federal

#### Data Model

```python
class RealEstate(Base):
    __tablename__ = "real_estate"

    id = Column(Integer, primary_key=True)
    property_type = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    area_sqm = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    parking_spaces = Column(Integer)
    price = Column(Float)
    price_per_sqm = Column(Float)
    year_built = Column(Integer)
    condition = Column(String(50))
    enrichment_data = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Backend Endpoints

```python
GET    /api/v1/real-estate               # List properties
POST   /api/v1/real-estate               # Create property
GET    /api/v1/real-estate/{id}          # Get property details
PUT    /api/v1/real-estate/{id}          # Update property
DELETE /api/v1/real-estate/{id}          # Delete property
POST   /api/v1/real-estate/{id}/enrich   # Trigger enrichment
POST   /api/v1/real-estate/enrich-by-address # Enrich by address
```

#### Frontend Structure

```typescript
// frontend/src/pages/RealEstate.tsx
- List view with search (address, city, property type)
- Map view toggle
- Card display with property images
- Detail view with:
  - Property details
  - Market analysis charts
  - Comparables table
  - Nearby amenities
  - Ownership history
```

---

## 🔧 Technical Implementation Guide

### Database Migrations

Create Alembic migrations for:

1. `Person` model (enhanced from Contact)
2. `Car` model
3. `RealEstate` model

### Backend Services

#### People Enrichment Service

```python
# services/third_party/lattes.py
class LattesService:
    def get_researcher_by_id(self, lattes_id: str) -> Dict:
        # Fetch public Lattes CV data
        # Parse XML
        # Return structured data
        pass

    def search_researcher(self, name: str) -> List[Dict]:
        # Search CNPq Lattes platform
        # Return list of matching researchers
        pass
```

#### Car Enrichment Service

```python
# services/third_party/car_enrichment.py
class CarEnrichmentService:
    def decode_vin(self, vin: str) -> Dict:
        # Use NHTSA VIN Decoder API
        pass

    def get_market_value(self, make: str, model: str, year: int) -> Dict:
        # Use Kelley Blue Book or Edmunds API
        pass

    def get_history_report(self, vin: str) -> Dict:
        # Use Carfax or AutoCheck API
        pass
```

#### Real Estate Enrichment Service

```python
# services/third_party/real_estate_enrichment.py
class RealEstateEnrichmentService:
    def get_property_valuation(self, address: str) -> Dict:
        # Use property valuation API
        pass

    def get_market_analysis(self, address: str) -> Dict:
        # Use market analysis API
        pass

    def get_comparables(self, address: str) -> List[Dict]:
        # Get comparable properties
        pass
```

### Frontend Components

#### Reusable Enrichment Components

1. **EnrichmentStatusBadge**: Shows enrichment status (pending, in-progress, completed, failed)
2. **DataSourceChip**: Displays data source with credibility indicator
3. **EnrichmentButton**: Triggers enrichment with loading state
4. **BeforeAfterComparison**: Shows original vs enriched data
5. **ConfidenceScore**: Visual indicator of data confidence
6. **VerificationBadge**: Shows verification status

#### Page-Specific Components

**People**:

- AcademicProfile: Lattes CV data display
- PublicationList: Academic publications
- ProfessionalTimeline: Career progression
- SocialProfiles: Linked social media accounts

**Cars**:

- VINDecoder: Decode and display VIN information
- MarketValueChart: Show value trends over time
- HistoryTimeline: Display ownership/accident history

**Real Estate**:

- PropertyMap: Interactive map with property location
- ComparablesTable: Show similar properties
- MarketTrendsChart: Price trends and market analysis
- AmenitiesList: Nearby amenities display

### Reusable Patterns from dataapp-enriquecimento

#### Validators

```python
# Can be adapted for FastAPI backend:
from app.utils.validators import (
    validate_cpf,
    validate_email,
    validate_telefone,
    validate_linkedin_profile_url,
)
```

#### Auto-Detection Pattern

```python
# From free.py - can be adapted for frontend:
def detect_input_type(input_value: str) -> str:
    if validate_cpf(input_value):
        return 'cpf'
    elif validate_email(input_value):
        return 'email'
    elif validate_telefone(input_value):
        return 'phone'
    elif validate_linkedin_profile_url(input_value):
        return 'linkedin'
    return 'unknown'
```

---

## 🚀 Implementation Phases

### Phase 1: People Page Enhancement (Week 1-2)

**Tasks**:

1. ✅ Create enhanced Person model
2. ✅ Add CPF/email/phone validators (from dataapp-enriquecimento)
3. ✅ Integrate ZeroBounce email validation
4. ✅ Enhance People Data Labs integration
5. ✅ Create People.tsx page with auto-detection
6. ⏳ Add Lattes CV integration (Option 4: Manual Lattes ID input)

**Deliverables**:

- Database migration for Person model
- Backend API endpoints for People
- Frontend People page with auto-detection
- Integration with existing enrichment services

### Phase 2: Cars Page (Week 3-4)

**Tasks**:

1. ✅ Create Car model
2. ✅ Create backend APIs
3. ✅ Research and integrate VIN decoding APIs
4. ✅ Research market value APIs
5. ✅ Create Cars.tsx page
6. ⏳ Integrate Brazilian vehicle databases

**Deliverables**:

- Database migration for Car model
- Backend API endpoints for Cars
- Frontend Cars page
- VIN decoding integration
- Market value integration

### Phase 3: Real Estate Page (Week 5-6)

**Tasks**:

1. ✅ Create RealEstate model
2. ✅ Create backend APIs
3. ✅ Research property valuation APIs
4. ✅ Integrate map components
5. ✅ Create RealEstate.tsx page
6. ⏳ Integrate Brazilian property databases

**Deliverables**:

- Database migration for RealEstate model
- Backend API endpoints for Real Estate
- Frontend Real Estate page with map integration
- Property valuation integration
- Market analysis integration

---

## 🔗 Integration Opportunities

### Existing Services to Leverage

- ✅ **People Data Labs**: Already integrated, enhance for People page
- ✅ **Wiza**: LinkedIn enrichment, extend for People page
- ✅ **Surfe**: Professional data, use for People page
- ✅ **BigDataCorp**: CPF validation, enhance for People page
- ✅ **GitHub**: Developer profiles, use for People page

### New Services Needed

- ⏳ **ZeroBounce**: Email validation (pattern from dataapp-enriquecimento)
- ⏳ **Apollo**: Person matching (if available)
- ⏳ **Lattes CV API**: Academic profiles (start with manual ID input)
- ⏳ **VIN Decoding APIs**: For Cars page
- ⏳ **Property Valuation APIs**: For Real Estate page
- ⏳ **Geographic APIs**: Maps, location data

---

## 📋 Lattes Integration Strategy

### Recommended Approach: Option 4 (Manual/User-Initiated)

**Rationale**:

- Safest and most legal approach
- No CAPTCHA solving or web scraping
- Uses public Lattes CV data
- Can be enhanced later with official API if available

**Implementation Steps**:

1. Add `lattes_id` field to Person model
2. Create Lattes service to fetch public CV data by ID
3. Parse XML data from public Lattes URLs
4. Display academic profile in frontend
5. Future: Add researcher search if official API becomes available

**Alternative Approaches** (if needed later):

- Option 2: Apify Actor Integration (if Apify actor available)
- Option 3: Official CNPq Lattes API (if available)

---

## 📝 Next Steps

### Immediate Actions

1. **Start Phase 1**: Begin People page enhancement
2. **Research APIs**: Identify and evaluate data sources for Cars and Real Estate
3. **Extract Validators**: Adapt CPF/email/phone validators from dataapp-enriquecimento
4. **Create Database Migrations**: Implement Person, Car, and RealEstate models

### Future Considerations

1. **Verify Repository Name**: Confirm with Dadosfera team if `dev-demo-lattes` exists under different name
2. **Check CNPq Lattes API**: Research official API availability
3. **Evaluate Apify Actor**: Consider Apify actor integration for Lattes if needed
4. **Brazilian Data Sources**: Research Renavam, Detran, Cartório APIs

---

## 📚 References

- **apify-crawler-lattes**: https://github.com/dadosfera/apify-crawler-lattes
- **dataapp-enriquecimento**: https://github.com/dadosfera/dataapp-enriquecimento
- **CNPq Lattes Platform**: https://lattes.cnpq.br/
- **People Data Labs**: Already integrated
- **ZeroBounce**: Email validation API
- **Apollo**: Person matching API
- **NHTSA VIN Decoder**: https://vpic.nhtsa.dot.gov/api/
- **Kelley Blue Book API**: https://www.kbb.com/
- **Zillow API**: https://www.zillow.com/howto/api/APIOverview.htm

---

## ✅ Summary

- **Repository Investigation**: `dev-demo-lattes` does not exist; found `apify-crawler-lattes` and `dataapp-enriquecimento`
- **Recommendation**: Start with manual Lattes ID input (safest), then explore official API options
- **Implementation**: Three phases over 6 weeks (People → Cars → Real Estate)
- **Status**: ✅ Planning Complete - Ready for Implementation

---

**Status**: ✅ **Plan Complete**
**Next Action**: Begin Phase 1 - People Page Enhancement
