# FC-001 | Fashion Cube – QA Automation Framework

> **Jira ID**: FC-001 – Full E-Commerce User Journey  
> **Application**: Fashion Cube (React + Redux + Express.js + MongoDB)

## 📁 Folder Structure

```
qa-automation/
│
├── requirements/
│     └── FC-001_requirement.md          # Jira requirement document
├── testcases/
│     ├── login_register.feature         # BDD: Auth scenarios (13 cases)
│     ├── product_browsing.feature       # BDD: Products/Search (11 cases)
│     └── shopping_cart.feature          # BDD: Cart/Checkout (12 cases)
├── pages/
│     ├── base_page.py                   # Base POM with reusable methods
│     ├── login_page.py                  # Login page object
│     ├── register_page.py              # Registration page object
│     ├── home_page.py                   # Home page object
│     ├── product_page.py               # Product detail page object
│     └── cart_page.py                   # Cart page object
├── tests/
│     ├── ui/
│     │     ├── test_login.py            # Login UI tests
│     │     ├── test_register.py         # Registration UI tests
│     │     ├── test_product_browsing.py # Product browsing UI tests
│     │     └── test_shopping_cart.py    # Cart UI tests
│     └── api/
│           ├── test_products_api.py     # Products API tests
│           ├── test_auth_api.py         # Auth API tests
│           └── test_cart_api.py         # Cart API tests
├── performance/
│     └── ecommerce_load.js              # k6 load test
├── reports/                             # Generated test reports
├── config/
│     └── config.py                      # Environment configuration
├── conftest.py                          # Pytest fixtures
├── pytest.ini                           # Pytest settings
├── requirements.txt                     # Python dependencies
├── ai_failure_analyzer.py               # AI failure analysis tool
└── .github/workflows/
      └── qa-pipeline.yml               # CI/CD pipeline
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js (for k6)
- Fashion Cube backend running locally

### 1. Install Dependencies

```bash
cd qa-automation
pip install -r requirements.txt
playwright install --with-deps chromium
```

### 2. Configure Environment

Create a `.env` file or set environment variables:

```bash
export BASE_URL="http://localhost:3000/fashion-cube"
export API_BASE_URL="http://localhost:3000"
export TEST_USER_EMAIL="testuser@fashioncube.com"
export TEST_USER_PASSWORD="Test@12345"
export HEADLESS="true"
export BROWSER="chromium"
```

### 3. Run Tests

```bash
# Run all tests
pytest -v --html=reports/report.html --self-contained-html

# Run only UI tests
pytest tests/ui/ -m ui -v --html=reports/ui_report.html

# Run only API tests
pytest tests/api/ -m api -v --html=reports/api_report.html

# Run smoke tests only
pytest -m smoke -v

# Run negative tests only
pytest -m negative -v

# Run with parallel execution
pytest -n auto -v
```

### 4. Run k6 Performance Tests

```bash
# Install k6 (https://k6.io/docs/get-started/installation/)

# Run load test
k6 run performance/ecommerce_load.js

# Run with custom environment
k6 run -e API_BASE_URL=http://staging:3000 performance/ecommerce_load.js
```

### 5. AI Failure Analyzer

```bash
# Analyze a log file
python ai_failure_analyzer.py path/to/failure.log

# Interactive mode (paste logs)
python ai_failure_analyzer.py
```

## 🧪 Test Coverage Summary

| Category | Test File | Count | Types |
|----------|-----------|-------|-------|
| Login UI | `test_login.py` | 9 | Functional, Negative, Edge, Boundary, State |
| Register UI | `test_register.py` | 4 | Functional, Negative, Boundary |
| Product UI | `test_product_browsing.py` | 7 | Functional, Negative, Edge, Boundary, State |
| Cart UI | `test_shopping_cart.py` | 5 | Functional, Negative, Edge, State |
| Products API | `test_products_api.py` | 14 | Functional, Negative, Edge, Boundary, Business |
| Auth API | `test_auth_api.py` | 12 | Functional, Negative, Edge, Token Validation |
| Cart API | `test_cart_api.py` | 8 | Functional, Negative, Edge, Business Rule |
| **Total** | | **59** | |

## 🏗️ Architecture

- **POM (Page Object Model)**: All UI interactions abstracted into page classes
- **Explicit Waits**: No hardcoded sleeps; all waits use Playwright's built-in wait mechanisms
- **Stable Locators**: Priority: `id` > `CSS class` > `text` > structural selectors
- **Environment Config**: All URLs, credentials, and timeouts via environment variables
- **Jira Traceability**: Every test name contains `FC-001`, every file header references the Jira ID

## 📊 CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/qa-pipeline.yml`) runs:

1. **UI Tests** → Playwright headless Chrome → HTML report
2. **API Tests** → pytest + requests → HTML report
3. **Performance Tests** → k6 load test → JSON report
4. **Results Summary** → Fail pipeline if any test suite fails

Reports are uploaded as GitHub Actions artifacts for 30-day retention.

## 🤖 AI Failure Analyzer

When test failures occur, the analyzer classifies root causes:

| Category | Example Pattern |
|----------|----------------|
| 🎯 Locator Issue | `Element not found`, `selector not visible` |
| ⏱️ Timing Issue | `Timeout exceeded`, `waiting for timed out` |
| 🧠 Business Logic | `AssertionError`, `expected but got` |
| 🌐 API Defect | `HTTP 500`, `ConnectionRefused` |
| 📊 Data Problem | `KeyError`, `NoneType`, `schema validation` |
| 🚀 Performance | `threshold exceeded`, `p95 exceeded` |

Each classification includes exact root cause, code-level fix, and application-level fix suggestions.
