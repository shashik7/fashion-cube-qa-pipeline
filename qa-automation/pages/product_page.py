# ============================================================================
# FC-001 | Fashion Cube QA Automation - Product Detail Page Object
# Requirement: AC-03 – Product Detail View
# Locators derived from: src/views/Product/SingleProduct.js
# ============================================================================

from pages.base_page import BasePage
from config.config import BASE_URL


class ProductPage(BasePage):
    """FC-001: Page Object for the Single Product Detail Page."""

    # ---- Locators ----
    LOCATOR_PRODUCT_CONTAINER = ".single_product_container"
    LOCATOR_PRODUCT_IMAGE = ".single_product_container .image_selected img"
    LOCATOR_PRODUCT_TITLE = ".product_details .product_details_title"
    LOCATOR_PRODUCT_PRICE = ".product_details .product_price"
    LOCATOR_PRODUCT_DESCRIPTION = ".product_details .product_description"
    LOCATOR_ADD_TO_CART_BUTTON = ".product_details .red_button"
    LOCATOR_QUANTITY_INPUT = ".product_details .quantity_input"
    LOCATOR_COLOR_OPTIONS = ".product_details .product_color"
    LOCATOR_SIZE_OPTIONS = ".product_details .product_size"
    LOCATOR_BREADCRUMB = ".breadcrumbs"
    LOCATOR_RELATED_PRODUCTS = ".product_slider_container"

    def __init__(self, page):
        super().__init__(page)

    def navigate(self, product_id):
        """FC-001: Navigate to a specific product detail page."""
        url = f"{BASE_URL}/single-product/{product_id}"
        super().navigate(url)

    def is_page_loaded(self):
        """FC-001: Check if the product detail page is loaded."""
        return self.is_visible(self.LOCATOR_PRODUCT_CONTAINER)

    def get_product_title(self):
        """FC-001: Get the product title."""
        return self.get_text(self.LOCATOR_PRODUCT_TITLE)

    def get_product_price(self):
        """FC-001: Get the product price text."""
        return self.get_text(self.LOCATOR_PRODUCT_PRICE)

    def get_product_description(self):
        """FC-001: Get the product description."""
        return self.get_text(self.LOCATOR_PRODUCT_DESCRIPTION)

    def is_product_image_visible(self):
        """FC-001: Check if the product image is visible."""
        return self.is_visible(self.LOCATOR_PRODUCT_IMAGE)

    def click_add_to_cart(self):
        """FC-001: Click the Add to Cart button."""
        self.click(self.LOCATOR_ADD_TO_CART_BUTTON)

    def select_color(self, color):
        """FC-001: Select a product color variant."""
        self.click(f"{self.LOCATOR_COLOR_OPTIONS} [data-color='{color}']")

    def select_size(self, size):
        """FC-001: Select a product size variant."""
        self.click(f"{self.LOCATOR_SIZE_OPTIONS} [data-size='{size}']")

    def get_quantity(self):
        """FC-001: Get the current quantity value."""
        return self.get_input_value(self.LOCATOR_QUANTITY_INPUT)

    def set_quantity(self, qty):
        """FC-001: Set the quantity input value."""
        self.fill(self.LOCATOR_QUANTITY_INPUT, str(qty))

    def has_related_products(self):
        """FC-001: Check if related products section exists."""
        return self.is_visible(self.LOCATOR_RELATED_PRODUCTS, timeout=5000)
