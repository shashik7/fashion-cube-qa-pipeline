# ============================================================================
# FC-001 | Fashion Cube QA Automation - Home Page Object
# Requirement: AC-03 (Product Browsing), AC-04 (Search & Filter), AC-05 (Categories)
# Locators derived from: src/views/Home/Home.js, src/components/NavBar/NavBar.js
# ============================================================================

from pages.base_page import BasePage
from config.config import BASE_URL


class HomePage(BasePage):
    """FC-001: Page Object for the Home Page."""

    # ---- Locators ----
    LOCATOR_NAVBAR = ".main_nav_container"
    LOCATOR_LOGO = ".logo_container a"
    LOCATOR_NAV_MENU = ".navbar_menu"
    LOCATOR_HOME_LINK = ".navbar_menu li:nth-child(1) a"
    LOCATOR_SHOP_DROPDOWN = ".mega-drop-down > a"
    LOCATOR_MEGA_MENU = ".mega-menu"
    LOCATOR_MEGA_MENU_CONTENT = ".mega-menu-content"
    LOCATOR_DEPARTMENT_TITLE = ".mega-menu-content h5"
    LOCATOR_CATEGORY_LINKS = ".mega-menu-content .stander li a"
    LOCATOR_SEARCH_ICON = ".navbar_user li:nth-child(1) a"
    LOCATOR_USER_ICON = ".navbar_user li:nth-child(2) a"
    LOCATOR_CART_ICON = ".checkout a"
    LOCATOR_CART_BADGE = "#checkout_items"
    LOCATOR_PRODUCTS_SECTION = ".product_slider_container"
    LOCATOR_SINGLE_PRODUCT = ".product-item"
    LOCATOR_PRODUCT_TITLE = ".product_name a"
    LOCATOR_PRODUCT_PRICE = ".product_price"
    LOCATOR_PRODUCT_IMAGE = ".product-item img"
    LOCATOR_BEST_SELLERS = ".product_slider_container"
    LOCATOR_NEW_ARRIVALS = ".product_slider_container"
    LOCATOR_SLIDER = ".main_slider"
    LOCATOR_BANNER = ".banner_2_background"
    LOCATOR_BENEFIT_SECTION = ".benefit_row"
    LOCATOR_ADVERTISEMENT = ".avid_background"
    LOCATOR_FOOTER = ".footer_background"

    def __init__(self, page):
        super().__init__(page)
        self.url = BASE_URL

    def navigate(self):
        """FC-001: Navigate to the home page."""
        super().navigate(self.url)

    def is_page_loaded(self):
        """FC-001: Check if the home page is loaded."""
        return self.is_visible(self.LOCATOR_NAVBAR)

    def get_product_count(self):
        """FC-001: Get the number of products displayed."""
        return self.get_element_count(self.LOCATOR_SINGLE_PRODUCT)

    def get_product_titles(self):
        """FC-001: Get all product titles displayed."""
        return self.get_all_texts(self.LOCATOR_PRODUCT_TITLE)

    def click_product(self, index=0):
        """FC-001: Click on a product by index."""
        products = self.page.locator(self.LOCATOR_SINGLE_PRODUCT)
        if products.count() > index:
            products.nth(index).click()
        else:
            raise AssertionError(
                f"FC-001: Product index {index} out of range (total: {products.count()})"
            )

    def click_product_by_title(self, title):
        """FC-001: Click on a product by title."""
        self.click(f"text={title}")

    def hover_shop_menu(self):
        """FC-001: Hover over the Shop dropdown to reveal mega menu."""
        self.hover(self.LOCATOR_SHOP_DROPDOWN)

    def is_mega_menu_visible(self):
        """FC-001: Check if the mega menu is visible."""
        return self.is_visible(self.LOCATOR_MEGA_MENU, timeout=3000)

    def get_department_names(self):
        """FC-001: Get all department names from the mega menu."""
        self.hover_shop_menu()
        return self.get_all_texts(self.LOCATOR_DEPARTMENT_TITLE)

    def click_category(self, category_text):
        """FC-001: Click a category link in the mega menu."""
        self.hover_shop_menu()
        self.click(f".stander li a[href*='{category_text}']")

    def open_cart_modal(self):
        """FC-001: Open the cart modal by clicking cart icon."""
        self.click(self.LOCATOR_CART_ICON)

    def get_cart_badge_count(self):
        """FC-001: Get the cart badge item count."""
        if self.is_visible(self.LOCATOR_CART_BADGE, timeout=3000):
            text = self.get_text(self.LOCATOR_CART_BADGE)
            return int(text) if text and text.isdigit() else 0
        return 0

    def is_slider_displayed(self):
        """FC-001: Check if the main slider is displayed."""
        return self.is_visible(self.LOCATOR_SLIDER, timeout=5000)

    def is_footer_displayed(self):
        """FC-001: Check if the footer is displayed."""
        return self.is_visible(self.LOCATOR_FOOTER)

    def click_home_link(self):
        """FC-001: Click the Home navigation link."""
        self.click(self.LOCATOR_HOME_LINK)

    def click_logo(self):
        """FC-001: Click the FashionCube logo to go home."""
        self.click(self.LOCATOR_LOGO)
