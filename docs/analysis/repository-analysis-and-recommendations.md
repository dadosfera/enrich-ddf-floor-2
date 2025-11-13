# Repository Analysis: dev-demo-lattes & Related Repositories

**Date**: 2025-01-27
**Purpose**: Analyze repositories for Cars, Real Estate, and People enrichment pages

---

## 🔍 Repository Investigation Summary

### Primary Target: `dadosfera/dev-demo-lattes`

- **Status**: ❌ **Does Not Exist (404)**
- **GitHub CLI Confirmation**: Repository not found in Dadosfera organization
- **Note**: "Lattes" refers to Brazilian academic CV platform

### Related Repository Found: `dadosfera/apify-crawler-lattes`

- **Status**: ✅ **Accessible (Private Repository)**
- **Description**: "Crawler do Apify que obtem dados do Lates. Utiliza 2captcha para quebrar Captchas"
- **Technology**: Apify crawler using Puppeteer
- **Purpose**: Downloads Lattes CVs from researcher names
- **Key Feature**: Uses 2captcha to solve CAPTCHAs

### Related Repository Found: `dadosfera/dataapp-enriquecimento`

- **Status**: ✅ **Accessible**
- **Description**: "Data app para enriquecimento de dados de pessoas" (People enrichment data app)
- **Technology**: Streamlit-based application
- **Key Features**: CPF, email, phone, LinkedIn enrichment

---

## 📊 Analysis of `dataapp-enriquecimento`

### Key Components Found

#### 1. **Enrichment Functions** (`app/enrich.py`)

- **People Data Labs Integration**: LinkedIn profile enrichment
- **Function**: `enrich(url)` - Enriches person data from LinkedIn URL
- **Output**: JSON data with person details

#### 2. **Validators** (`app/utils/validators.py`)

```python
- validate_cpf(cpf)          # Brazilian CPF validation
- validate_email(email)       # Email format validation
- validate_telefone(telefone) # Phone number validation
- validate_url(url)           # URL validation
- validate_linkedin_profile_url(url) # LinkedIn URL validation
```

#### 3. **Enrichment Services**

- **ZeroBounce**: Email validation (`utils/zerobounce_single.py`)
- **Apollo**: Person matching (`utils/apollo_single.py`)
- **People Data Labs**: LinkedIn enrichment (`enrich.py`)

#### 4. **UI Patterns** (`app/views/free.py`)

- Single input field that auto-detects data type (CPF, email, phone, LinkedIn)
- Conditional processing based on detected data type
- Results display with enriched data

### What We Can Reuse

✅ **CPF Validation Logic**: Can be integrated into People enrichment
✅ **Email Validation**: ZeroBounce integration pattern
✅ **LinkedIn Enrichment**: People Data Labs integration
✅ **Data Type Detection**: Auto-detection pattern for input
✅ **Validation Functions**: Reusable validators for Brazilian data

---

## 🎯 Recommendations for New Pages

### 1. **People Enrichment Page** (Priority: High)

#### Current State

- ✅ Partially exists as `Contacts.tsx`
- ✅ Has People Data Labs integration
- ✅ Has BigDataCorp CPF enrichment

#### Enhancements Needed

```typescript
// New features to add:
- Lattes CV integration (if dev-demo-lattes becomes available)
- Enhanced CPF validation (from dataapp-enriquecimento)
- Email validation with ZeroBounce
- Phone number enrichment
- Academic profile display (publications, research areas)
- Professional timeline visualization
```

#### Implementation Plan

1. **Extend Contact Model** → Create enhanced Person model
2. **Add Validators** → Import CPF/email/phone validators from dataapp-enriquecimento
3. **Integrate Services**:
   - ZeroBounce for email validation
   - Apollo for person matching (if available)
   - Lattes CV API (if dev-demo-lattes provides integration)
4. **Create UI Components**:
   - Auto-detection input field (like dataapp-enriquecimento)
   - Academic profile section
   - Publication list component
   - Professional timeline

---

### 2. **Cars Enrichment Page** (Priority: Medium)

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

#### Implementation Pattern

Follow existing `Companies.tsx` pattern:

- List view with search
- Card-based display
- Enrichment button
- Detail view with enriched data

---

### 3. **Real Estate Enrichment Page** (Priority: Medium)

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

#### Implementation Pattern

