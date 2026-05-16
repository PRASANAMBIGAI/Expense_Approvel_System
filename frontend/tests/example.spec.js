import { test, expect } from '@playwright/test';

test('has title and login page loads', async ({ page }) => {
  await page.goto('/');

  // Check if the page title is set
  await expect(page).toHaveTitle(/Expense/i);
});
