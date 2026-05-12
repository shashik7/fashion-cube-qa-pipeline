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
import os
import json
from datetime import datetime


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


# File-based storage for AI results to support xdist/parallel workers
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
AI_DATA_FILE = os.path.join(REPORTS_DIR, "ai_results_cache.json")


def _save_ai_result(nodeid, result):
    """Save AI result to a shared JSON file."""
    data = {}
    if os.path.exists(AI_DATA_FILE):
        try:
            with open(AI_DATA_FILE, "r") as f:
                data = json.load(f)
        except:
            pass
    
    data[nodeid] = result
    
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
        
    with open(AI_DATA_FILE, "w") as f:
        json.dump(data, f)


def _get_ai_result(nodeid):
    """Retrieve AI result from the shared JSON file."""
    if os.path.exists(AI_DATA_FILE):
        try:
            with open(AI_DATA_FILE, "r") as f:
                data = json.load(f)
                return data.get(nodeid, {})
        except:
            pass
    return {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """FC-001: Attach test result and perform AI self-healing on failure."""
    outcome = yield
    report = outcome.get_result()
    
    # Store report on item for screenshot fixture access
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        log_text = report.longreprtext
        analysis_result = {
            "status": "failed",
            "classification": "Unknown",
            "root_cause": "Manual review required",
            "message": "Analysis skipped or failed"
        }

        # ── Attempt 1: LangChain LLM Healer ──
        try:
            from langchain_healer import LangChainHealer
            healer = LangChainHealer()
            if healer.llm is not None:
                llm_result = healer.heal(log_text)
                if llm_result:
                    analysis_result = llm_result
                    if llm_result.get("status") == "fixed":
                        print(f"\n[AI-HEAL] LangChain: {llm_result['message']}")
                        _save_ai_result(report.nodeid, analysis_result)
                        return
        except Exception as e:
            print(f"\n[AI-HEAL] LangChain unavailable ({e}), falling back to regex...")

        # ── Attempt 2: Regex-Based Fallback ──
        try:
            from ai_failure_analyzer import AIFailureAnalyzer
            analyzer = AIFailureAnalyzer()
            regex_result = analyzer.analyze(log_text)
            
            # If LLM failed, use regex results
            if analysis_result.get("classification") == "Unknown":
                analysis_result["classification"] = regex_result.get("classification", "Unknown")
                analysis_result["root_cause"] = regex_result.get("root_cause", "Manual review required")
            
            analyzer.print_analysis(regex_result)
            heal_result = analyzer.self_heal(log_text)
            print(f"\n[AI-HEAL] Regex: {heal_result.get('status', 'unknown')}: {heal_result.get('message', '')}")
        except Exception as e:
            print(f"\n[AI-HEAL] Analyzer error (non-blocking): {e}")

        # Store for HTML report
        _save_ai_result(report.nodeid, analysis_result)


def pytest_html_results_table_header(cells):
    """FC-001: Add AI columns to the report table."""
    from py.xml import html
    cells.insert(2, html.th("AI Classification", class_="sortable"))
    cells.insert(3, html.th("AI Root Cause", class_="sortable"))
    if len(cells) > 4:
        cells.pop() # Remove the Links column to make space


def pytest_html_results_table_row(report, cells):
    """FC-001: Populate AI columns in the report table."""
    from py.xml import html
    
    # Retrieve from file storage (to support xdist)
    ai_heal = _get_ai_result(report.nodeid)
    
    status = ai_heal.get("status", "failed")
    classification = ai_heal.get("classification", "Analysis Error" if status == "error" else "N/A")
    root_cause = ai_heal.get("root_cause", ai_heal.get("message", "N/A"))
    
    # Color coding based on classification
    color = "#f8f9fa" # Default (Off-white)
    text_color = "#212529"
    
    if "Timing" in classification:
        color = "#fff3cd" # Yellow
        text_color = "#856404"
    elif "Selector" in classification:
        color = "#f8d7da" # Red
        text_color = "#721c24"
    elif "Data" in classification:
        color = "#d1ecf1" # Blue
        text_color = "#0c5460"
    elif "Success" in classification or status == "fixed":
        color = "#d4edda" # Green
        text_color = "#155724"

    cells.insert(2, html.td(classification, style=f"background-color: {color}; color: {text_color}; font-weight: bold; border: 1px solid #dee2e6;"))
    cells.insert(3, html.td(root_cause, style=f"background-color: {color}; color: {text_color}; border: 1px solid #dee2e6;"))
    if len(cells) > 5:
        cells.pop() # Remove the Links cell


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """FC-001: Configure HTML report styling and metadata."""
    if not hasattr(config, "_metadata"):
        config._metadata = {}
    config._metadata['AI Engine'] = 'LangChain (Gemini)'
    config._metadata['Project'] = 'Fashion Cube'


def pytest_html_report_title(report):
    report.title = "Fashion Cube - AI Self-Healing QA Infrastructure"


def pytest_html_results_summary(prefix, summary, postfix):
    from py.xml import html
    prefix.extend([
        html.h2("AI Self-Healing Insights", style="color: #007bff; margin-top: 20px; font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif;"),
        html.p("This report includes automated root-cause analysis and code-level fixes generated by the LangChain AI engine.", 
               style="font-style: italic; color: #6c757d;")
    ])

