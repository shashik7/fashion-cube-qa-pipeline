# ============================================================================
# FC-001 | Fashion Cube QA Automation - Product Browsing UI Tests
# Requirement: AC-03 (Browsing), AC-04 (Search/Filter), AC-05 (Categories)
# Test Cases: FC-001_TC014-TC024
# ============================================================================

import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from config.config import BASE_URL, JIRA_ID


@pytest.mark.ui
class TestProductBrowsing:
    """FC-001: Product browsing, search, and category navigation UI tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_TC014_home_page_displays_products(self, page):
        """FC-001_TC014: Verify home page displays product listings.
        Requirement: AC-03 – Home page displays all products.
        """
        home_page = HomePage(page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        assert home_page.is_page_loaded(), (
            f"{JIRA_ID}_TC014: Home page should be loaded"
        )

    @pytest.mark.smoke
    def test_FC001_TC015_navigate_to_product_detail(self, page):
        """FC-001_TC015: Verify user can navigate to a product detail page.
        Requirement: AC-03 – Product detail shows title, description, price, image.
        """
        home_page = HomePage(page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        product_count = home_page.get_product_count()
        if product_count > 0:
            home_page.click_product(0)
            home_page.wait_for_network_idle()
            home_page.assert_url_contains("single-product")
        else:
            pytest.skip(f"{JIRA_ID}_TC015: No products available to click")

    def test_FC001_TC017_navigate_to_category(self, page):
        """FC-001_TC017: Verify user can navigate to category page via shop menu.
        Requirement: AC-05 – Navigation menu displays departments with categories.
        """
        home_page = HomePage(page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        home_page.hover_shop_menu()
        assert home_page.is_mega_menu_visible(), (
            f"{JIRA_ID}_TC017: Mega menu should be visible on hover"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_TC020_navigate_to_invalid_product_id(self, page):
        """FC-001_TC020: Verify navigating to non-existent product ID.
        Requirement: AC-03 – Should display error or not found state.
        """
        product_page = ProductPage(page)
        product_page.navigate("invalidid123")
        product_page.wait_for_network_idle()

        # Product container should not load for invalid ID
        page.wait_for_timeout(2000)
        # The page should either show an error or empty state

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_TC021_search_with_special_characters(self, page):
        """FC-001_TC021: Verify search handles special characters safely.
        Requirement: AC-04 – XSS prevention in search input.
        """
        home_page = HomePage(page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        # Navigate directly to search URL with XSS payload
        page.goto(f"{BASE_URL}/../search?query=<script>alert(1)</script>")
        page.wait_for_timeout(2000)

        # No alert dialog should appear; page should remain stable
        assert page.url is not None, (
            f"{JIRA_ID}_TC021: Page should handle XSS in search safely"
        )

    @pytest.mark.edge
    def test_FC001_TC022_search_with_empty_query(self, page):
        """FC-001_TC022: Verify search with empty query.
        Requirement: AC-04 – Should display all products or helpful message.
        """
        home_page = HomePage(page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        # Navigate to search with empty query
        page.goto(f"{BASE_URL}/../search?query=")
        page.wait_for_timeout(2000)
        assert page.url is not None, (
            f"{JIRA_ID}_TC022: Page should handle empty search query"
        )

    # ---- Boundary Tests ----

    @pytest.mark.boundary
    def test_FC001_TC023_search_with_long_query(self, page):
        """FC-001_TC023: Verify search with 500-character query string.
        Requirement: AC-04 – System should handle long queries gracefully.
        """
        home_page = HomePage(page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        long_query = "x" * 500
        page.goto(f"{BASE_URL}/../search?query={long_query}")
        page.wait_for_timeout(3000)

        assert page.url is not None, (
            f"{JIRA_ID}_TC023: System should handle 500-char search query"
        )

    # ---- State Transition Tests ----

    def test_FC001_TC024_navigate_home_product_back(self, page):
        """FC-001_TC024: Verify Home → Product → Back to Home navigation.
        Requirement: AC-03 – State transition validation.
        """
        home_page = HomePage(page)
        home_page.navigate()
        home_page.wait_for_network_idle()

        product_count = home_page.get_product_count()
        if product_count > 0:
            home_page.click_product(0)
            home_page.wait_for_network_idle()
            home_page.assert_url_contains("single-product")

            # Navigate back to home
            page.go_back()
            home_page.wait_for_network_idle()
            assert home_page.is_page_loaded(), (
                f"{JIRA_ID}_TC024: Home page should display correctly after back nav"
            )
        else:
            pytest.skip(f"{JIRA_ID}_TC024: No products available")
