import { test, expect } from '@playwright/test';

test.describe('End-to-End Expense Flow', () => {
  const uniqueId = Date.now();
  const adminEmail = `admin${uniqueId}@test.com`;
  const managerEmail = `manager${uniqueId}@test.com`;
  const employeeEmail = `employee${uniqueId}@test.com`;
  const password = 'password123';

  test('Complete flow: Admin creates category, Employee creates expense, Manager approves', async ({ page }) => {
    // ==========================================
    // 1. Register and Login as Admin
    // ==========================================
    await page.goto('/register');
    await page.fill('input[name="employee_name"]', 'System Admin');
    await page.fill('input[name="employee_email"]', adminEmail);
    await page.fill('input[name="password"]', password);
    await page.selectOption('select[name="role"]', 'admin');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/login/);
    await page.fill('input[name="employee_email"]', adminEmail);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');

    // Admin Dashboard
    await expect(page).toHaveURL(/.*\/admin\/dashboard/);
    
    // Create a new Category
    await page.fill('input[placeholder="Category Name"]', `Travel ${uniqueId}`);
    await page.fill('input[placeholder="Description (Optional)"]', 'Travel expenses');
    await page.click('button:has-text("Add Category")');
    
    // Ensure category is added
    await expect(page.locator('table')).toContainText(`Travel ${uniqueId}`);

    // Logout
    await page.click('text=Sign Out');

    // ==========================================
    // 2. Register Manager
    // ==========================================
    await page.goto('/register');
    await page.fill('input[name="employee_name"]', 'System Manager');
    await page.fill('input[name="employee_email"]', managerEmail);
    await page.fill('input[name="password"]', password);
    await page.selectOption('select[name="role"]', 'manager');
    await page.click('button[type="submit"]');

    // ==========================================
    // 3. Register and Login as Employee
    // ==========================================
    await page.goto('/register');
    await page.fill('input[name="employee_name"]', 'Regular Employee');
    await page.fill('input[name="employee_email"]', employeeEmail);
    await page.fill('input[name="password"]', password);
    await page.selectOption('select[name="role"]', 'employee');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/login/);
    await page.fill('input[name="employee_email"]', employeeEmail);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');

    // Employee Dashboard
    await expect(page).toHaveURL(/.*\/employee\/dashboard/);
    
    // Create an Expense
    await page.click('text=+ New Request');
    await page.fill('input[name="title"]', `Flight to NYC ${uniqueId}`);
    await page.fill('input[name="amount"]', '500');
    // Select the newly created category (should be selected by default if it's the first one, or we can select it)
    await page.selectOption('select[name="category_id"]', { label: `Travel ${uniqueId}` });
    await page.fill('textarea[name="description"]', 'Business trip to NYC');
    await page.click('button:has-text("Submit Request")');

    // Ensure expense shows up in the table
    await expect(page.locator('table')).toContainText(`Flight to NYC ${uniqueId}`);
    await expect(page.locator('table')).toContainText('Pending');

    // Logout
    await page.click('text=Sign Out');

    // ==========================================
    // 4. Login as Manager to Approve Expense
    // ==========================================
    await expect(page).toHaveURL(/.*\/login/);
    await page.fill('input[name="employee_email"]', managerEmail);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');

    // Manager Dashboard
    await expect(page).toHaveURL(/.*\/manager\/dashboard/);
    
    // Find the expense and click it
    await page.click(`text=Flight to NYC ${uniqueId}`);

    // Modal should be open
    await expect(page.locator('.modal-content')).toBeVisible();
    
    // Approve it
    await page.click('button:has-text("Approve Request")');

    // Ensure it shows as approved in the manager queue
    // Wait for modal to close
    await expect(page.locator('.modal-content')).not.toBeVisible();
    const row = page.locator('tr', { hasText: `Flight to NYC ${uniqueId}` });
    await expect(row).toContainText('Approved');
  });
});
