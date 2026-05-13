# ============================================================================
# FC-001 | Fashion Cube QA Automation - Cart Page Object
# Requirement: AC-06 (Shopping Cart), AC-07 (Checkout)
# Locators derived from: src/views/Cart/Cart.js, src/views/Cart/CartItem.js
# ============================================================================
# SOURCE VERIFICATION:
#   Cart.js:23       → div.shopping--cart (main container)
#   Cart.js:27       → <Heading title="Your Shopping Cart" /> → .section_title h2
#   Cart.js:56-60    → h3 (total price)
#   Cart.js:64-66    → Button variant="danger" text="Confirm Checkout"
#   Cart.js:70-75    → img.img-fluid (empty cart image, src=empty_cart.png)
#   CartItem.js:15   → div.shopping--cart--item (each cart item row)
#   CartItem.js:27   → div.basket--item--title (item name)
#   CartItem.js:33   → div.basket--item--quantity span (displayed qty)
#   CartItem.js:39   → div.basket--item--price span (item price)
#   CartItem.js:50   → span.minus > i.fa.fa-minus (decrease qty)
#   CartItem.js:56   → span#quantity_value (editable qty)
#   CartItem.js:57   → span.plus > i.fa.fa-plus (increase qty)
#   NavBar.js:105    → span#checkout_items (cart badge in navbar)
# ============================================================================

from pages.base_page import BasePage
from config.config import BASE_URL


class CartPage(BasePage):
    """FC-001: Page Object for the Shopping Cart Page."""

    # ---- Locators (verified from React source) ----
    # Cart.js:23 – main wrapper
    LOCATOR_CART_CONTAINER = ".shopping--cart"
    # Heading component renders: div.section_title > h2
    LOCATOR_CART_HEADING = ".section_title h2"
    # CartItem.js:15 – each item row
    LOCATOR_CART_ITEM = ".shopping--cart--item"
    # CartItem.js:27 – item title
    LOCATOR_CART_ITEM_TITLE = ".basket--item--title"
    # CartItem.js:39-43 – item price
    LOCATOR_CART_ITEM_PRICE = ".basket--item--price span"
    # CartItem.js:33-36 – displayed quantity text
    LOCATOR_CART_ITEM_QTY_TEXT = ".basket--item--quantity span"
    # CartItem.js:56 – editable quantity value in quantity selector
    LOCATOR_CART_ITEM_QTY = "#quantity_value"
    # CartItem.js:57-62 – increase quantity button
    LOCATOR_INCREASE_QTY_BUTTON = ".quantity_selector .plus"
    # CartItem.js:50-54 – decrease quantity button
    LOCATOR_DECREASE_QTY_BUTTON = ".quantity_selector .minus"
    # Cart.js:42-43 – SubTotal text
    LOCATOR_SUBTOTAL = "text=SubTotal"
    # Cart.js:46 – Shipping text
    LOCATOR_SHIPPING = "text=Shipping"
    # Cart.js:50 – Taxes text
    LOCATOR_TAXES = "text=Taxes"
    # Cart.js:56-60 – Total h3
    LOCATOR_TOTAL = ".shopping--cart h3"
    # Cart.js:64-66 – Confirm Checkout button (react-bootstrap Button)
    LOCATOR_CHECKOUT_BUTTON = "button:has-text('Confirm Checkout')"
    # Cart.js:70-75 – Empty cart image (img with src containing empty_cart)
    LOCATOR_EMPTY_CART_IMAGE = ".shopping--cart img.img-fluid"
    # NavBar.js:105 – Cart badge count in navbar
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

    def get_cart_heading_text(self):
        """FC-001: Get the cart heading text ('Your Shopping Cart')."""
        return self.get_text(self.LOCATOR_CART_HEADING)

    def get_cart_items_count(self):
        """FC-001: Get the number of cart item rows displayed."""
        return self.get_element_count(self.LOCATOR_CART_ITEM)

    def get_cart_item_titles(self):
        """FC-001: Get all cart item titles."""
        return self.get_all_texts(self.LOCATOR_CART_ITEM_TITLE)

    def get_item_quantity(self, index=0):
        """FC-001: Get the quantity of a specific cart item from #quantity_value."""
        qty_elements = self.page.locator(self.LOCATOR_CART_ITEM_QTY)
        if qty_elements.count() > index:
            text = qty_elements.nth(index).text_content().strip()
            return int(text) if text and text.isdigit() else 0
        return 0

    def increase_quantity(self, index=0):
        """FC-001: Click the plus button to increase quantity of a cart item."""
        buttons = self.page.locator(self.LOCATOR_INCREASE_QTY_BUTTON)
        if buttons.count() > index:
            buttons.nth(index).click()
            self.wait_for_network_idle()

    def decrease_quantity(self, index=0):
        """FC-001: Click the minus button to decrease quantity of a cart item."""
        buttons = self.page.locator(self.LOCATOR_DECREASE_QTY_BUTTON)
        if buttons.count() > index:
            buttons.nth(index).click()
            self.wait_for_network_idle()

    def get_total_text(self):
        """FC-001: Get the total price text from the h3 element."""
        return self.get_text(self.LOCATOR_TOTAL)

    def click_checkout(self):
        """FC-001: Click the Confirm Checkout button."""
        self.click(self.LOCATOR_CHECKOUT_BUTTON)

    def is_cart_empty(self):
        """FC-001: Check if the empty cart image is displayed.
        Cart.js:70-75 renders img.img-fluid when items is null/undefined.
        """
        return self.is_visible(self.LOCATOR_EMPTY_CART_IMAGE, timeout=5000)

    def get_cart_badge_count(self):
        """FC-001: Get the cart badge count from navbar (NavBar.js:105)."""
        if self.is_visible(self.LOCATOR_CART_BADGE, timeout=3000):
            text = self.get_text(self.LOCATOR_CART_BADGE)
            return int(text) if text and text.isdigit() else 0
        return 0