- List view with map integration
- Property detail cards
- Market analysis charts
- Comparables table
- Amenities display

---

## 🔧 Technical Implementation Guide

### Database Models

#### Enhanced Person Model

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

#### Car Model

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

#### Real Estate Model

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

### Backend API Endpoints

#### People Endpoints

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
POST   /api/v1/people/enrich-by-lattes   # Enrich by Lattes ID
```

#### Cars Endpoints

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

#### Real Estate Endpoints

```python
GET    /api/v1/real-estate               # List properties
POST   /api/v1/real-estate               # Create property
GET    /api/v1/real-estate/{id}          # Get property details
PUT    /api/v1/real-estate/{id}          # Update property
DELETE /api/v1/real-estate/{id}          # Delete property
POST   /api/v1/real-estate/{id}/enrich   # Trigger enrichment
POST   /api/v1/real-estate/enrich-by-address # Enrich by address
```

### Frontend Pages Structure

#### People Page (`frontend/src/pages/People.tsx`)

```typescript
// Follow pattern from Contacts.tsx but enhanced:
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

#### Cars Page (`frontend/src/pages/Cars.tsx`)

```typescript
// Follow pattern from Companies.tsx:
- List view with search (VIN, license plate, make/model)
- Card display with key vehicle info
- Enrichment status indicators
- Detail view with:
  - Basic specs
  - Market value chart
  - History timeline
  - Maintenance records
```

#### Real Estate Page (`frontend/src/pages/RealEstate.tsx`)

```typescript
// New pattern with map integration:
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

## 📋 Reusable Components from dataapp-enriquecimento

### 1. **Validators** (`utils/validators.py`)

```python
# Can be adapted for our FastAPI backend:
from app.utils.validators import (
    validate_cpf,
    validate_email,
    validate_telefone,
    validate_linkedin_profile_url,
)
```

### 2. **Enrichment Pattern**

```python
# Pattern from enrich.py:
def enrich_person_by_linkedin(url: str) -> Dict:
    # Use People Data Labs API
    # Return enriched data
    pass
```

### 3. **Auto-Detection Pattern**

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

## 🚀 Implementation Priority

### Phase 1: People Page Enhancement (Week 1-2)

1. ✅ Create enhanced Person model
2. ✅ Add CPF/email/phone validators
3. ✅ Integrate ZeroBounce email validation
4. ✅ Enhance People Data Labs integration
5. ✅ Create People.tsx page with auto-detection
6. ⏳ Add Lattes CV integration (if dev-demo-lattes available)

### Phase 2: Cars Page (Week 3-4)

1. ✅ Create Car model
2. ✅ Create backend APIs
3. ✅ Research and integrate VIN decoding APIs
4. ✅ Research market value APIs
5. ✅ Create Cars.tsx page
6. ⏳ Integrate Brazilian vehicle databases

### Phase 3: Real Estate Page (Week 5-6)

1. ✅ Create RealEstate model
2. ✅ Create backend APIs
3. ✅ Research property valuation APIs
4. ✅ Integrate map components
5. ✅ Create RealEstate.tsx page
6. ⏳ Integrate Brazilian property databases

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
- ⏳ **Lattes CV API**: Academic profiles (if dev-demo-lattes provides)
- ⏳ **VIN Decoding APIs**: For Cars page
- ⏳ **Property Valuation APIs**: For Real Estate page
- ⏳ **Geographic APIs**: Maps, location data

---

## 📝 Next Steps

1. **Request Access**: Contact Dadosfera team for `dev-demo-lattes` access
2. **Review Code**: Analyze `dataapp-enriquecimento` in detail
3. **Extract Components**: Identify reusable validators and patterns
4. **Start Implementation**: Begin with People page enhancement
5. **Research APIs**: Identify and evaluate data sources for Cars and Real Estate

---

## 📚 References

- **dataapp-enriquecimento**: https://github.com/dadosfera/dataapp-enriquecimento
- **Lattes Platform**: https://lattes.cnpq.br/
- **People Data Labs**: Already integrated
- **ZeroBounce**: Email validation API
- **Apollo**: Person matching API

---

**Status**: ✅ **Analysis Complete**
**Action**: Proceed with implementation using patterns from `dataapp-enriquecimento`
**Awaiting**: Access to `dev-demo-lattes` for Lattes CV integration
