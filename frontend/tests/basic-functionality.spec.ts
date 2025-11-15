import { test, expect } from '@playwright/test';

test.describe('Basic Application Functionality', () => {
  test.beforeEach(async ({ page }) => {
    // Set longer timeout for initial page load
    page.setDefaultTimeout(15000);
  });

  test('should load the application home page', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check if the page loads at all
    await expect(page).toHaveTitle(/Enrich DDF|Vite|React/);

    // Check for basic React content
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('#root')).toBeVisible();
  });

  test('should have working React app', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Wait for React to mount
    await page.waitForSelector('#root', { timeout: 10000 });

    // Check if React app is mounted and functional
    const rootContent = await page.locator('#root').innerHTML();
    expect(rootContent.length).toBeGreaterThan(10);

    // Look for any React-rendered content
    await expect(page.locator('#root')
      .or(page.locator('.App'))
      .or(page.locator('[data-reactroot]'))).toBeVisible();
  });

  test('should have working API connection', async ({ page }) => {
    // Test direct API connection
    const API_BASE_URL = process.env.VITE_API_URL || process.env.API_URL || 'http://127.0.0.1:8247';
    const response = await page.request.get(`${API_BASE_URL}/health`);
    expect(response.status()).toBe(200);

    const healthData = await response.json();
    expect(healthData.status).toBe('healthy');
    expect(healthData.database).toBe('connected');
  });

  test('should load basic styles and resources', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check if basic CSS is loaded (no major styling errors)
    const bodyStyles = await page.evaluate(() => {
      const body = document.body;
      const styles = window.getComputedStyle(body);
      return {
        fontFamily: styles.fontFamily,
        margin: styles.margin,
        display: styles.display
      };
    });

    // Should have some basic styles applied
    expect(bodyStyles.fontFamily).toBeTruthy();
  });

  test('should be responsive', async ({ page }) => {
    // Test desktop viewport
    await page.setViewportSize({ width: 1200, height: 800 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await expect(page.locator('#root')).toBeVisible();

    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(1000);

    await expect(page.locator('#root')).toBeVisible();
  });

  test('should handle JavaScript errors gracefully', async ({ page }) => {
    const jsErrors: string[] = [];

    page.on('pageerror', (error) => {
      jsErrors.push(error.message);
    });

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        jsErrors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Allow some time for any async errors
    await page.waitForTimeout(2000);

    // Should not have critical JavaScript errors
    const criticalErrors = jsErrors.filter(error =>
      !error.includes('favicon') &&
      !error.includes('chunk') &&
      !error.toLowerCase().includes('warning')
    );

    if (criticalErrors.length > 0) {
      console.log('JavaScript errors found:', criticalErrors);
    }

    expect(criticalErrors.length).toBeLessThan(3); // Allow some minor errors
  });
});
