# ============================================================================
# FC-001 | Fashion Cube QA Automation - Cart Page Object
# Requirement: AC-06 (Shopping Cart), AC-07 (Checkout)
# Locators derived from: src/views/Cart/Cart.js, src/views/Cart/CartItem.js
# ============================================================================

from pages.base_page import BasePage
from config.config import BASE_URL


class CartPage(BasePage):
    """FC-001: Page Object for the Shopping Cart Page."""

    # ---- Locators ----
    LOCATOR_CART_CONTAINER = ".shopping--cart"
    LOCATOR_CART_HEADING = ".shopping--cart .heading h2"
    LOCATOR_CART_ITEM = ".cart_item"
    LOCATOR_CART_ITEM_TITLE = ".cart_item .cart_item_title"
    LOCATOR_CART_ITEM_PRICE = ".cart_item .cart_item_price"
    LOCATOR_CART_ITEM_QTY = ".cart_item .cart_item_quantity span"
    LOCATOR_INCREASE_QTY_BUTTON = ".cart_item .fa-plus"
    LOCATOR_DECREASE_QTY_BUTTON = ".cart_item .fa-minus"
    LOCATOR_REMOVE_ITEM_BUTTON = ".cart_item .fa-trash"
    LOCATOR_SUBTOTAL = "text=SubTotal"
    LOCATOR_SHIPPING = "text=Shipping"
    LOCATOR_TAXES = "text=Taxes"
    LOCATOR_TOTAL = ".shopping--cart h3"
    LOCATOR_CHECKOUT_BUTTON = "button:has-text('Confirm Checkout')"
    LOCATOR_EMPTY_CART_IMAGE = ".shopping--cart img[src*='empty_cart']"
    LOCATOR_CART_BADGE = "#checkout_items"

    def __init__(self, page):
        super().__init__(page)
        self.url = f"{BASE_URL}/cart"

    def navigate(self):
        """FC-001: Navigate to the cart page."""
        super().navigate(self.url)

    def is_page_loaded(self):
        """FC-001: Check if the cart page is loaded."""
        return self.is_visible(self.LOCATOR_CART_CONTAINER)

    def get_cart_items_count(self):
        """FC-001: Get the number of cart items displayed."""
        return self.get_element_count(self.LOCATOR_CART_ITEM)

    def get_cart_item_titles(self):
        """FC-001: Get all cart item titles."""
        return self.get_all_texts(self.LOCATOR_CART_ITEM_TITLE)

    def get_item_quantity(self, index=0):
        """FC-001: Get the quantity of a specific cart item."""
        qty_elements = self.page.locator(self.LOCATOR_CART_ITEM_QTY)
        if qty_elements.count() > index:
            text = qty_elements.nth(index).text_content()
            return int(text) if text and text.isdigit() else 0
        return 0

    def increase_quantity(self, index=0):
        """FC-001: Increase quantity of a cart item."""
        buttons = self.page.locator(self.LOCATOR_INCREASE_QTY_BUTTON)
        if buttons.count() > index:
            buttons.nth(index).click()
            self.wait_for_network_idle()

    def decrease_quantity(self, index=0):
        """FC-001: Decrease quantity of a cart item."""
        buttons = self.page.locator(self.LOCATOR_DECREASE_QTY_BUTTON)
        if buttons.count() > index:
            buttons.nth(index).click()
            self.wait_for_network_idle()

    def get_total_text(self):
        """FC-001: Get the total price text."""
        return self.get_text(self.LOCATOR_TOTAL)

    def click_checkout(self):
        """FC-001: Click the Confirm Checkout button."""
        self.click(self.LOCATOR_CHECKOUT_BUTTON)

    def is_cart_empty(self):
        """FC-001: Check if the empty cart image is displayed."""
        return self.is_visible(self.LOCATOR_EMPTY_CART_IMAGE, timeout=5000)

    def get_cart_badge_count(self):
        """FC-001: Get the cart badge count from navbar."""
        if self.is_visible(self.LOCATOR_CART_BADGE, timeout=3000):
            text = self.get_text(self.LOCATOR_CART_BADGE)
            return int(text) if text and text.isdigit() else 0
        return 0
