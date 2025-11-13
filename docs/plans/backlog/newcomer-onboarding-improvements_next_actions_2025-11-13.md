# newcomer-onboarding-improvements – next actions

**Status**: backlog  
**Created from**: Conversation review on 2025-11-13  
**Objective**: Continue improving newcomer onboarding experience  
**Priority**: Low  
**Estimated effort**: 2-4 AI hours / 1-2 Human hours (review)

## Next actions (not-yet-tried / unplanned)

### Documentation Improvements
- [ ] Add video walkthrough or GIF showing application startup
- [ ] Create troubleshooting FAQ for common setup issues
- [ ] Add code examples for common use cases (API usage, enrichment flows)
- [ ] Document API authentication and rate limiting (when implemented)

### Developer Experience
- [ ] Add VS Code workspace settings for consistent development environment
- [ ] Create development container (devcontainer.json) for one-click setup
- [ ] Add example .env file with working demo API keys (non-production)
- [ ] Create quick-start script that checks prerequisites and sets up environment

### Testing & Validation
- [ ] Add smoke test script to validate installation (`make verify-install`)
- [ ] Create health check dashboard showing all service statuses
- [ ] Add automated documentation validation in CI/CD

### Frontend Enhancements
- [ ] Add welcome tour for first-time users (product tour library)
- [ ] Create interactive API documentation with try-it-out features
- [ ] Add keyboard shortcuts guide and help overlay

## Context from conversation

### What was completed
- ✅ Comprehensive documentation suite created (GETTING_STARTED, ARCHITECTURE, etc.)
- ✅ Application startup working (backend + frontend)
- ✅ Console logging improved with user-friendly URLs
- ✅ Configuration made flexible (no hardcoded values)
- ✅ README restructured with better navigation

### Key decisions
- Documentation follows progressive disclosure pattern (start with getting started, then dive deeper)
- Configuration uses environment variables for all host/port settings
- Console output shows both backend and frontend URLs clearly
- Separate repos (enrich-ddf-floor-2 vs enrich-ddf-mod-ncm) serve different purposes

### Constraints
- Must maintain Floor 2 architecture standards (scalable frameworks, no Streamlit)
- Frontend is React + TypeScript + Material-UI (modern, not simplified)
- Configuration must remain flexible via environment variables

### Lessons learned
- Always verify current state before assuming work is needed
- Ask clarifying questions when requirements are ambiguous
- Check git history to understand previous work
- The existing UI was already complete and production-ready

## Links

**Related documentation**:
- docs/GETTING_STARTED.md - Main entry point for newcomers
- docs/ARCHITECTURE.md - System design details
- docs/PROJECT_STRUCTURE.md - Directory layout explanation
- docs/CONTRIBUTING.md - Developer guidelines

**Related plans**:
- docs/plans/active/76_cars_real_estate_people_enrichment_pages_plan.md - Future enrichment features

**Conversation archive**:
- docs/conversations/2025-11-13_newcomer-onboarding-improvements.md

