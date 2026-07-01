---
name: "webapp-testing-playwright"
description: "Load this skill when you need to automate web application testing. Connects Claude's code engine with automated browsers to script, validate, and execute complex UI test flows end-to-end."
---
# Webapp Testing via Playwright

Connects Claude's code engine directly with automated web browsers. Empowers Claude to script, validate, and execute complex user experience UI test flows end-to-end.

## Natural Triggers
- "test this web app"
- "automate UI testing"
- "Playwright test"
- "end-to-end test"
- "browser automation"
- "test user flows"
- "UI validation"
- "cross-browser testing"
- "web application test"

## Core Capabilities

### Browser Automation
- Control Chrome, Firefox, WebKit
- Simulate user interactions
- Navigate pages
- Handle popups and dialogs
- Manage tabs and windows

### Test Authoring
- Write test scripts in JavaScript/TypeScript
- Use declarative syntax
- Create reusable components
- Define test data
- Handle assertions

### Test Execution
- Run tests in headless mode
- Run tests with visible browser
- Parallel test execution
- Cross-browser testing
- CI/CD integration

### Reporting
- Generate test reports
- Capture screenshots
- Record videos
- Collect traces
- Generate HTML reports

## Setup

### Installation
```bash
# Install Playwright
npm init playwright@latest

# Or install as dev dependency
npm install --save-dev @playwright/test

# Install browsers
npx playwright install
```

### Project Structure
```
project/
  tests/
    example.spec.ts
    login.spec.ts
    checkout.spec.ts
  playwright.config.ts
  package.json
```

### Configuration (playwright.config.ts)
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
});
```

## Test Writing

### Basic Test Structure
```typescript
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  // Navigate to page
  await page.goto('https://example.com');
  
  // Assert title
  await expect(page).toHaveTitle(/Example Domain/);
  
  // Click element
  await page.click('text=Get Started');
  
  // Fill form
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password123');
  
  // Submit form
  await page.click('button[type="submit"]');
  
  // Assert result
  await expect(page).toHaveURL(/dashboard/);
});
```

### Page Objects
```typescript
// pages/LoginPage.ts
import { Locator, Page } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.locator('#username');
    this.passwordInput = page.locator('#password');
    this.submitButton = page.locator('button[type="submit"]');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// tests/login.spec.ts
import { test } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('login test', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('https://example.com/login');
  await loginPage.login('testuser', 'password123');
  await expect(page).toHaveURL(/dashboard/);
});
```

### Fixtures
```typescript
// tests.fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

export const test = base.extend({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await page.goto('https://example.com/login');
    await use(loginPage);
  },
});

// tests/login.spec.ts
import { test } from '../tests.fixtures';

test('login with fixture', async ({ loginPage }) => {
  await loginPage.login('testuser', 'password123');
  await expect(loginPage.page).toHaveURL(/dashboard/);
});
```

## Common Test Patterns

### Authentication
```typescript
// Global setup (playwright.config.ts)
import { chromium } from '@playwright/test';

async function globalSetup() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com/login');
  await page.fill('#username', 'admin');
  await page.fill('#password', 'admin123');
  await page.click('button[type="submit"]');
  await page.context().storageState({ path: 'storageState.json' });
  await browser.close();
}

// Use in tests
test.use({ storageState: 'storageState.json' });
```

### Form Testing
```typescript
test('form submission', async ({ page }) => {
  await page.goto('https://example.com/form');
  
  // Fill form
  await page.fill('#name', 'John Doe');
  await page.fill('#email', 'john@example.com');
  await page.selectOption('#country', 'US');
  await page.check('#subscribe');
  
  // Submit and verify
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/thank-you/);
  await expect(page.locator('.confirmation')).toHaveText(/Thank you/);
});
```

### Navigation Testing
```typescript
test('navigation flow', async ({ page }) => {
  await page.goto('https://example.com');
  
  // Test main navigation
  await page.click('text=Products');
  await expect(page).toHaveURL(/products/);
  
  await page.click('text=About');
  await expect(page).toHaveURL(/about/);
  
  await page.click('text=Home');
  await expect(page).toHaveURL(/$/);
});
```

### API Testing
```typescript
test('API testing', async ({ request }) => {
  // POST request
  const response = await request.post('https://api.example.com/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com'
    }
  });
  
  expect(response.status()).toBe(201);
  const responseBody = await response.json();
  expect(responseBody.id).toBeTruthy();
  
  // GET request
  const getResponse = await request.get(`https://api.example.com/users/${responseBody.id}`);
  expect(getResponse.status()).toBe(200);
});
```

### Visual Testing
```typescript
test('visual regression', async ({ page }) => {
  await page.goto('https://example.com');
  
  // Compare with baseline
  expect(await page.screenshot()).toMatchSnapshot('homepage.png');
});
```

### Mobile Testing
```typescript
test.use({ 
  viewport: { width: 375, height: 812 },
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)',
});

