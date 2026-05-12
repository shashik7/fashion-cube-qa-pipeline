# ============================================================================
# FC-001 | LangChain Self-Healing Demo
# Demonstrates LLM-powered code fixing with real Gemini API
# ============================================================================

import os
import sys

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from langchain_healer import LangChainHealer


def demo():
    print("=" * 60)
    print("  FC-001 | LangChain Self-Healing Engine - LIVE DEMO")
    print(f"  Provider: Google Gemini")
    print("=" * 60)

    # Create a temporary test file with a deliberate bug
    demo_file = os.path.join(os.path.dirname(__file__), "tests", "ui", "_demo_langchain_test.py")
    buggy_code = '''\
import pytest


class TestDemoLangChain:
    """Demo test with a timing bug."""

    def test_product_page_loads(self, page):
        """Verify product page displays correctly."""
        page.goto("http://localhost:3000/fashion-cube")
        # BUG: No wait, element might not be rendered yet
        title = page.locator(".product-card h3").first.text_content()
        assert title is not None, "Product title should be visible"
        assert len(title) > 0, "Product title should not be empty"

    def test_add_to_cart(self, authenticated_page):
        """Verify add to cart works."""
        authenticated_page.goto("http://localhost:3000/fashion-cube")
        # BUG: Clicking before page is ready
        authenticated_page.locator(".red_button").first.click()
        cart_count = authenticated_page.locator("#checkout_items").text_content()
        assert int(cart_count) > 0, "Cart should have items"
'''

    with open(demo_file, "w") as f:
        f.write(buggy_code)

    print(f"\n[1/3] Created buggy test file: {demo_file}")
    print("      Bug: No waits before interacting with elements\n")

    # Simulate a failure traceback
    fake_log = f'''\
FAILED tests/ui/_demo_langchain_test.py::TestDemoLangChain::test_product_page_loads
Traceback (most recent call last):
  File "{demo_file}", line 11, in test_product_page_loads
    title = page.locator(".product-card h3").first.text_content()
TimeoutError: Timeout 30000ms exceeded.
Call log:
  - waiting for locator(".product-card h3").first

During handling of the above exception, another exception occurred:
  playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded waiting for locator(".product-card h3")
'''

    print("[2/3] Sending failure to Gemini for analysis...\n")

    healer = LangChainHealer()
    result = healer.heal(fake_log)

    # Show the patched file
    print(f"\n[3/3] Patched file contents:")
    print("-" * 50)
    with open(demo_file, "r") as f:
        for i, line in enumerate(f.readlines(), 1):
            marker = " <<<< AI FIX" if "[AI-HEAL]" in line else ""
            print(f"  {i:>3}: {line.rstrip()}{marker}")
    print("-" * 50)

    # Cleanup
    os.remove(demo_file)
    print(f"\nCleaned up demo file.")
    print("=" * 60)


if __name__ == "__main__":
    demo()
