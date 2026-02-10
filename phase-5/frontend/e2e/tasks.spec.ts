import { test, expect, Page } from '@playwright/test';

test.describe('Task Management - E2E Tests', () => {
  let page: Page;

  test.beforeEach(async ({ page: testPage }) => {
    page = testPage;

    // Navigate to application
    await page.goto('http://localhost:3000');

    // Login (assuming auth is implemented)
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'Test123!@#');
    await page.click('button[type="submit"]');

    // Wait for redirect to tasks page
    await page.waitForURL('**/tasks');
  });

  test.describe('Task Creation', () => {
    test('should create a new task', async () => {
      // Click create task button
      await page.click('button:has-text("New Task")');

      // Fill task form
      await page.fill('input[name="title"]', 'E2E Test Task');
      await page.fill('textarea[name="description"]', 'This is an E2E test task');
      await page.selectOption('select[name="priority"]', 'high');

      // Add tags
      await page.fill('input[name="tags"]', 'test');
      await page.keyboard.press('Enter');
      await page.fill('input[name="tags"]', 'e2e');
      await page.keyboard.press('Enter');

      // Submit form
      await page.click('button:has-text("Create Task")');

      // Verify task appears in list
      await expect(page.locator('text=E2E Test Task')).toBeVisible();
      await expect(page.locator('text=This is an E2E test task')).toBeVisible();

      // Verify tags are displayed
      await expect(page.locator('span:has-text("test")')).toBeVisible();
      await expect(page.locator('span:has-text("e2e")')).toBeVisible();
    });

    test('should show validation errors for invalid input', async () => {
      await page.click('button:has-text("New Task")');

      // Try to submit without title
      await page.click('button:has-text("Create Task")');

      // Verify error message
      await expect(page.locator('text=Title is required')).toBeVisible();
    });

    test('should create recurring task', async () => {
      await page.click('button:has-text("New Task")');

      await page.fill('input[name="title"]', 'Daily Standup');
      await page.check('input[name="isRecurring"]');
      await page.selectOption('select[name="recurrencePattern"]', 'daily');

      await page.click('button:has-text("Create Task")');

      // Verify recurring indicator
      await expect(page.locator('[data-testid="recurring-badge"]')).toBeVisible();
    });
  });

  test.describe('Task Editing', () => {
    test('should edit existing task', async () => {
      // Create a task first
      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Task to Edit');
      await page.click('button:has-text("Create Task")');

      // Click edit button
      await page.click('[data-testid="edit-task-button"]');

      // Update title
      await page.fill('input[name="title"]', 'Updated Task Title');
      await page.selectOption('select[name="priority"]', 'urgent');

      // Save changes
      await page.click('button:has-text("Save")');

      // Verify changes
      await expect(page.locator('text=Updated Task Title')).toBeVisible();
      await expect(page.locator('[data-priority="urgent"]')).toBeVisible();
    });
  });

  test.describe('Task Completion', () => {
    test('should mark task as complete', async () => {
      // Create a task
      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Task to Complete');
      await page.click('button:has-text("Create Task")');

      // Mark as complete
      await page.click('[data-testid="complete-checkbox"]');

      // Verify completed state
      await expect(page.locator('[data-testid="complete-checkbox"]')).toBeChecked();
      await expect(page.locator('text=Task to Complete')).toHaveClass(/completed/);
    });

    test('should show completion animation', async () => {
      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Animated Task');
      await page.click('button:has-text("Create Task")');

      await page.click('[data-testid="complete-checkbox"]');

      // Verify animation class is applied
      const taskElement = page.locator('[data-testid="task-item"]').first();
      await expect(taskElement).toHaveClass(/completing/);
    });
  });

  test.describe('Task Filtering', () => {
    test.beforeEach(async () => {
      // Create multiple tasks with different properties
      const tasks = [
        { title: 'High Priority Work', priority: 'high', tags: ['work'] },
        { title: 'Low Priority Personal', priority: 'low', tags: ['personal'] },
        { title: 'Urgent Work Task', priority: 'urgent', tags: ['work', 'urgent'] },
      ];

      for (const task of tasks) {
        await page.click('button:has-text("New Task")');
        await page.fill('input[name="title"]', task.title);
        await page.selectOption('select[name="priority"]', task.priority);

        for (const tag of task.tags) {
          await page.fill('input[name="tags"]', tag);
          await page.keyboard.press('Enter');
        }

        await page.click('button:has-text("Create Task")');
        await page.waitForTimeout(500);
      }
    });

    test('should filter by priority', async () => {
      await page.selectOption('select[name="filterPriority"]', 'high');

      await expect(page.locator('text=High Priority Work')).toBeVisible();
      await expect(page.locator('text=Low Priority Personal')).not.toBeVisible();
    });

    test('should filter by tags', async () => {
      await page.click('button:has-text("Filter by Tags")');
      await page.click('label:has-text("work")');

      await expect(page.locator('text=High Priority Work')).toBeVisible();
      await expect(page.locator('text=Urgent Work Task')).toBeVisible();
      await expect(page.locator('text=Low Priority Personal')).not.toBeVisible();
    });

    test('should search tasks', async () => {
      await page.fill('input[placeholder="Search tasks..."]', 'Urgent');

      await expect(page.locator('text=Urgent Work Task')).toBeVisible();
      await expect(page.locator('text=High Priority Work')).not.toBeVisible();
    });
  });

  test.describe('Real-Time Sync', () => {
    test('should sync task updates across tabs', async ({ context }) => {
      // Open second tab
      const secondPage = await context.newPage();
      await secondPage.goto('http://localhost:3000/tasks');

      // Create task in first tab
      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Sync Test Task');
      await page.click('button:has-text("Create Task")');

      // Verify task appears in second tab
      await expect(secondPage.locator('text=Sync Test Task')).toBeVisible({ timeout: 5000 });

      await secondPage.close();
    });

    test('should show real-time completion updates', async ({ context }) => {
      const secondPage = await context.newPage();
      await secondPage.goto('http://localhost:3000/tasks');

      // Create task
      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Real-Time Task');
      await page.click('button:has-text("Create Task")');

      // Wait for sync
      await page.waitForTimeout(1000);

      // Complete in first tab
      await page.click('[data-testid="complete-checkbox"]');

      // Verify completion in second tab
      const checkbox = secondPage.locator('[data-testid="complete-checkbox"]').first();
      await expect(checkbox).toBeChecked({ timeout: 5000 });

      await secondPage.close();
    });
  });

  test.describe('Audit Trail', () => {
    test('should display audit history', async () => {
      // Create and modify a task
      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Audited Task');
      await page.click('button:has-text("Create Task")');

      // Edit task
      await page.click('[data-testid="edit-task-button"]');
      await page.fill('input[name="title"]', 'Modified Task');
      await page.click('button:has-text("Save")');

      // Navigate to audit page
      await page.click('a:has-text("Audit")');

      // Verify audit entries
      await expect(page.locator('text=task.created')).toBeVisible();
      await expect(page.locator('text=task.updated')).toBeVisible();
    });
  });

  test.describe('Reminders', () => {
    test('should set reminder for task', async () => {
      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Task with Reminder');

      // Set due date
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      await page.fill('input[name="dueDate"]', tomorrow.toISOString().split('T')[0]);

      // Enable reminder
      await page.check('input[name="enableReminder"]');
      await page.check('input[name="reminderChannels"][value="email"]');

      await page.click('button:has-text("Create Task")');

      // Verify reminder indicator
      await expect(page.locator('[data-testid="reminder-badge"]')).toBeVisible();
    });
  });

  test.describe('Accessibility', () => {
    test('should be keyboard navigable', async () => {
      // Tab through interface
      await page.keyboard.press('Tab');
      await page.keyboard.press('Tab');
      await page.keyboard.press('Enter'); // Open create dialog

      // Fill form with keyboard
      await page.keyboard.type('Keyboard Task');
      await page.keyboard.press('Tab');
      await page.keyboard.type('Created with keyboard');

      // Submit with keyboard
      await page.keyboard.press('Tab');
      await page.keyboard.press('Tab');
      await page.keyboard.press('Enter');

      await expect(page.locator('text=Keyboard Task')).toBeVisible();
    });

    test('should have proper ARIA labels', async () => {
      await expect(page.locator('[aria-label="Create new task"]')).toBeVisible();
      await expect(page.locator('[aria-label="Search tasks"]')).toBeVisible();
      await expect(page.locator('[role="main"]')).toBeVisible();
    });
  });

  test.describe('Error Handling', () => {
    test('should handle network errors gracefully', async () => {
      // Simulate offline
      await page.context().setOffline(true);

      await page.click('button:has-text("New Task")');
      await page.fill('input[name="title"]', 'Offline Task');
      await page.click('button:has-text("Create Task")');

      // Verify error message
      await expect(page.locator('text=Network error')).toBeVisible();

      // Go back online
      await page.context().setOffline(false);
    });

    test('should retry failed operations', async () => {
      // This would require mocking API failures
      // Implementation depends on retry logic in the app
    });
  });
});
