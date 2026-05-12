# ============================================================================
# FC-001 | Fashion Cube QA Automation - Auth API Tests
# Requirement: AC-01 (Registration), AC-02 (Login)
# Endpoints: POST /users/login, POST /users/signin
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
    TEST_USER_FULLNAME,
    JIRA_ID,
)


# ---- JSON Schemas ----

LOGIN_SUCCESS_SCHEMA = {
    "type": "object",
    "properties": {
        "user_token": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "user_name": {"type": "string"},
                "token": {"type": "string"},
                "expire_in": {"type": "string"},
            },
            "required": ["user_id", "user_name", "token", "expire_in"],
        }
    },
    "required": ["user_token"],
}

ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "status": {"type": "integer"},
        "errorType": {"type": "string"},
    },
}


@pytest.mark.api
class TestAuthAPI:
    """FC-001: Authentication API endpoint tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_AUTH_API001_login_valid_credentials(self):
        """FC-001_AUTH_API001: Verify POST /users/login with valid credentials.
        Requirement: AC-02 – Returns JWT token with 7-day expiry.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        payload = {
            "credential": {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD,
            }
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 201, (
            f"{JIRA_ID}_AUTH_API001: Expected 201, got {response.status_code}"
        )
        data = response.json()
        validate(instance=data, schema=LOGIN_SUCCESS_SCHEMA)
        assert data["user_token"]["expire_in"] == "7d", (
            f"{JIRA_ID}_AUTH_API001: Token expiry should be '7d'"
        )

    def test_FC001_AUTH_API002_register_new_user(self):
        """FC-001_AUTH_API002: Verify POST /users/signin creates new user.
        Requirement: AC-01 – User created with fullname, email, password.
        """
        import time

        url = f"{API_BASE_URL}{ENDPOINTS['register']}"
        unique_email = f"testuser_{int(time.time())}@example.com"
        payload = {
            "fullname": "Test Registration User",
            "email": unique_email,
            "password": "TestPass@123",
            "verifyPassword": "TestPass@123",
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 200, (
            f"{JIRA_ID}_AUTH_API002: Expected 200, got {response.status_code}"
        )
        data = response.json()
        assert data.get("message") == "user created", (
            f"{JIRA_ID}_AUTH_API002: Expected 'user created' message"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_AUTH_API003_login_missing_email(self):
        """FC-001_AUTH_API003: Verify login fails with missing email.
        Requirement: AC-02 – Missing fields return HTTP 400.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        payload = {"credential": {"password": TEST_USER_PASSWORD}}
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 400, (
            f"{JIRA_ID}_AUTH_API003: Expected 400, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_AUTH_API004_login_missing_password(self):
        """FC-001_AUTH_API004: Verify login fails with missing password.
        Requirement: AC-02 – Missing fields return HTTP 400.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        payload = {"credential": {"email": TEST_USER_EMAIL}}
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 400, (
            f"{JIRA_ID}_AUTH_API004: Expected 400, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_AUTH_API005_login_wrong_password(self):
        """FC-001_AUTH_API005: Verify login fails with incorrect password.
        Requirement: AC-02 – Returns HTTP 403 'Incorrect email or password'.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        payload = {
            "credential": {
                "email": TEST_USER_EMAIL,
                "password": "WrongPassword123",
            }
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 403, (
            f"{JIRA_ID}_AUTH_API005: Expected 403, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_AUTH_API006_login_nonexistent_user(self):
        """FC-001_AUTH_API006: Verify login fails for non-existent user.
        Requirement: AC-02 – Non-existent email returns HTTP 403.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        payload = {
            "credential": {
                "email": "nonexistent@nowhere.com",
                "password": "anything",
            }
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 403, (
            f"{JIRA_ID}_AUTH_API006: Expected 403, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_AUTH_API007_register_duplicate_email(self):
        """FC-001_AUTH_API007: Verify registration fails with duplicate email.
        Requirement: AC-01 – Duplicate email returns HTTP 409.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['register']}"
        payload = {
            "fullname": "Duplicate User",
            "email": TEST_USER_EMAIL,
            "password": "Test@12345",
            "verifyPassword": "Test@12345",
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 409, (
            f"{JIRA_ID}_AUTH_API007: Expected 409, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_AUTH_API008_register_missing_fields(self):
        """FC-001_AUTH_API008: Verify registration fails with missing fields.
        Requirement: AC-01 – All fields required, HTTP 400 on missing.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['register']}"
        payload = {"email": "partial@example.com"}
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 400, (
            f"{JIRA_ID}_AUTH_API008: Expected 400, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_FC001_AUTH_API009_register_invalid_email(self):
        """FC-001_AUTH_API009: Verify registration fails with invalid email.
        Requirement: AC-01 – Email validation enforced server-side.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['register']}"
        payload = {
            "fullname": "Invalid Email User",
            "email": "not-a-valid-email",
            "password": "Test@12345",
            "verifyPassword": "Test@12345",
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 400, (
            f"{JIRA_ID}_AUTH_API009: Expected 400, got {response.status_code}"
        )

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_AUTH_API010_login_empty_body(self):
        """FC-001_AUTH_API010: Verify login with empty request body.
        Requirement: AC-02 – Edge case: empty payload handling.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        response = requests.post(url, json={}, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code == 400, (
            f"{JIRA_ID}_AUTH_API010: Expected 400, got {response.status_code}"
        )

    @pytest.mark.edge
    def test_FC001_AUTH_API011_login_sql_injection(self):
        """FC-001_AUTH_API011: Verify login handles SQL injection safely.
        Requirement: AC-02 – Security edge case.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        payload = {
            "credential": {
                "email": "' OR '1'='1' --",
                "password": "anything",
            }
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        assert response.status_code in [400, 403], (
            f"{JIRA_ID}_AUTH_API011: Expected 400/403, got {response.status_code}"
        )

    # ---- Token Validation ----

    def test_FC001_AUTH_API012_token_format_validation(self):
        """FC-001_AUTH_API012: Verify JWT token format in login response.
        Requirement: AC-02 – Token should be a valid JWT string.
        """
        url = f"{API_BASE_URL}{ENDPOINTS['login']}"
        payload = {
            "credential": {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD,
            }
        }
        response = requests.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)

        if response.status_code == 201:
            token = response.json()["user_token"]["token"]
            # JWT tokens have 3 parts separated by dots
            parts = token.split(".")
            assert len(parts) == 3, (
                f"{JIRA_ID}_AUTH_API012: JWT should have 3 parts, got {len(parts)}"
            )
        else:
            pytest.skip(f"{JIRA_ID}_AUTH_API012: Login failed, cannot validate token")
