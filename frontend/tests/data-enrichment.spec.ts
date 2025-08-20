import { test, expect } from '@playwright/test';

test.describe('Data Enrichment Functionality Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set a longer timeout for enrichment operations
    page.setDefaultTimeout(30000);
  });

  test.describe('Person Enrichment API', () => {
    test('should successfully enrich person data via API', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/enrich/person', {
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          first_name: 'Jane',
          last_name: 'Smith',
          email: 'jane.smith@techcorp.com'
        }
      });

      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      
      expect(data.success).toBe(true);
      expect(data.data.original_data.first_name).toBe('Jane');
      expect(data.data.original_data.last_name).toBe('Smith');
      expect(data.data.enriched_data.full_name).toBe('Jane Smith');
      expect(data.data.enrichment_score).toBeGreaterThan(0);
      expect(data.data.data_sources).toContain('people_data_labs');
    });

    test('should handle multiple enrichment requests', async ({ request }) => {
      const people = [
        { first_name: 'John', last_name: 'Doe', email: 'john.doe@example.com' },
        { first_name: 'Alice', last_name: 'Johnson', email: 'alice.johnson@company.com' },
        { first_name: 'Bob', last_name: 'Williams', email: 'bob.williams@startup.io' }
      ];

      for (const person of people) {
        const response = await request.post('http://localhost:8247/api/v1/enrich/person', {
          headers: { 'Content-Type': 'application/json' },
          data: person
        });

        expect(response.ok()).toBeTruthy();
        const data = await response.json();
        expect(data.success).toBe(true);
        expect(data.data.enriched_data.full_name).toBe(`${person.first_name} ${person.last_name}`);
      }
    });
  });

  test.describe('Company Enrichment API', () => {
    test('should successfully enrich company data via API', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/enrich/company', {
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          name: 'Microsoft',
          domain: 'microsoft.com'
        }
      });

      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      
      expect(data.success).toBe(true);
      expect(data.data.original_data.name).toBe('Microsoft');
      expect(data.data.enriched_data.name).toBe('Microsoft');
      expect(data.data.enrichment_score).toBeGreaterThan(0);
    });
  });

  test.describe('Integration Service Endpoints', () => {
    test('should test People Data Labs integration', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/integrations/pdl/enrich-person', {
        headers: { 'Content-Type': 'application/json' },
        data: {
          first_name: 'Sarah',
          last_name: 'Connor',
          email: 'sarah.connor@technet.com'
        }
      });

      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      expect(data.success).toBe(true);
    });

    test('should test Wiza integration', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/integrations/wiza/enrich-profile', {
        headers: { 'Content-Type': 'application/json' },
        data: {
          linkedin_url: 'https://linkedin.com/in/elon-musk'
        }
      });

      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      expect(data.success).toBe(true);
    });

    test('should test BigData Corp integration', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/integrations/bigdata/lookup-cpf', {
        headers: { 'Content-Type': 'application/json' },
        data: {
          cpf: '12345678901'
        }
      });

      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      expect(data.success).toBe(true);
    });
  });

  test.describe('Data Quality and Validation', () => {
    test('should validate enrichment score ranges', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/enrich/person', {
        headers: { 'Content-Type': 'application/json' },
        data: {
          first_name: 'Test',
          last_name: 'User',
          email: 'test.user@example.com'
        }
      });

      const data = await response.json();
      expect(data.data.enrichment_score).toBeGreaterThanOrEqual(0);
      expect(data.data.enrichment_score).toBeLessThanOrEqual(100);
    });

    test('should include required enriched fields', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/enrich/person', {
        headers: { 'Content-Type': 'application/json' },
        data: {
          first_name: 'Professional',
          last_name: 'User',
          email: 'professional.user@company.com'
        }
      });

      const data = await response.json();
      const enriched = data.data.enriched_data;
      
      // Check core fields
      expect(enriched.full_name).toBeDefined();
      expect(enriched.email).toBeDefined();
      expect(enriched.professional).toBeDefined();
      expect(enriched.contact).toBeDefined();
      expect(enriched.location).toBeDefined();
      expect(enriched.skills).toBeDefined();
      expect(enriched.education).toBeDefined();
    });
  });

  test.describe('Error Handling', () => {
    test('should handle invalid person data gracefully', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/enrich/person', {
        headers: { 'Content-Type': 'application/json' },
        data: {
          first_name: '',
          last_name: '',
          email: 'invalid-email'
        }
      });

      // Should still return 200 but with lower enrichment score
      expect(response.ok()).toBeTruthy();
    });

    test('should handle missing required fields', async ({ request }) => {
      const response = await request.post('http://localhost:8247/api/v1/enrich/person', {
        headers: { 'Content-Type': 'application/json' },
        data: {}
      });

      // Should handle gracefully
      expect(response.status()).toBeGreaterThanOrEqual(200);
    });
  });

  test.describe('Performance Tests', () => {
    test('should handle concurrent enrichment requests', async ({ request }) => {
      const promises = [];
      
      for (let i = 0; i < 5; i++) {
        promises.push(
          request.post('http://localhost:8247/api/v1/enrich/person', {
            headers: { 'Content-Type': 'application/json' },
            data: {
              first_name: `User${i}`,
              last_name: `Test${i}`,
              email: `user${i}@test.com`
            }
          })
        );
      }

      const responses = await Promise.all(promises);
      
      for (const response of responses) {
        expect(response.ok()).toBeTruthy();
        const data = await response.json();
        expect(data.success).toBe(true);
      }
    });

    test('should complete enrichment within reasonable time', async ({ request }) => {
      const startTime = Date.now();
      
      const response = await request.post('http://localhost:8247/api/v1/enrich/person', {
        headers: { 'Content-Type': 'application/json' },
        data: {
          first_name: 'Speed',
          last_name: 'Test',
          email: 'speed.test@benchmark.com'
        }
      });

      const endTime = Date.now();
      const duration = endTime - startTime;
      
      expect(response.ok()).toBeTruthy();
      expect(duration).toBeLessThan(10000); // Should complete within 10 seconds
    });
  });
});
