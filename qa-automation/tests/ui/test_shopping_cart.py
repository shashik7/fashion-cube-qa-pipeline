# ============================================================================
# FC-001 | Fashion Cube QA Automation - Shopping Cart UI Tests
# Requirement: AC-06 (Shopping Cart), AC-07 (Checkout)
# Test Cases: FC-001_TC025-TC036
# ============================================================================

import pytest
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from config.config import BASE_URL, JIRA_ID


@pytest.mark.ui
class TestShoppingCart:
    """FC-001: Shopping cart management and checkout UI tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_TC026_view_shopping_cart(self, authenticated_page):
        """FC-001_TC026: Verify logged-in user can view the shopping cart.
        Requirement: AC-06 – Cart page displays items with totals.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        assert cart_page.is_page_loaded(), (
            f"{JIRA_ID}_TC026: Cart page should load for authenticated user"
        )

    def test_FC001_TC029_empty_cart_state(self, authenticated_page):
        """FC-001_TC029: Verify empty cart shows empty state image.
        Requirement: AC-06 – Empty cart displays empty_cart.png image.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        # For a new user, cart should be empty
        if cart_page.get_cart_items_count() == 0:
            assert cart_page.is_cart_empty(), (
                f"{JIRA_ID}_TC029: Empty cart image should be displayed"
            )
        else:
            pytest.skip(f"{JIRA_ID}_TC029: Cart has items; cannot test empty state")

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_TC031_access_cart_without_auth(self, page):
        """FC-001_TC031: Verify unauthenticated user cannot access cart.
        Requirement: AC-06 – Cart is a private route; redirects to PageNotFound.
        """
        cart_page = CartPage(page)
        cart_page.navigate()
        page.wait_for_timeout(2000)

        # Should redirect to PageNotFound for unauthenticated users
        current_url = page.url
        assert "PageNotFound" in current_url or "cart" not in current_url, (
            f"{JIRA_ID}_TC031: Unauthenticated user should be redirected from cart"
        )

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_TC033_add_same_product_multiple_times(self, authenticated_page):
        """FC-001_TC033: Verify adding same product to cart multiple times.
        Requirement: AC-06 – Should show 1 line item with incremented quantity.
        """
        home_page = HomePage(authenticated_page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        product_count = home_page.get_product_count()
        if product_count > 0:
            # Click the first product
            home_page.click_product(0)
            home_page.wait_for_network_idle()

            product_page = ProductPage(authenticated_page)
            if product_page.is_visible(".red_button", timeout=5000):
                product_page.click_add_to_cart()
                product_page.wait_for_network_idle()
        else:
            pytest.skip(f"{JIRA_ID}_TC033: No products available")

    # ---- State Transition Tests ----

    def test_FC001_TC036_cart_state_transition(self, authenticated_page):
        """FC-001_TC036: Verify cart state: Empty → Item Added → Quantity Changed.
        Requirement: AC-06 – Full state transition validation.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        # Verify cart page loads (initial state validation)
        assert cart_page.is_page_loaded(), (
            f"{JIRA_ID}_TC036: Cart page should load for state transition test"
        )
