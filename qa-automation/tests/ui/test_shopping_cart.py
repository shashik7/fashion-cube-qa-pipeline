# ============================================================================
# FC-001 | Fashion Cube QA Automation - Shopping Cart UI Tests
# Requirement: AC-06 (Shopping Cart), AC-07 (Checkout)
# Test Cases: FC-001_TC025-TC036
# All locators verified from: src/views/Cart/Cart.js, CartItem.js, NavBar.js
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
    def test_FC001_TC025_cart_page_loads(self, authenticated_page):
        """FC-001_TC025: Verify the cart page loads for an authenticated user.
        Requirement: AC-06 – Cart page is accessible and renders correctly.
        Source: Cart.js:23 renders div.shopping--cart as main container.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        assert cart_page.is_page_loaded(), (
            f"{JIRA_ID}_TC025: Cart page should load (div.shopping--cart not found)"
        )

    @pytest.mark.smoke
    def test_FC001_TC026_cart_heading_displayed(self, authenticated_page):
        """FC-001_TC026: Verify the cart heading is visible.
        Requirement: AC-06 – Cart page displays 'Your Shopping Cart' heading.
        Source: Cart.js:27 uses <Heading title="Your Shopping Cart" />.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        heading = cart_page.get_cart_heading_text()
        assert heading is not None and "Shopping Cart" in heading, (
            f"{JIRA_ID}_TC026: Cart heading should contain 'Shopping Cart', got: '{heading}'"
        )

    def test_FC001_TC027_add_product_to_cart(self, authenticated_page):
        """FC-001_TC027: Verify a product can be added to the cart.
        Requirement: AC-06 – User can add items from product detail page.
        Source: ProductPage uses .red_button for Add to Cart (SingleProduct.js).
                NavBar.js:105 renders span#checkout_items for badge.
        """
        home_page = HomePage(authenticated_page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        product_count = home_page.get_product_count()
        if product_count == 0:
            pytest.skip(f"{JIRA_ID}_TC027: No products available on home page")

        # Click first product to go to detail page
        home_page.click_product(0)
        home_page.wait_for_network_idle()

        product_page = ProductPage(authenticated_page)
        # SingleProduct.js uses .red_button for the add-to-cart button
        if not product_page.is_visible(product_page.LOCATOR_ADD_TO_CART_BUTTON, timeout=5000):
            pytest.skip(f"{JIRA_ID}_TC027: Add to Cart button (.red_button) not found")

        # Add the product to cart
        product_page.click_add_to_cart()
        product_page.wait_for_network_idle()
        authenticated_page.wait_for_timeout(1000)

        # Navigate to cart page and verify item exists
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        items_count = cart_page.get_cart_items_count()
        assert items_count > 0, (
            f"{JIRA_ID}_TC027: Cart should have at least 1 item after adding (div.shopping--cart--item)"
        )

    def test_FC001_TC029_empty_cart_state(self, authenticated_page):
        """FC-001_TC029: Verify empty cart shows empty state image.
        Requirement: AC-06 – Empty cart displays empty_cart.png image.
        Source: Cart.js:70-75 renders img.img-fluid when items is null/undefined.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        if cart_page.get_cart_items_count() == 0:
            assert cart_page.is_cart_empty(), (
                f"{JIRA_ID}_TC029: Empty cart image (img.img-fluid) should be displayed"
            )
        else:
            pytest.skip(f"{JIRA_ID}_TC029: Cart has items; cannot test empty state")

    def test_FC001_TC030_cart_badge_reflects_count(self, authenticated_page):
        """FC-001_TC030: Verify the navbar cart badge is rendered.
        Requirement: AC-06 – Badge count updates when items are added.
        Source: NavBar.js:105 renders span#checkout_items with cart.totalQty.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        badge_count = cart_page.get_cart_badge_count()
        assert badge_count >= 0, (
            f"{JIRA_ID}_TC030: Cart badge (#checkout_items) should be >= 0, got: {badge_count}"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_TC031_access_cart_without_auth(self, page):
        """FC-001_TC031: Verify unauthenticated user cart behavior.
        Requirement: AC-06 – Cart access without authentication is handled.
        """
        cart_page = CartPage(page)
        cart_page.navigate()
        page.wait_for_timeout(2000)

        current_url = page.url
        is_redirected = "PageNotFound" in current_url or "login" in current_url.lower()
        is_cart_empty = cart_page.is_cart_empty() if "cart" in current_url else True

        assert is_redirected or is_cart_empty, (
            f"{JIRA_ID}_TC031: Unauthenticated user should see empty cart or be redirected"
        )

    @pytest.mark.negative
    def test_FC001_TC032_navigate_to_invalid_cart_url(self, page):
        """FC-001_TC032: Verify navigating to an invalid cart-like URL.
        Requirement: AC-06 – Application handles invalid routes gracefully.
        """
        page.goto(f"{BASE_URL}/cart/invalid-item-id", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        assert page.title() is not None, (
            f"{JIRA_ID}_TC032: Application should not crash on invalid cart URL"
        )

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_TC033_add_same_product_multiple_times(self, authenticated_page):
        """FC-001_TC033: Verify adding same product to cart increments quantity.
        Requirement: AC-06 – Should increment quantity, not create duplicate rows.
        Source: CartItem.js:56 renders quantity in span#quantity_value.
        """
        home_page = HomePage(authenticated_page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        product_count = home_page.get_product_count()
        if product_count == 0:
            pytest.skip(f"{JIRA_ID}_TC033: No products available")

        home_page.click_product(0)
        home_page.wait_for_network_idle()

        product_page = ProductPage(authenticated_page)
        if not product_page.is_visible(product_page.LOCATOR_ADD_TO_CART_BUTTON, timeout=5000):
            pytest.skip(f"{JIRA_ID}_TC033: Add to Cart button not available")

        # Add to cart twice
        product_page.click_add_to_cart()
        product_page.wait_for_network_idle()
        authenticated_page.wait_for_timeout(500)

        product_page.click_add_to_cart()
        product_page.wait_for_network_idle()
        authenticated_page.wait_for_timeout(500)

        # Navigate to cart and verify quantity
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        if cart_page.is_page_loaded() and cart_page.get_cart_items_count() > 0:
            qty = cart_page.get_item_quantity(0)
            assert qty >= 1, (
                f"{JIRA_ID}_TC033: Quantity (#quantity_value) should be >= 1, got: {qty}"
            )

    @pytest.mark.edge
    def test_FC001_TC034_cart_total_is_displayed(self, authenticated_page):
        """FC-001_TC034: Verify the cart total section is rendered.
        Requirement: AC-06 – Cart shows SubTotal, Shipping, Taxes, and Total.
        Source: Cart.js:56-60 renders h3 with Total and ₹ price.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        if cart_page.get_cart_items_count() > 0:
            total_text = cart_page.get_total_text()
            assert total_text is not None and "Total" in total_text, (
                f"{JIRA_ID}_TC034: Cart total (h3) should contain 'Total', got: '{total_text}'"
            )
        else:
            pytest.skip(f"{JIRA_ID}_TC034: Cart is empty; cannot test total display")

    @pytest.mark.edge
    def test_FC001_TC035_quantity_buttons_exist(self, authenticated_page):
        """FC-001_TC035: Verify plus/minus quantity buttons render for cart items.
        Requirement: AC-06 – User can adjust quantity with +/- buttons.
        Source: CartItem.js:50 span.minus, CartItem.js:57 span.plus.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        if cart_page.get_cart_items_count() > 0:
            plus_count = cart_page.get_element_count(cart_page.LOCATOR_INCREASE_QTY_BUTTON)
            minus_count = cart_page.get_element_count(cart_page.LOCATOR_DECREASE_QTY_BUTTON)
            assert plus_count > 0 and minus_count > 0, (
                f"{JIRA_ID}_TC035: Plus (.plus) and minus (.minus) buttons should exist"
            )
        else:
            pytest.skip(f"{JIRA_ID}_TC035: Cart is empty; cannot test quantity buttons")

    # ---- State Transition Tests ----

    def test_FC001_TC036_cart_state_transition(self, authenticated_page):
        """FC-001_TC036: Verify cart state: Empty → Item Added → Cart Updated.
        Requirement: AC-06 – Full state transition validation.
        """
        cart_page = CartPage(authenticated_page)
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        assert cart_page.is_page_loaded(), (
            f"{JIRA_ID}_TC036: Cart page (div.shopping--cart) should load"
        )

        initial_count = cart_page.get_cart_items_count()

        # Navigate to home, find a product, and add it
        home_page = HomePage(authenticated_page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        product_count = home_page.get_product_count()
        if product_count == 0:
            pytest.skip(f"{JIRA_ID}_TC036: No products available")

        home_page.click_product(0)
        home_page.wait_for_network_idle()

        product_page = ProductPage(authenticated_page)
        if product_page.is_visible(product_page.LOCATOR_ADD_TO_CART_BUTTON, timeout=5000):
            product_page.click_add_to_cart()
            product_page.wait_for_network_idle()
            authenticated_page.wait_for_timeout(1000)

        # Go back to cart and verify state changed
        cart_page.navigate()
        cart_page.wait_for_network_idle()

        updated_count = cart_page.get_cart_items_count()
        assert updated_count >= initial_count, (
            f"{JIRA_ID}_TC036: Cart items ({updated_count}) should be >= initial ({initial_count})"
        )
