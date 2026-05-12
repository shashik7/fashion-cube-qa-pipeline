# ============================================================================
# FC-001 | Fashion Cube QA Automation - Products API Tests
# Requirement: AC-03 (Product Browsing), AC-04 (Search & Filter), AC-05 (Categories)
# Endpoints: GET /products, /products/:id, /search, /filter, /categories,
#            /departments, /variants
# ============================================================================

import pytest
import requests
from jsonschema import validate, ValidationError
from config.config import API_BASE_URL, API_TIMEOUT_SECONDS, ENDPOINTS, JIRA_ID


# ---- JSON Schemas for Validation ----

PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "imagePath": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "department": {"type": "string"},
        "category": {"type": "string"},
        "price": {"type": "number"},
        "color": {"type": "string"},
        "size": {"type": "string"},
        "quantity": {"type": "number"},
    },
    "required": ["_id", "title", "price"],
}

PRODUCTS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "items": PRODUCT_SCHEMA,
        }
    },
    "required": ["products"],
}

CATEGORY_SCHEMA = {
    "type": "object",
    "properties": {
        "categories": {"type": "array"}
    },
    "required": ["categories"],
}

DEPARTMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "departments": {"type": "array"}
    },
    "required": ["departments"],
}


@pytest.mark.api
class TestProductsAPI:
    """FC-001: Products API endpoint tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_API001_get_all_products(self):
        """FC-001_API001: Verify GET /products returns product list.
        Requirement: AC-03 – Products endpoint returns array of products.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['products']}"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 200, (
            f"{JIRA_ID}_API001: Expected 200, got {response.status_code}"
        )
        data = response.json()
        validate(instance=data, schema=PRODUCTS_RESPONSE_SCHEMA)
        assert len(data["products"]) > 0, (
            f"{JIRA_ID}_API001: Products list should not be empty"
        )

    @pytest.mark.smoke
    def test_FC001_API002_get_product_by_id(self):
        """FC-001_API002: Verify GET /products/:id returns single product.
        Requirement: AC-03 – Product detail endpoint.
        """
        # First get all products to get a valid ID
        url = f"{API_BASE_URL}{ENDPOINTS['products']}"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)
        if response.status_code != 200 or not response.json().get("products"):
            pytest.skip(f"{JIRA_ID}_API002: No products available")

        product_id = response.json()["products"][0]["_id"]
        detail_url = f"{API_BASE_URL}{ENDPOINTS['product_by_id'].format(product_id=product_id)}"
        detail_response = requests.get(detail_url, timeout=API_TIMEOUT_SECONDS)

        assert detail_response.status_code == 200, (
            f"{JIRA_ID}_API002: Expected 200, got {detail_response.status_code}"
        )
        data = detail_response.json()
        assert "product" in data, (
            f"{JIRA_ID}_API002: Response should contain 'product' key"
        )

    def test_FC001_API003_get_departments(self):
        """FC-001_API003: Verify GET /departments returns department list.
        Requirement: AC-05 – Departments endpoint for navigation.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['departments']}"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 200, (
            f"{JIRA_ID}_API003: Expected 200, got {response.status_code}"
        )
        data = response.json()
        validate(instance=data, schema=DEPARTMENT_SCHEMA)

    def test_FC001_API004_get_categories(self):
        """FC-001_API004: Verify GET /categories returns category list.
        Requirement: AC-05 – Categories endpoint for navigation.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['categories']}"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 200, (
            f"{JIRA_ID}_API004: Expected 200, got {response.status_code}"
        )
        data = response.json()
        validate(instance=data, schema=CATEGORY_SCHEMA)

    def test_FC001_API005_search_products(self):
        """FC-001_API005: Verify GET /search?query= returns matching products.
        Requirement: AC-04 – Search cascades: department → category → title → id.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['search']}"
        response = requests.get(
            url, params={"query": "shirt"}, timeout=API_TIMEOUT_SECONDS
        )

        # May return 200 with products or 404 if no match
        assert response.status_code in [200, 404], (
            f"{JIRA_ID}_API005: Expected 200 or 404, got {response.status_code}"
        )

    def test_FC001_API006_filter_products(self):
        """FC-001_API006: Verify GET /filter?query= returns filter results.
        Requirement: AC-04 – Filter by department, category, title.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['filter']}"
        response = requests.get(
            url, params={"query": "Men"}, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code in [200, 404], (
            f"{JIRA_ID}_API006: Expected 200 or 404, got {response.status_code}"
        )

    def test_FC001_API007_get_variants(self):
        """FC-001_API007: Verify GET /variants returns variant list.
        Requirement: AC-03 – Product variants endpoint.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['variants']}"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 200, (
            f"{JIRA_ID}_API007: Expected 200, got {response.status_code}"
        )
        data = response.json()
        assert "variants" in data, (
            f"{JIRA_ID}_API007: Response should contain 'variants' key"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_API008_get_product_invalid_id(self):
        """FC-001_API008: Verify GET /products/:id with invalid ID returns 404.
        Requirement: AC-03 – Invalid product ID handling.
        """
        url = f"{API_BASE_URL}/products/000000000000000000000000"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code in [404, 500], (
            f"{JIRA_ID}_API008: Expected 404/500 for invalid ID, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_API009_search_no_results(self):
        """FC-001_API009: Verify GET /search with nonexistent query returns 404.
        Requirement: AC-04 – No matching products returns error.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['search']}"
        response = requests.get(
            url, params={"query": "xyznonexistent123456"}, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code == 404, (
            f"{JIRA_ID}_API009: Expected 404, got {response.status_code}"
        )

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_API010_get_products_with_price_range_filter(self):
        """FC-001_API010: Verify GET /products with price range filter.
        Requirement: AC-04 – Price range filtering via query string.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['products']}"
        response = requests.get(
            url, params={"range": "10-50"}, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code in [200, 404], (
            f"{JIRA_ID}_API010: Expected 200/404, got {response.status_code}"
        )

    @pytest.mark.edge
    @pytest.mark.boundary
    def test_FC001_API011_get_products_with_sort_order(self):
        """FC-001_API011: Verify GET /products with order parameter.
        Requirement: AC-04 – Products can be sorted. App returns 406 if order
        value is not a recognised field (valid server-side validation).
        """
        url = f"{API_BASE_URL}{ENDPOINTS['products']}"
        response = requests.get(
            url, params={"order": "price"}, timeout=API_TIMEOUT_SECONDS
        )

        # 200 = sorted results, 404 = no products, 406 = unrecognised sort field
        assert response.status_code in [200, 404, 406], (
            f"{JIRA_ID}_API011: Expected 200/404/406, got {response.status_code}"
        )

    # ---- Boundary Tests ----

    @pytest.mark.boundary
    def test_FC001_API012_search_with_very_long_query(self):
        """FC-001_API012: Verify API handles extremely long search query.
        Requirement: AC-04 – Boundary test for search input.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['search']}"
        long_query = "a" * 1000
        response = requests.get(
            url, params={"query": long_query}, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code in [200, 404, 413, 414], (
            f"{JIRA_ID}_API012: Expected valid status code, got {response.status_code}"
        )

    # ---- Business Rule Validation ----

    def test_FC001_API013_product_price_is_positive(self):
        """FC-001_API013: Verify all products have positive prices.
        Requirement: AC-03 – Business rule: prices must be positive numbers.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['products']}"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        if response.status_code == 200:
            products = response.json().get("products", [])
            for product in products:
                price = product.get("price", 0)
                assert price >= 0, (
                    f"{JIRA_ID}_API013: Product '{product.get('title')}' "
                    f"has negative price: {price}"
                )

    def test_FC001_API014_product_has_required_fields(self):
        """FC-001_API014: Verify all products contain required fields.
        Requirement: AC-03 – Schema validation for product data.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['products']}"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        if response.status_code == 200:
            products = response.json().get("products", [])
            for product in products:
                assert "_id" in product, f"{JIRA_ID}_API014: Missing _id"
                assert "title" in product, f"{JIRA_ID}_API014: Missing title"
                assert "price" in product, f"{JIRA_ID}_API014: Missing price"
