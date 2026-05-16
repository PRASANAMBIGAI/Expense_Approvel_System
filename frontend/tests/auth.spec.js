import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  const uniqueId = Date.now();
  const employeeEmail = `employee${uniqueId}@test.com`;
  const password = 'password123';

  test('should register a new employee and log in successfully', async ({ page }) => {
    // 1. Navigate to Registration Page
    await page.goto('/register');
    await expect(page.locator('h2')).toContainText('Create Account');

    // 2. Fill out Registration Form
    await page.fill('input[name="employee_name"]', 'Test Employee');
    await page.fill('input[name="employee_email"]', employeeEmail);
    await page.fill('input[name="password"]', password);
    await page.selectOption('select[name="role"]', 'employee');
    
    // 3. Submit
    await page.click('button[type="submit"]');

    // 4. Should redirect to Login page
    await expect(page).toHaveURL(/.*\/login/);
    await expect(page.locator('h2')).toContainText('Welcome Back');

    // 5. Login with new credentials
    await page.fill('input[name="employee_email"]', employeeEmail);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');

    // 6. Should redirect to Employee Dashboard
    await expect(page).toHaveURL(/.*\/employee\/dashboard/);
    await expect(page.locator('h1')).toContainText('My Expenses');
  });

  test('should fail login with invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="employee_email"]', 'wrong@test.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    // Should show error message
    const errorMsg = page.locator('.error-message');
    await expect(errorMsg).toBeVisible();
    await expect(errorMsg).toContainText('Invalid email or password');
  });
});
