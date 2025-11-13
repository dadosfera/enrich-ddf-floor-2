# Lattes Repositories Investigation - Final Findings

**Date**: 2025-01-27
**Investigation Method**: GitHub CLI (`gh`)

---

## 🔍 Repository Access Results

### Target Repository: `dadosfera/dev-demo-lattes`
- **Status**: ❌ **DOES NOT EXIST**
- **GitHub CLI Result**: `GraphQL: Could not resolve to a Repository`
- **API Result**: `404 Not Found`
- **Conclusion**: Repository name may be incorrect, or it was never created

### Related Repository Found: `dadosfera/apify-crawler-lattes`
- **Status**: ✅ **ACCESSIBLE** (Private repository, but accessible via GitHub CLI)
- **Visibility**: Private
- **Description**: "Crawler do Apify que obtem dados do Lates. Utiliza 2captcha para quebrar Captchas"
- **Technology Stack**:
  - Apify SDK
  - Puppeteer (headless browser)
  - Puppeteer-extra with reCAPTCHA plugin
  - 2captcha service for CAPTCHA solving

---

## 📊 Analysis of `apify-crawler-lattes`

### Purpose
Downloads Lattes CVs (XML files) from the CNPq Lattes platform by researcher names.

### Key Features

1. **Researcher Search**: Searches for researchers by name on CNPq Lattes platform
2. **CV Download**: Downloads Lattes CV as ZIP files containing XML data
3. **CAPTCHA Solving**: Uses 2captcha service to solve reCAPTCHA challenges
4. **Batch Processing**: Can process multiple researchers in a single run
5. **Storage**: Saves downloaded CVs to Apify Key-Value Store

### Technical Implementation

#### Main Components (`main.js`)

```javascript
// Key functions:
- procurarPesquisador()      // Search for researcher by name
- getAbrirCurriculoPage()    // Open CV page
- getBaixarCurriculoPage()   // Navigate to download page
- extractLattesId()          // Extract Lattes ID from URL
- saveFileIntoStore()        // Save ZIP file to storage
```

#### Input Schema (`input-schema.json`)
```json
{
  "nomeDosPesquisadores": ["Researcher Name 1", "Researcher Name 2", ...]
}
```

#### Dependencies (`package.json`)
- `apify`: ^3.0.0
- `crawlee`: ^3.1.4
- `puppeteer`: ^19.6.2
- `puppeteer-extra`: ^3.3.4
- `puppeteer-extra-plugin-recaptcha`: ^3.6.6

### Workflow

1. **Input**: List of researcher names
2. **Search**: Navigate to CNPq Lattes search page
3. **Select**: Click on first search result
4. **Open CV**: Click "Abrir Currículo" button
5. **Download**: Navigate to download page
6. **Solve CAPTCHA**: Use 2captcha to solve reCAPTCHA
7. **Download**: Download CV as ZIP file
8. **Store**: Save to Apify Key-Value Store

---

## 🎯 What This Means for Your Application

### For People Enrichment Page

#### ✅ What We Can Use

1. **Lattes CV Data Source**:
   - Can integrate similar crawler logic to fetch Lattes CV data
   - Extract researcher information from Lattes platform
   - Parse XML data from downloaded CVs

2. **CAPTCHA Handling Pattern**:
   - Use 2captcha or similar service for automated CAPTCHA solving
   - Pattern for handling protected web scraping

3. **Researcher Search Pattern**:
   - How to search CNPq Lattes platform programmatically
   - Extract Lattes IDs from URLs
   - Handle researcher name variations

#### ⚠️ Considerations

1. **Legal/Ethical**:
   - Crawler uses CAPTCHA solving (may violate terms of service)
   - Should check CNPq Lattes terms of use
   - Consider using official APIs if available

2. **Technical**:
   - Requires Puppeteer/headless browser
   - Requires 2captcha API key (paid service)
   - Slower than API-based solutions
   - May break if CNPq changes their website structure

3. **Alternative Approaches**:
   - Check if CNPq Lattes has official API
   - Use web scraping libraries (requests + BeautifulSoup) if possible
   - Consider using Apify actors if available

---

## 🔧 Integration Recommendations

### Option 1: Direct Integration (Not Recommended)
- Copy crawler logic from `apify-crawler-lattes`
- Integrate into FastAPI backend
- Requires Puppeteer setup
- Requires 2captcha API key
- **Risk**: May violate terms of service

### Option 2: Apify Actor Integration (Recommended)
- Use Apify actor if available
- Call Apify API from backend
- Handle CAPTCHA solving via Apify
- **Benefit**: Separates concerns, uses existing infrastructure

### Option 3: Official API (Best, if available)
- Check CNPq Lattes for official API
- Use REST/GraphQL endpoints
- No CAPTCHA solving needed
- **Benefit**: Legal, fast, reliable

### Option 4: Manual/User-Initiated (Safest)
- Allow users to provide Lattes ID manually
- Fetch public data using Lattes ID
- Parse XML data from public URLs
- **Benefit**: No scraping, fully legal

---

## 📋 Implementation Plan for People Enrichment

### Phase 1: Basic Lattes Integration

1. **Add Lattes ID Field** to Person model:
   ```python
   lattes_id = Column(String(50), index=True)
   ```

2. **Create Lattes Service** (`services/third_party/lattes.py`):
   ```python
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

3. **Backend Endpoint**:
   ```python
   POST /api/v1/people/enrich-by-lattes
   {
     "lattes_id": "1234567890123456"
   }
   ```

4. **Frontend Component**:
   - Add Lattes ID input field
   - Display academic profile section
   - Show publications list
   - Display research areas

### Phase 2: Enhanced Integration (If Needed)

1. **Integrate Apify Actor** (if using Option 2):
   - Create Apify client service
   - Call Apify actor for CV download
   - Parse downloaded XML files
   - Store parsed data

2. **Add Researcher Search**:
   - Search by name functionality
   - Display search results
   - Allow user to select researcher

---

## 🚀 Next Steps

1. **Verify Repository Name**:
   - Confirm with Dadosfera team if `dev-demo-lattes` exists under different name
   - Check if it's in a different organization

2. **Check CNPq Lattes API**:
   - Research official API availability
   - Check documentation for public endpoints
   - Verify terms of service

3. **Decide Integration Approach**:
   - Choose between Options 1-4 above
   - Consider legal and technical implications
   - Plan implementation accordingly

4. **Start Implementation**:
   - Begin with Option 4 (manual Lattes ID input)
   - Add Lattes ID field to Person model
   - Create basic Lattes service
   - Build frontend components

---

## 📚 References

- **apify-crawler-lattes**: https://github.com/dadosfera/apify-crawler-lattes
- **CNPq Lattes Platform**: https://lattes.cnpq.br/
- **Apify SDK**: https://sdk.apify.com/
- **Puppeteer**: https://pptr.dev/
- **2captcha**: https://2captcha.com/

---

## ✅ Summary

- **`dev-demo-lattes`**: Does not exist
- **`apify-crawler-lattes`**: Found and accessible
- **Recommendation**: Start with manual Lattes ID input, then explore official API options
- **Next Action**: Verify repository name with Dadosfera team or proceed with `apify-crawler-lattes` patterns

---

**Status**: ✅ **Investigation Complete**
**Action**: Proceed with People enrichment implementation using findings above
