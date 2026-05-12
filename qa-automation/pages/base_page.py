# ============================================================================
# FC-001 | Fashion Cube QA Automation - Base Page Object
# Requirement: Reusable page object methods with explicit waits and
#              exception handling for all page objects
# ============================================================================

import os
from config.config import REPORTS_DIR, DEFAULT_TIMEOUT_MS


class BasePage:
    """FC-001: Base Page Object with reusable methods for all pages."""

    def __init__(self, page):
        self.page = page
        self.timeout = DEFAULT_TIMEOUT_MS

    # ---- Navigation ----

    def navigate(self, url):
        """FC-001: Navigate to a URL with error handling and retry mechanism."""
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    self.take_screenshot("navigation_error")
                    raise AssertionError(f"FC-001: Failed to navigate to {url} after {max_retries} attempts: {e}")
                print(f"Navigation attempt {attempt + 1} failed, retrying in 2s... ({e})")
                time.sleep(2)
    
    def reload(self):
        """FC-001: Reload the current page."""
        self.page.reload(wait_until="domcontentloaded")

    # ---- Wait Methods ----

    def wait_for_element(self, selector, state="visible", timeout=None):
        """FC-001: Wait for an element with explicit wait."""
        timeout = timeout or self.timeout
        try:
            # Ensure the DOM is loaded before attempting to find or wait for any element. # [AI-HEAL]
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout) # [AI-HEAL]
            # The following block for 'hidden' state is now redundant due to the general wait above.
            # if state == "hidden": # [AI-HEAL]
            #     # Before waiting for an element to be hidden, ensure the page has settled. # [AI-HEAL]
            #     # This helps with race conditions where the element might still be present # [AI-HEAL]
            #     # while the page is navigating or loading new content after an action. # [AI-HEAL]
            #     self.page.wait_for_load_state("domcontentloaded", timeout=timeout) # [AI-HEAL]
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
            return self.page.locator(selector)
        except Exception as e:
            self.take_screenshot("wait_timeout")
            raise AssertionError(
                f"FC-001: Element '{selector}' not {state} within {timeout}ms: {e}"
            )

    def wait_for_url(self, url_pattern, timeout=None):
        """FC-001: Wait for URL to match pattern."""
        timeout = timeout or self.timeout
        try:
            self.page.wait_for_url(url_pattern, timeout=timeout)
        except Exception as e:
            raise AssertionError(
                f"FC-001: URL did not match '{url_pattern}' within {timeout}ms: {e}"
            )

    def wait_for_network_idle(self, timeout=None):
        """FC-001: Wait for network to be idle."""






        timeout = timeout or self.timeout
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            pass  # Non-critical; page may have long-polling

    # ---- Interaction Methods ----

    def click(self, selector, timeout=None):
        """FC-001: Click an element with explicit wait."""
        element = self.wait_for_element(selector, timeout=timeout)
        element.click()

    def fill(self, selector, value, timeout=None):
        """FC-001: Fill an input field with explicit wait and clear first."""
        element = self.wait_for_element(selector, timeout=timeout)
        element.fill("")
        element.fill(value)

    def get_text(self, selector, timeout=None):
        """FC-001: Get text content of an element."""
        element = self.wait_for_element(selector, timeout=timeout)
        return element.text_content()

    def get_input_value(self, selector, timeout=None):
        """FC-001: Get value of an input field."""
        element = self.wait_for_element(selector, timeout=timeout)
        return element.input_value()

    def is_visible(self, selector, timeout=5000):
        """FC-001: Check if an element is visible."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_hidden(self, selector, timeout=5000):
        """FC-001: Check if an element is hidden."""
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
            return True
        except Exception:
            return False

    def hover(self, selector, timeout=None):
        """FC-001: Hover over an element."""
        element = self.wait_for_element(selector, timeout=timeout)
        element.hover()

    def get_element_count(self, selector):
        """FC-001: Get count of elements matching selector."""
        return self.page.locator(selector).count()

    def get_all_texts(self, selector):
        """FC-001: Get all text contents for matching elements."""
        return self.page.locator(selector).all_text_contents()

    # ---- Assertions ----

    def assert_element_visible(self, selector, message=None):
        """FC-001: Assert that an element is visible."""
        assert self.is_visible(selector), (
            message or f"FC-001: Expected element '{selector}' to be visible"
        )

    def assert_element_hidden(self, selector, message=None):
        """FC-001: Assert that an element is hidden."""
        assert self.is_hidden(selector), (
            message or f"FC-001: Expected element '{selector}' to be hidden"
        )

    def assert_text_contains(self, selector, expected_text, message=None):
        """FC-001: Assert element text contains expected text."""
        actual_text = self.get_text(selector)
        assert expected_text in actual_text, (
            message
            or f"FC-001: Expected '{expected_text}' in '{actual_text}'"
        )

    def assert_url_contains(self, expected_url_part, message=None):
        """FC-001: Assert current URL contains expected string."""
        current_url = self.page.url
        assert expected_url_part in current_url, (
            message
            or f"FC-001: Expected '{expected_url_part}' in URL '{current_url}'"
        )

    # ---- Utilities ----

    def take_screenshot(self, name):
        """FC-001: Take a screenshot and save to reports directory."""
        os.makedirs(REPORTS_DIR, exist_ok=True)
        path = os.path.join(REPORTS_DIR, f"{name}.png")
        try:
            self.page.screenshot(path=path, full_page=True)
        except Exception:
            pass
        return path

    def get_current_url(self):
        """FC-001: Get the current page URL."""
        return self.page.url

    def get_title(self):
        """FC-001: Get the current page title."""
        return self.page.title()
