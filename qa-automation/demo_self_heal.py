# ============================================================================
# FC-001 | Self-Healing Demo
# Demonstrates the AIFailureAnalyzer fixing test scripts automatically
# ============================================================================

import os
import tempfile
import shutil
from ai_failure_analyzer import AIFailureAnalyzer


def demo_timing_fix():
    """Demo: Auto-fix a timing issue by injecting a wait."""
    print("\n" + "=" * 70)
    print("  DEMO 1: Timing Issue – Auto-Inject Wait")
    print("=" * 70)

    # Create a temporary test file that simulates a real test
    demo_test = os.path.join(os.path.dirname(__file__), "tests", "ui", "_demo_timing_test.py")
    original_code = '''\
import pytest

class TestDemoTiming:
    def test_page_load(self, page):
        page.goto("http://localhost:3000")
        assert page.locator(".product-card").is_visible()
        assert page.title() == "Fashion Cube"
'''
    with open(demo_test, 'w') as f:
        f.write(original_code)

    print(f"\n📄 Created demo test file: {demo_test}")
    print(f"   Original line 6: assert page.locator('.product-card').is_visible()")

    # Simulate a traceback that points at line 6 of that file
    fake_log = f'''\
FAILED tests/ui/_demo_timing_test.py::TestDemoTiming::test_page_load
Traceback (most recent call last):
  File "{demo_test}", line 6, in test_page_load
    assert page.locator(".product-card").is_visible()
TimeoutError: Timeout 30000ms exceeded waiting for selector ".product-card"
'''

    analyzer = AIFailureAnalyzer()

    # Step 1: Analyze
    result = analyzer.analyze(fake_log)
    analyzer.print_analysis(result)

    # Step 2: Self-Heal
    heal_result = analyzer.self_heal(fake_log)
    print(f"✨ Healing Result: [{heal_result['status']}] {heal_result['message']}")

    # Step 3: Show the patched file
    with open(demo_test, 'r') as f:
        patched = f.read()
    print(f"\n📄 Patched file contents:")
    print("-" * 40)
    for i, line in enumerate(patched.splitlines(), 1):
        marker = " <<<< INJECTED" if "[AI-HEAL]" in line else ""
        print(f"  {i:>3}: {line}{marker}")
    print("-" * 40)

    # Cleanup
    os.remove(demo_test)
    print(f"\n🧹 Cleaned up demo file.")


def demo_locator_fix():
    """Demo: Auto-flag a broken locator for review."""
    print("\n" + "=" * 70)
    print("  DEMO 2: Locator Issue – Auto-Flag for Review")
    print("=" * 70)

    demo_page = os.path.join(os.path.dirname(__file__), "pages", "_demo_page.py")
    original_code = '''\
from pages.base_page import BasePage

class DemoPage(BasePage):
    LOCATOR_PRODUCT_CARD = ".product-card"
    LOCATOR_ADD_TO_CART = ".btn-add-cart"
    LOCATOR_PRICE_TAG = ".price-label"

    def click_add(self):
        self.click(self.LOCATOR_ADD_TO_CART)
'''
    with open(demo_page, 'w') as f:
        f.write(original_code)

    print(f"\n📄 Created demo page object: {demo_page}")
    print(f"   Original line 5: LOCATOR_ADD_TO_CART = '.btn-add-cart'")

    fake_log = f'''\
FAILED tests/ui/test_demo.py::TestDemo::test_add_to_cart
Traceback (most recent call last):
  File "{demo_page}", line 5, in click_add
    LOCATOR_ADD_TO_CART = ".btn-add-cart"
Element not found: selector ".btn-add-cart" not visible on the page
NoSuchElementException: could not find element matching .btn-add-cart
'''

    analyzer = AIFailureAnalyzer()

    # Step 1: Analyze
    result = analyzer.analyze(fake_log)
    analyzer.print_analysis(result)

    # Step 2: Self-Heal
    heal_result = analyzer.self_heal(fake_log)
    print(f"✨ Healing Result: [{heal_result['status']}] {heal_result['message']}")

    # Step 3: Show the patched file
    with open(demo_page, 'r') as f:
        patched = f.read()
    print(f"\n📄 Patched file contents:")
    print("-" * 40)
    for i, line in enumerate(patched.splitlines(), 1):
        marker = " <<<< FLAGGED" if "[AI-HEAL]" in line else ""
        print(f"  {i:>3}: {line}{marker}")
    print("-" * 40)

    # Cleanup
    os.remove(demo_page)
    print(f"\n🧹 Cleaned up demo file.")


if __name__ == "__main__":
    print("=" * 70)
    print("  FC-001 | AIFailureAnalyzer – Self-Healing Engine Demo")
    print("=" * 70)

    demo_timing_fix()
    demo_locator_fix()

    print("\n" + "=" * 70)
    print("  ✅ DEMO COMPLETE")
    print("  Usage in production:")
    print("    Analyze only:  python ai_failure_analyzer.py failure.log")
    print("    Auto-fix:      python ai_failure_analyzer.py --fix failure.log")
    print("=" * 70)
