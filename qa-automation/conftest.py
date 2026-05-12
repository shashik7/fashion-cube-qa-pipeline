# ============================================================================
# FC-001 | Fashion Cube QA Automation - Shared Pytest Fixtures
# Requirement: Provide reusable browser and API fixtures for all test suites
# ============================================================================

import os
import pytest
from playwright.sync_api import sync_playwright
from config.config import (
    BASE_URL,
    API_BASE_URL,
    DEFAULT_TIMEOUT_MS,
    NAVIGATION_TIMEOUT_MS,
    BROWSER,
    HEADLESS,
    SLOW_MO,
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
    REPORTS_DIR,
    SCREENSHOT_ON_FAILURE,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)


@pytest.fixture(scope="session")
def browser_context_args():
    """FC-001: Browser context arguments for Playwright."""
    return {
        "viewport": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def playwright_instance():
    """FC-001: Launch Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """FC-001: Launch browser based on config."""
    browser_type = getattr(playwright_instance, BROWSER)
    browser = browser_type.launch(headless=HEADLESS, slow_mo=SLOW_MO)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser, browser_context_args):
    """FC-001: Provide a fresh page for each test function."""
    context = browser.new_context(**browser_context_args)
    context.set_default_timeout(DEFAULT_TIMEOUT_MS)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(browser, browser_context_args):
    """FC-001: Provide an authenticated page with login state."""
    context = browser.new_context(**browser_context_args)
    context.set_default_timeout(DEFAULT_TIMEOUT_MS)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
    page = context.new_page()

    # Inject auth token via localStorage
    page.goto(BASE_URL)
    page.evaluate(
        """() => {
        const mockAuth = {
            user_id: 'test_user_id',
            user_name: 'Test User',
            token: 'test_jwt_token',
            expire_in: '7d'
        };
        localStorage.setItem('auth', JSON.stringify(mockAuth));
    }"""
    )
    page.reload()
    yield page
    page.close()
    context.close()


@pytest.fixture
def app_base_url():
    """FC-001: Return the base URL for navigation."""
    return BASE_URL


@pytest.fixture
def app_api_base_url():
    """FC-001: Return the API base URL for API tests."""
    return API_BASE_URL


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """FC-001: Attach test result to request node for screenshot capture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_runtest_logreport(report):
    """FC-001: Auto-analyze and self-heal failures with AIFailureAnalyzer.

    Every test failure is analyzed AND auto-patched automatically.
    All patches are tagged with [AI-HEAL] for easy review.
    """
    if report.when == "call" and report.failed:
        try:
            from ai_failure_analyzer import AIFailureAnalyzer

            analyzer = AIFailureAnalyzer()
            log_text = report.longreprtext

            result = analyzer.analyze(log_text)
            analyzer.print_analysis(result)

            # Always self-heal
            heal_result = analyzer.self_heal(log_text)
            print(f"\n[AI-HEAL] {heal_result.get('status', 'unknown')}: {heal_result.get('message', '')}")
        except Exception as e:
            # Never let the analyzer crash the test runner
            print(f"\n[AI-HEAL] Analyzer error (non-blocking): {e}")


