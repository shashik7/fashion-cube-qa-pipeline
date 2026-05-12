# ============================================================================
# FC-001 | Fashion Cube QA Automation - Configuration Module
# Requirement: Environment-based configuration for all test suites
# ============================================================================

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Jira Traceability
# ---------------------------------------------------------------------------
JIRA_ID = "FC-001"
JIRA_SUMMARY = (
    "As a user, I can browse products, view product details, register/login, "
    "manage my shopping cart, filter/search products by category/department, "
    "and checkout via PayPal."
)

# ---------------------------------------------------------------------------
# Environment URLs
# ---------------------------------------------------------------------------
BASE_URL = os.getenv("BASE_URL", "http://localhost:3001/fashion-cube")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")

# ---------------------------------------------------------------------------
# Timeouts (milliseconds for Playwright, seconds for API)
# ---------------------------------------------------------------------------
DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "30000"))
NAVIGATION_TIMEOUT_MS = int(os.getenv("NAVIGATION_TIMEOUT_MS", "60000"))
API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))

# ---------------------------------------------------------------------------
# Test Credentials
# ---------------------------------------------------------------------------
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "testuser@fashioncube.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "Test@12345")
TEST_USER_FULLNAME = os.getenv("TEST_USER_FULLNAME", "Test User")

# ---------------------------------------------------------------------------
# Browser Configuration
# ---------------------------------------------------------------------------
BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "1000"))
VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1280"))
VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "720"))

# ---------------------------------------------------------------------------
# Report Configuration
# ---------------------------------------------------------------------------
REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

# ---------------------------------------------------------------------------
# API Endpoints (relative to API_BASE_URL)
# ---------------------------------------------------------------------------
ENDPOINTS = {
    "products": "/products",
    "product_by_id": "/products/{product_id}",
    "variants": "/variants",
    "variant_by_id": "/variants/{variant_id}",
    "departments": "/departments",
    "categories": "/categories",
    "search": "/search",
    "filter": "/filter",
    "login": "/users/login",
    "register": "/users/signin",
    "cart": "/users/{user_id}/cart",
    "checkout": "/checkout/{cart_id}",
    "payment_success": "/payment/success",
}