test('mobile view', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page.locator('.mobile-menu')).toBeVisible();
});
```

## Advanced Features

### Parallel Execution
```bash
# Run tests in parallel
npx playwright test --workers=4

# Run specific test files in parallel
npx playwright test tests/login tests/checkout --workers=2
```

### Cross-Browser Testing
```typescript
// playwright.config.ts
projects: [
  { name: 'chromium', use: { browserName: 'chromium' } },
  { name: 'firefox', use: { browserName: 'firefox' } },
  { name: 'webkit', use: { browserName: 'webkit' } },
  
  // Mobile emulation
  { 
    name: 'Mobile Chrome', 
    use: { 
      browserName: 'chromium',
      viewport: { width: 375, height: 812 },
      userAgent: 'iPhone'
    }
  },
]
```

### Test Retries
```typescript
// playwright.config.ts
export default defineConfig({
  retries: 2, // Retry failed tests twice
  
  // Or per-test
  test: {
    retries: 1
  }
});
```

### Custom Reporters
```typescript
// Custom reporter
import { Reporter, TestCase, TestResult, FullResult } from '@playwright/test/reporter';

class MyReporter implements Reporter {
  onBegin(config: FullConfig, suite: Suite) {
    console.log(`Starting test run with ${suite.allTests().length} tests`);
  }
  
  onTestBegin(test: TestCase) {
    console.log(`Starting test: ${test.title}`);
  }
  
  onTestEnd(test: TestCase, result: TestResult) {
    console.log(`Test ${test.title}: ${result.status}`);
  }
  
  onEnd(result: FullResult) {
    console.log(`Test run complete: ${result.status}`);
  }
}

// playwright.config.ts
export default defineConfig({
  reporter: [['html'], ['./my-reporter.ts']],
});
```

### Debugging
```bash
# Run in headed mode
npx playwright test --headed

# Run specific test
npx playwright test tests/login.spec.ts

# Debug with Playwright Inspector
npx playwright codegen https://example.com

# Show test report
npx playwright show-report
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright browsers
      run: npx playwright install --with-deps
    - name: Run Playwright tests
      run: npx playwright test
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: playwright-report
        path: playwright-report/
```

### GitLab CI
```yaml
test:
  image: mcr.microsoft.com/playwright:v1.32.1-focal
  script:
    - npm ci
    - npx playwright install --with-deps
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
```

### Azure Pipelines
```yaml
- task: NodeTool@0
  inputs:
    versionSpec: '16.x'

- script: |
    npm ci
    npx playwright install --with-deps
    npx playwright test
  displayName: 'Run Playwright tests'

- task: PublishPipelineArtifact@1
  inputs:
    targetPath: 'playwright-report'
    artifact: 'playwright-report'
```

## Best Practices

### Test Organization
- Group related tests together
- Use descriptive test names
- Keep tests focused and independent
- Avoid test interdependence
- Use setup and teardown appropriately

### Selectors
- Prefer text content over complex selectors
- Use role-based selectors for accessibility
- Avoid brittle XPath selectors
- Use test IDs for stable elements
- Keep selectors simple and readable

### Assertions
- Use explicit assertions
- Assert on user-visible behavior
- Avoid asserting on implementation details
- Use soft assertions when appropriate
- Provide meaningful error messages

### Data Management
- Use test data builders
- Generate unique test data
- Clean up test data after tests
- Use fixtures for common test data
- Externalize test data when large

### Performance
- Avoid unnecessary waits
- Use auto-waiting when possible
- Parallelize independent tests
- Reuse browser contexts
- Optimize test execution

## Common Anti-Patterns

### ❌ Don't
- Use `page.waitForTimeout()` (use proper wait conditions)
- Hardcode waits (use auto-waiting)
- Create interdependent tests
- Test implementation details
- Ignore test failures
- Skip cleanup

### ✅ Do
- Use `page.waitForSelector()` or `expect(locator).toBeVisible()`
- Let Playwright auto-wait for actions
- Keep tests independent
- Test user-visible behavior
- Investigate and fix failures
- Always clean up test data

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- Playwright Documentation: https://playwright.dev/
- Playwright GitHub: https://github.com/microsoft/playwright
- Playwright API Reference: https://playwright.dev/docs/api

## Integration with Other Skills
- **Pypict Combinatorial QA**: For generating test data combinations
- **Test-Driven Development**: For writing tests first
- **Systematic Debugging**: For analyzing test failures
- **Finishing a Dev Branch**: For including tests in merge workflows
