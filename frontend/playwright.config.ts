import { defineConfig, devices } from '@playwright/test';

// Get frontend port from environment variable or use default
const FRONTEND_PORT = process.env.FRONTEND_PORT || '5173';
const FRONTEND_URL = `http://127.0.0.1:${FRONTEND_PORT}`;

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 2,
  reporter: 'html',
  use: {
    baseURL: FRONTEND_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: FRONTEND_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
