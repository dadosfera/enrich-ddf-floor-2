# repository-investigation-enrichment-pages – next actions

**Status**: backlog
**Created from**: Conversation review on 2025-01-27
**Objective**: Investigate repositories and plan implementation of Cars, Real Estate, and People enrichment pages
**Priority**: Medium
**Estimated effort**: 2 AI hours / 40 Human hours

## Next actions (not-yet-tried / unplanned)

### High Priority

- [ ] Verify repository name with Dadosfera team - Confirm if `dev-demo-lattes` exists under different name or organization
- [ ] Research CNPq Lattes official API - Check for official API availability before implementing scraping solution
- [ ] Extract and adapt validators from `dataapp-enriquecimento` - Adapt CPF/email/phone/LinkedIn validators for FastAPI backend

### Medium Priority

- [ ] Research ZeroBounce API integration - Review API documentation and create service integration pattern
- [ ] Research VIN decoding APIs - Evaluate NHTSA VIN Decoder API and Brazilian vehicle databases (Renavam, Detran)
- [ ] Research property valuation APIs - Evaluate Zillow API, Brazilian equivalents, and Google Maps API for geographic data
- [ ] Evaluate Apify actor availability - Check if Apify actor exists for Lattes CV integration (Option 2)

### Low Priority

- [ ] Research Brazilian data sources - Investigate Renavam, Detran, Cartório APIs for Cars/Real Estate enrichment
- [ ] Plan Phase 1 implementation - Detailed task breakdown for People Page Enhancement (Week 1-2)
- [ ] Plan Phase 2 implementation - Detailed task breakdown for Cars Page (Week 3-4)
- [ ] Plan Phase 3 implementation - Detailed task breakdown for Real Estate Page (Week 5-6)

## Context from conversation

### Investigation Results

- **Target Repository**: `dadosfera/dev-demo-lattes` does not exist (404 Not Found)
- **Found Repositories**:
  - `apify-crawler-lattes`: Lattes CV crawler using Puppeteer + 2captcha
  - `dataapp-enriquecimento`: People enrichment app with reusable validators

### Key Decisions

- **Lattes Integration**: Start with Option 4 (Manual/User-Initiated Lattes ID input) - safest and legal approach
- **Implementation Pattern**: Follow existing patterns from Companies.tsx and Contacts.tsx
- **Implementation Phases**: 3-phase approach (People → Cars → Real Estate) over 6 weeks

### Constraints

- No web scraping initially (legal/ethical concerns)
- Must reuse existing enrichment services where possible
- Follow existing FastAPI + React + Material-UI architecture

### Reusable Components Identified

- CPF validation logic from `dataapp-enriquecimento`
- Email validation (ZeroBounce pattern)
- LinkedIn enrichment (People Data Labs)
- Data type auto-detection pattern
- Validation functions for Brazilian data

## Links

- **Active Plan**: `docs/plans/active/76_cars_real_estate_people_enrichment_pages_plan.md`
- **Related Repositories**:
  - `apify-crawler-lattes`: https://github.com/dadosfera/apify-crawler-lattes
  - `dataapp-enriquecimento`: https://github.com/dadosfera/dataapp-enriquecimento
- **CNPq Lattes Platform**: https://lattes.cnpq.br/

## Notes

- Investigation phase is complete; comprehensive plan document exists
- Implementation not yet started - ready to begin Phase 1 (People Page Enhancement)
- All technical specifications, data models, and API endpoints are documented in the active plan
