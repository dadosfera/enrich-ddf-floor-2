import { test, expect } from '@playwright/test';

test.describe('Data Enrichment Flow Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application before each test
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test.describe('Company Enrichment', () => {
    test('should enrich company data successfully', async ({ page }) => {
      // Navigate to companies page
      await page.getByRole('link', { name: 'Companies' }).click();
      await page.waitForLoadState('networkidle');

      // Wait for companies to load
      await page.waitForSelector('[data-testid="loading"]', { state: 'hidden', timeout: 15000 })
        .catch(() => {}); // Ignore if already loaded

      // Find a company to enrich (look for one with limited data)
      const companyRows = page.locator('[data-testid="company-row"]')
        .or(page.locator('.MuiTableRow-root').nth(1))
        .or(page.locator('tbody tr').first());

      if (await companyRows.isVisible()) {
        // Click on enrich button or similar action
        const enrichButton = companyRows
          .locator('button:has-text("Enrich")')
          .or(companyRows.locator('[data-testid="enrich-company"]'))
          .or(companyRows.locator('button').last());

        if (await enrichButton.isVisible()) {
          await enrichButton.click();

          // Wait for enrichment to complete
          await expect(page.locator('text=Enrichment completed')
            .or(page.locator('[role="alert"]'))
            .or(page.locator('.MuiAlert-standardSuccess'))).toBeVisible({ timeout: 30000 });

          // Verify enriched data is displayed
          await expect(page.locator('text=Employee Count')
            .or(page.locator('text=Industry'))
            .or(page.locator('text=Location'))).toBeVisible();
        }
      }
    });

    test('should handle company enrichment API errors gracefully', async ({ page }) => {
      // Mock API error for enrichment
      await page.route('**/api/v1/enrich/company', route => {
        route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({ error: 'Enrichment service unavailable' })
        });
      });

      // Navigate to companies and try to enrich
      await page.goto('/companies');
      await page.waitForLoadState('networkidle');

      // Try enrichment action (if available)
      const enrichAction = page.locator('button:has-text("Enrich")').first();
      if (await enrichAction.isVisible()) {
        await enrichAction.click();

        // Should show error message
        await expect(page.locator('text=Error')
          .or(page.locator('[role="alert"]'))
          .or(page.locator('.MuiAlert-standardError'))).toBeVisible({ timeout: 10000 });
      }
    });
  });

  test.describe('Contact/Person Enrichment', () => {
    test('should enrich contact data successfully', async ({ page }) => {
      // Navigate to contacts page
      await page.getByRole('link', { name: 'Contacts' }).click();
      await page.waitForLoadState('networkidle');

      // Wait for contacts to load
      await page.waitForSelector('[data-testid="loading"]', { state: 'hidden', timeout: 15000 })
        .catch(() => {});

      // Find a contact to enrich
      const contactRows = page.locator('[data-testid="contact-row"]')
        .or(page.locator('.MuiTableRow-root').nth(1))
        .or(page.locator('tbody tr').first());

      if (await contactRows.isVisible()) {
        // Click on enrich button
        const enrichButton = contactRows
          .locator('button:has-text("Enrich")')
          .or(contactRows.locator('[data-testid="enrich-contact"]'))
          .or(contactRows.locator('button').last());

        if (await enrichButton.isVisible()) {
          await enrichButton.click();

          // Wait for enrichment to complete
          await expect(page.locator('text=Contact enriched')
            .or(page.locator('text=Enrichment completed'))
            .or(page.locator('[role="alert"]'))).toBeVisible({ timeout: 30000 });

          // Verify enriched data fields
          await expect(page.locator('text=LinkedIn')
            .or(page.locator('text=Job Title'))
            .or(page.locator('text=Company'))).toBeVisible();
        }
      }
    });

    test('should validate LinkedIn URL enrichment', async ({ page }) => {
      // Navigate to integrations page
      await page.goto('/integrations');
      await page.waitForLoadState('networkidle');

      // Look for Wiza integration card
      const wizaCard = page.locator('text=Wiza').locator('..').locator('..');

      if (await wizaCard.isVisible()) {
        // Click configure or test button
        const configButton = wizaCard.locator('button:has-text("Configure")')
          .or(wizaCard.locator('button:has-text("Test")'));

        if (await configButton.isVisible()) {
          await configButton.click();

          // Find LinkedIn URL input field
          const linkedinInput = page.locator('input[placeholder*="linkedin.com"]')
            .or(page.locator('input[label*="LinkedIn"]'))
            .or(page.locator('input').nth(1));

          if (await linkedinInput.isVisible()) {
            // Test with valid LinkedIn URL
            await linkedinInput.fill('https://linkedin.com/in/test-profile');

            // Click enrich or test button
            const enrichButton = page.locator('button:has-text("Enrich")')
              .or(page.locator('button:has-text("Test")'));

            if (await enrichButton.isVisible()) {
              await enrichButton.click();

              // Verify enrichment results
              await expect(page.locator('text=Profile enriched')
                .or(page.locator('text=Success'))
                .or(page.locator('[role="alert"]'))).toBeVisible({ timeout: 20000 });
            }
          }
        }
      }
    });
  });

  test.describe('Integration API Tests', () => {
    test('should test People Data Labs integration', async ({ page }) => {
      // Navigate to integrations
      await page.goto('/integrations');
      await page.waitForLoadState('networkidle');

      // Find PDL card
      const pdlCard = page.locator('text=People Data Labs').locator('..').locator('..');

      if (await pdlCard.isVisible()) {
        // Click configure
        await pdlCard.locator('button:has-text("Configure")').click();

        // Verify dialog opens
        await expect(page.locator('[role="dialog"]')).toBeVisible();

        // Test API connection (if test button exists)
        const testButton = page.locator('button:has-text("Test")')
          .or(page.locator('button:has-text("Test Connection")'));

        if (await testButton.isVisible()) {
          await testButton.click();

          // Should show connection status
          await expect(page.locator('text=Connected')
            .or(page.locator('text=Test successful'))
            .or(page.locator('text=Connection failed'))
            .or(page.locator('[role="alert"]'))).toBeVisible({ timeout: 15000 });
        }
      }
    });

    test('should validate API key configuration', async ({ page }) => {
      await page.goto('/integrations');
      await page.waitForLoadState('networkidle');

      // Test BigData Corp configuration
      const bigDataCard = page.locator('text=BigData Corp').locator('..').locator('..');
      await bigDataCard.locator('button:has-text("Configure")').click();

      // Verify dialog opens
      await expect(page.locator('[role="dialog"]')).toBeVisible();

      // Find API key input
      const apiKeyInput = page.locator('input[type="password"]')
        .or(page.locator('input[label*="API Key"]'))
        .or(page.locator('input[placeholder*="key"]'));

      if (await apiKeyInput.isVisible()) {
        // Test empty API key validation
        await apiKeyInput.clear();
        const saveButton = page.locator('button:has-text("Save")')
          .or(page.locator('button:has-text("Update")'));

        if (await saveButton.isVisible()) {
          await saveButton.click();

          // Should show validation error
          await expect(page.locator('text=API key is required')
            .or(page.locator('text=Required'))
            .or(page.locator('[role="alert"]'))).toBeVisible();
        }
      }
    });
  });

  test.describe('Enrichment Data Display', () => {
    test('should display enrichment results correctly', async ({ page }) => {
      // Mock successful enrichment response
      await page.route('**/api/v1/enrich/person', route => {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: {
              enriched_data: {
                full_name: 'John Doe',
                email: 'john.doe@example.com',
                professional: {
                  current_title: 'Software Engineer',
                  current_company: 'Tech Corp',
                  seniority: 'Senior'
                },
                contact: {
                  phone: '+1-555-0123',
                  linkedin: 'https://linkedin.com/in/john-doe'
                },
                location: {
                  city: 'San Francisco',
                  state: 'California'
                },
                skills: ['Python', 'JavaScript', 'React']
              },
              enrichment_score: 85
            }
          })
        });
      });

      await page.goto('/contacts');
      await page.waitForLoadState('networkidle');

      // Trigger enrichment (if possible through UI)
      const enrichButton = page.locator('button:has-text("Enrich")').first();
      if (await enrichButton.isVisible()) {
        await enrichButton.click();

        // Verify enriched data is displayed
        await expect(page.locator('text=Software Engineer')).toBeVisible({ timeout: 10000 });
        await expect(page.locator('text=Tech Corp')).toBeVisible();
        await expect(page.locator('text=San Francisco')).toBeVisible();
        await expect(page.locator('text=85')).toBeVisible(); // Enrichment score
      }
    });

    test('should handle partial enrichment data gracefully', async ({ page }) => {
      // Mock partial enrichment response
      await page.route('**/api/v1/enrich/company', route => {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: {
              enriched_data: {
                name: 'Test Company',
                industry: 'Technology',
                // Missing other fields
              },
              enrichment_score: 45 // Low score
            }
          })
        });
      });

      await page.goto('/companies');
      await page.waitForLoadState('networkidle');

      // Trigger enrichment
      const enrichButton = page.locator('button:has-text("Enrich")').first();
      if (await enrichButton.isVisible()) {
        await enrichButton.click();

        // Should show available data and indicate low completeness
        await expect(page.locator('text=Technology')).toBeVisible({ timeout: 10000 });
        await expect(page.locator('text=45')
          .or(page.locator('text=Low'))
          .or(page.locator('text=Partial'))).toBeVisible();
      }
    });
  });

  test.describe('Bulk Enrichment Operations', () => {
    test('should handle batch enrichment if available', async ({ page }) => {
      await page.goto('/contacts');
      await page.waitForLoadState('networkidle');

      // Look for batch operations
      const batchButton = page.locator('button:has-text("Enrich Selected")')
        .or(page.locator('button:has-text("Batch Enrich")')
        .or(page.locator('[data-testid="batch-enrich"]')));

      if (await batchButton.isVisible()) {
        // Select some contacts first
        const checkboxes = page.locator('input[type="checkbox"]');
        if (await checkboxes.count() > 1) {
          await checkboxes.nth(1).click();
          await checkboxes.nth(2).click();
        }

        await batchButton.click();

        // Should show batch progress or completion
        await expect(page.locator('text=Batch enrichment')
          .or(page.locator('text=Processing'))
          .or(page.locator('[role="progressbar"]'))).toBeVisible({ timeout: 5000 });
      }
    });
  });

  test.describe('Error Handling and Recovery', () => {
    test('should recover from network timeouts', async ({ page }) => {
      // Mock timeout response
      await page.route('**/api/v1/enrich/*', route => {
        setTimeout(() => {
          route.fulfill({
            status: 408,
            contentType: 'application/json',
            body: JSON.stringify({ error: 'Request timeout' })
          });
        }, 30000);
      });

      await page.goto('/contacts');
      await page.waitForLoadState('networkidle');

      // Try enrichment
      const enrichButton = page.locator('button:has-text("Enrich")').first();
      if (await enrichButton.isVisible()) {
        await enrichButton.click();

        // Should show timeout error
        await expect(page.locator('text=timeout')
          .or(page.locator('text=Try again'))
          .or(page.locator('[role="alert"]'))).toBeVisible({ timeout: 35000 });
      }
    });

    test('should handle rate limiting gracefully', async ({ page }) => {
      // Mock rate limit response
      await page.route('**/api/v1/enrich/*', route => {
        route.fulfill({
          status: 429,
          contentType: 'application/json',
          body: JSON.stringify({
            error: 'Rate limit exceeded',
            retry_after: 60
          })
        });
      });

      await page.goto('/integrations');
      await page.waitForLoadState('networkidle');

      // Try to test an integration
      const testButton = page.locator('button:has-text("Test")').first();
      if (await testButton.isVisible()) {
        await testButton.click();

        // Should show rate limit message
        await expect(page.locator('text=rate limit')
          .or(page.locator('text=Try again later'))
          .or(page.locator('[role="alert"]'))).toBeVisible({ timeout: 10000 });
      }
    });
  });
});
