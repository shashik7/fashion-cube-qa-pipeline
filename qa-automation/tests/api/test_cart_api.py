# ============================================================================
# FC-001 | Fashion Cube QA Automation - Cart API Tests
# Requirement: AC-06 (Shopping Cart), AC-07 (Checkout)
# Endpoints: GET/POST/PUT /users/:userId/cart, GET /checkout/:cartId
# ============================================================================

import pytest
import requests
from jsonschema import validate
from config.config import (
    API_BASE_URL,
    API_TIMEOUT_SECONDS,
    ENDPOINTS,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    JIRA_ID,
)


# ---- JSON Schemas ----

CART_SCHEMA = {
    "type": "object",
    "properties": {
        "cart": {
            "type": "object",
            "properties": {
                "_id": {"type": "string"},
                "items": {"type": "object"},
                "totalQty": {"type": "number"},
                "totalPrice": {"type": "number"},
                "userId": {"type": "string"},
            },
        }
    },
}


@pytest.fixture
def auth_token():
    """FC-001: Get authentication token for cart API tests."""
    url = f"{API_BASE_URL}{ENDPOINTS['login']}"
    payload = {
        "credential": {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)
        if response.status_code == 201:
            data = response.json()
            return {
                "token": data["user_token"]["token"],
                "user_id": data["user_token"]["user_id"],
            }
    except Exception:
        pass
    pytest.skip(f"{JIRA_ID}: Could not obtain auth token")


@pytest.fixture
def auth_headers(auth_token):
    """FC-001: Build authorization headers."""
    return {"authorization": auth_token["token"]}


@pytest.fixture
def valid_product_id():
    """FC-001: Get a valid product ID for cart tests."""
    url = f"{API_BASE_URL}{ENDPOINTS['products']}"
    try:
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)
        if response.status_code == 200:
            products = response.json().get("products", [])
            if products:
                return products[0]["_id"]
    except Exception:
        pass
    pytest.skip(f"{JIRA_ID}: No valid product ID available")


