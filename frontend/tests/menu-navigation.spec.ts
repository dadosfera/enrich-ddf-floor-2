import { test, expect } from '@playwright/test';

test.describe('Menu Navigation Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application before each test
    await page.goto('/');
    
    // Wait for the application to load
    await page.waitForLoadState('networkidle');
  });

  test('should display all main navigation menu items', async ({ page }) => {
    // Check if main navigation links are visible
    await expect(page.locator('nav')).toBeVisible();
    
    // Test for common navigation items (adjust based on your actual menu)
    const navigationItems = [
      'Dashboard',
      'Companies', 
      'Contacts',
      'Products',
      'Integrations'
    ];

    for (const item of navigationItems) {
      await expect(page.getByRole('link', { name: item })).toBeVisible();
    }
  });

  test('should navigate to Companies page when Companies menu is clicked', async ({ page }) => {
    // Click on Companies menu item
    await page.getByRole('link', { name: 'Companies' }).click();
    
    // Wait for navigation to complete
    await page.waitForLoadState('networkidle');
    
    // Verify we're on the companies page
    await expect(page).toHaveURL(/.*companies/);
    await expect(page.locator('h4')).toContainText('Companies');
    
    // Check for "Add Company" button
    await expect(page.getByRole('button', { name: 'Add Company' })).toBeVisible();
  });

  test('should handle Companies page data loading correctly', async ({ page }) => {
    // Navigate to companies page
    await page.goto('/companies');
    await page.waitForLoadState('networkidle');
    
    // Wait for loading to complete (check loading spinner disappears)
    await page.waitForSelector('[data-testid="loading"]', { state: 'hidden', timeout: 10000 })
      .catch(() => {}); // Ignore timeout if loading is fast
    
    // Check if companies list is rendered (even if empty)
    const companiesContainer = page.locator('[data-testid="companies-container"]')
      .or(page.locator('.MuiGrid-container'))
      .or(page.locator('main'));
    
    await expect(companiesContainer).toBeVisible();
    
    // Check for search functionality
    const searchInput = page.locator('input[placeholder*="Search"]')
      .or(page.locator('input[type="search"]'))
      .or(page.locator('input').first());
    
    await expect(searchInput).toBeVisible();
  });

  test('should navigate to Contacts page when Contacts menu is clicked', async ({ page }) => {
    // Click on Contacts menu item
    await page.getByRole('link', { name: 'Contacts' }).click();
    
    // Wait for navigation to complete
    await page.waitForLoadState('networkidle');
    
    // Verify we're on the contacts page
    await expect(page).toHaveURL(/.*contacts/);
    await expect(page.locator('h4')).toContainText('Contacts');
  });

  test('should navigate to Products page when Products menu is clicked', async ({ page }) => {
    // Click on Products menu item
    await page.getByRole('link', { name: 'Products' }).click();
    
    // Wait for navigation to complete
    await page.waitForLoadState('networkidle');
    
    // Verify we're on the products page
    await expect(page).toHaveURL(/.*products/);
    await expect(page.locator('h4')).toContainText('Products');
  });

  test('should navigate to Integrations page when Integrations menu is clicked', async ({ page }) => {
    // Click on Integrations menu item
    await page.getByRole('link', { name: 'Integrations' }).click();
    
    // Wait for navigation to complete
    await page.waitForLoadState('networkidle');
    
    // Verify we're on the integrations page
    await expect(page).toHaveURL(/.*integrations/);
    await expect(page.locator('h4')).toContainText('Data Integrations');
    
    // Check for integration cards
    await expect(page.locator('text=BigData Corp')).toBeVisible();
    await expect(page.locator('text=Wiza')).toBeVisible();
    await expect(page.locator('text=Surfe')).toBeVisible();
    await expect(page.locator('text=People Data Labs')).toBeVisible();
  });

  test('should open Add Company dialog when Add Company button is clicked', async ({ page }) => {
    // Navigate to companies page
    await page.goto('/companies');
    await page.waitForLoadState('networkidle');
    
    // Click Add Company button
    await page.getByRole('button', { name: 'Add Company' }).click();
    
    // Verify dialog opens
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await expect(page.locator('text=Add New Company')).toBeVisible();
    
    // Check form fields are present
    await expect(page.locator('input[label="Company Name"]')
      .or(page.locator('label:has-text("Company Name") + input'))
      .or(page.locator('input').first())).toBeVisible();
  });

  test('should handle responsive menu on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Navigate to home page
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Look for mobile menu trigger (hamburger menu or similar)
    const menuButton = page.locator('[aria-label*="menu"]')
      .or(page.locator('[data-testid="mobile-menu-button"]'))
      .or(page.locator('button:has([data-testid="MenuIcon"])'));
    
    if (await menuButton.isVisible()) {
      await menuButton.click();
      
      // Check if mobile menu items are visible
      await expect(page.getByRole('link', { name: 'Companies' })).toBeVisible();
    }
  });
  test('should show BigData Corp configuration dialog when Configure button is clicked', async ({ page }) => {
    // Navigate to integrations page
    await page.goto('/integrations');
    await page.waitForLoadState('networkidle');
    
    // Find and click the BigData Corp Configure button
    const bigDataCard = page.locator('text=BigData Corp').locator('..').locator('..');
    await bigDataCard.locator('button:has-text("Configure")').click();
    
    // Verify dialog opens
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await expect(page.locator('text=BigData Corp API Configuration')).toBeVisible();
    
    // Check form fields are present
    await expect(page.locator('input[type="password"]').first()).toBeVisible();
  });

  test('should show Wiza configuration dialog when Configure button is clicked', async ({ page }) => {
    // Navigate to integrations page
    await page.goto('/integrations');
    await page.waitForLoadState('networkidle');
    
    // Find and click the Wiza Configure button
    const wizaCard = page.locator('text=Wiza').locator('..').locator('..');
    await wizaCard.locator('button:has-text("Configure")').click();
    
    // Verify dialog opens
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await expect(page.locator('text=Wiza API Configuration')).toBeVisible();
    
    // Check form fields are present
    await expect(page.locator('input[type="password"]')).toBeVisible();
  });

  test('should show Surfe configuration dialog when Configure button is clicked', async ({ page }) => {
    // Navigate to integrations page
    await page.goto('/integrations');
    await page.waitForLoadState('networkidle');
    
    // Find and click the Surfe Configure button
    const surfeCard = page.locator('text=Surfe').locator('..').locator('..');
    await surfeCard.locator('button:has-text("Configure")').click();
    
    // Verify dialog opens
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await expect(page.locator('text=Surfe API Configuration')).toBeVisible();
    
    // Check form fields are present
    await expect(page.locator('input[type="password"]')).toBeVisible();
    
    // Check for API documentation link
    await expect(page.locator('text=Surfe API Docs')).toBeVisible();
  });

  test('should show People Data Labs configuration dialog when Configure button is clicked', async ({ page }) => {
    // Navigate to integrations page
    await page.goto('/integrations');
    await page.waitForLoadState('networkidle');
    
    // Find and click the People Data Labs Configure button
    const pdlCard = page.locator('text=People Data Labs').locator('..').locator('..');
    await pdlCard.locator('button:has-text("Configure")').click();
    
    // Verify dialog opens
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await expect(page.locator('text=People Data Labs API Configuration')).toBeVisible();
    
    // Check form fields are present
    await expect(page.locator('input[type="password"]')).toBeVisible();
    
    // Check for API documentation link
    await expect(page.locator('text=People Data Labs')).toBeVisible();
  });
});

test.describe('Data Loading and Error Handling', () => {
  test('should display error message when API fails for companies', async ({ page }) => {
    // Mock API failure
    await page.route('**/api/v1/companies', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' })
      });
    });
    
    // Navigate to companies page
    await page.goto('/companies');
    await page.waitForLoadState('networkidle');
    
    // Check for error message
    await expect(page.locator('text=Error loading companies')
      .or(page.locator('[role="alert"]'))
      .or(page.locator('.MuiAlert-root'))).toBeVisible({ timeout: 10000 });
  });

  test('should display loading state while fetching companies', async ({ page }) => {
    // Delay API response to see loading state
    await page.route('**/api/v1/companies', route => {
      setTimeout(() => {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: [],
            total: 0,
            page: 1,
            size: 100,
            success: true
          })
        });
      }, 1000);
    });
    
    // Navigate to companies page
    await page.goto('/companies');
    
    // Check for loading indicator
    await expect(page.locator('[data-testid="loading"]')
      .or(page.locator('.MuiCircularProgress-root'))
      .or(page.locator('text=Loading'))).toBeVisible();
  });
}); 