@pytest.mark.api
class TestCartAPI:
    """FC-001: Cart API endpoint tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_CART_API001_get_cart(self, auth_token, auth_headers):
        """FC-001_CART_API001: Verify GET /users/:userId/cart returns cart.
        Requirement: AC-06 – Authenticated user can view cart.
        """
        user_id = auth_token["user_id"]
        url = f"{API_BASE_URL}{ENDPOINTS['cart'].format(user_id=user_id)}"
        response = requests.get(
            url, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )

        # 200 = cart exists, 404 = no cart yet (both are valid)
        assert response.status_code in [200, 404], (
            f"{JIRA_ID}_CART_API001: Expected 200/404, got {response.status_code}"
        )
        if response.status_code == 200:
            data = response.json()
            assert "cart" in data, (
                f"{JIRA_ID}_CART_API001: Response should contain 'cart' key"
            )

    @pytest.mark.smoke
    def test_FC001_CART_API002_add_product_to_cart(
        self, auth_token, auth_headers, valid_product_id
    ):
        """FC-001_CART_API002: Verify POST /users/:userId/cart adds a product.
        Requirement: AC-06 – Authenticated user can add products to cart.
        """
        user_id = auth_token["user_id"]
        url = f"{API_BASE_URL}{ENDPOINTS['cart'].format(user_id=user_id)}"
        payload = {
            "userId": user_id,
            "productId": valid_product_id,
        }
        response = requests.post(
            url, json=payload, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code in [200, 201], (
            f"{JIRA_ID}_CART_API002: Expected 200/201, got {response.status_code}"
        )
        data = response.json()
        assert "cart" in data, (
            f"{JIRA_ID}_CART_API002: Response should contain 'cart' key"
        )

    def test_FC001_CART_API003_increase_quantity(
        self, auth_token, auth_headers, valid_product_id
    ):
        """FC-001_CART_API003: Verify POST /users/:userId/cart with increase flag.
        Requirement: AC-06 – User can increase item quantities.
        """
        user_id = auth_token["user_id"]
        url = f"{API_BASE_URL}{ENDPOINTS['cart'].format(user_id=user_id)}"
        payload = {
            "userId": user_id,
            "productId": valid_product_id,
            "increase": True,
        }
        response = requests.post(
            url, json=payload, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code in [200, 201], (
            f"{JIRA_ID}_CART_API003: Expected 200/201, got {response.status_code}"
        )

    def test_FC001_CART_API004_decrease_quantity(
        self, auth_token, auth_headers, valid_product_id
    ):
        """FC-001_CART_API004: Verify POST /users/:userId/cart with decrease flag.
        Requirement: AC-06 – User can decrease item quantities.
        """
        user_id = auth_token["user_id"]
        url = f"{API_BASE_URL}{ENDPOINTS['cart'].format(user_id=user_id)}"
        payload = {
            "userId": user_id,
            "productId": valid_product_id,
            "decrease": True,
        }
        response = requests.post(
            url, json=payload, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code in [200, 201], (
            f"{JIRA_ID}_CART_API004: Expected 200/201, got {response.status_code}"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_CART_API005_get_cart_without_auth(self):
        """FC-001_CART_API005: Verify GET cart without auth returns 401.
        Requirement: AC-06 – Cart requires authentication.
        """
        url = f"{API_BASE_URL}/users/fakeuserid/cart"
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code in [401, 403], (
            f"{JIRA_ID}_CART_API005: Expected 401/403, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_CART_API006_add_invalid_product_to_cart(
        self, auth_token, auth_headers
    ):
        """FC-001_CART_API006: Verify adding invalid product ID to cart.
        Requirement: AC-06 – Invalid product returns 'invalid request body'.
        """
        user_id = auth_token["user_id"]
        url = f"{API_BASE_URL}{ENDPOINTS['cart'].format(user_id=user_id)}"
        payload = {
            "userId": user_id,
            "productId": "000000000000000000000000",
        }
        response = requests.post(
            url, json=payload, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )

        assert response.status_code in [400, 406], (
            f"{JIRA_ID}_CART_API006: Expected 400/406, got {response.status_code}"
        )

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_CART_API007_create_empty_cart(self, auth_token, auth_headers):
        """FC-001_CART_API007: Verify POST cart without productId.
        Requirement: AC-06 – No productId on a new cart returns 400 (missing field)
        or 201 if cart already exists from prior tests.
        """
        user_id = auth_token["user_id"]
        url = f"{API_BASE_URL}{ENDPOINTS['cart'].format(user_id=user_id)}"
        payload = {"userId": user_id}
        response = requests.post(
            url, json=payload, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )

        # 200/201 = cart updated/created; 400 = no productId on fresh cart (valid server behavior)
        assert response.status_code in [200, 201, 400], (
            f"{JIRA_ID}_CART_API007: Expected 200/201/400, got {response.status_code}"
        )

    # ---- Business Rule Validation ----

    def test_FC001_CART_API008_cart_total_consistency(
        self, auth_token, auth_headers, valid_product_id
    ):
        """FC-001_CART_API008: Verify cart totalQty and totalPrice are consistent.
        Requirement: AC-06 – Business rule: totals must be non-negative.
        """
        user_id = auth_token["user_id"]
        url = f"{API_BASE_URL}{ENDPOINTS['cart'].format(user_id=user_id)}"

        # Add a product first
        payload = {"userId": user_id, "productId": valid_product_id}
        requests.post(
            url, json=payload, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )

        # Get cart and validate
        response = requests.get(
            url, headers=auth_headers, timeout=API_TIMEOUT_SECONDS
        )
        if response.status_code == 200:
            cart = response.json().get("cart", {})
            total_qty = cart.get("totalQty", 0)
            total_price = cart.get("totalPrice", 0)
            assert total_qty >= 0, (
                f"{JIRA_ID}_CART_API008: totalQty should be >= 0, got {total_qty}"
            )
            assert total_price >= 0, (
                f"{JIRA_ID}_CART_API008: totalPrice should be >= 0, got {total_price}"
            )
