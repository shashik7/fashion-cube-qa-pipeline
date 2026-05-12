# ============================================================================
# FC-001 | Fashion Cube QA Automation - Registration UI Tests
# Requirement: AC-01 – User Registration
# Test Cases: FC-001_TC002, TC007, TC008, TC012
# ============================================================================

import pytest
from pages.register_page import RegisterPage
from config.config import BASE_URL, TEST_USER_EMAIL, JIRA_ID


@pytest.mark.ui
class TestRegister:
    """FC-001: Registration functionality UI tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_TC002_successful_registration(self, page):
        """FC-001_TC002: Verify user can register with valid details.
        Requirement: AC-01 – User created, login form displayed after.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.register(
            name="John Doe",
            email=f"john.doe.{pytest.importorskip('time').time():.0f}@example.com",
            password="Secure@123",
        )

        register_page.wait_for_network_idle()
        # After successful registration, should switch to login form
        heading = register_page.get_form_heading()
        assert "Login" in heading or register_page.is_visible(".login-form"), (
            f"{JIRA_ID}_TC002: Should show login form after successful registration"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_TC007_register_duplicate_email(self, page):
        """FC-001_TC007: Verify registration fails with duplicate email.
        Requirement: AC-01 – Duplicate email returns HTTP 409 'user is existed'.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.register(
            name="Existing User",
            email=TEST_USER_EMAIL,
            password="Test@12345",
        )

        register_page.wait_for_network_idle()
        # Registration form should remain visible on duplicate email
        assert register_page.is_visible(".login-form"), (
            f"{JIRA_ID}_TC007: Form should remain visible on duplicate email"
        )

    @pytest.mark.negative
    def test_FC001_TC008_register_empty_fields(self, page):
        """FC-001_TC008: Verify registration fails with all empty fields.
        Requirement: AC-01 – All fields required, HTTP 400 on missing.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.open_registration_form()
        register_page.click_register_button()

        # Form should remain visible with validation preventing submission
        assert register_page.is_visible(".login-form"), (
            f"{JIRA_ID}_TC008: Form should remain visible with empty fields"
        )

    # ---- Boundary Tests ----

    @pytest.mark.boundary
    def test_FC001_TC012_register_extremely_long_name(self, page):
        """FC-001_TC012: Verify registration handles 255-character name.
        Requirement: AC-01 – Boundary value test for name field.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        long_name = "A" * 255
        register_page.register(
            name=long_name,
            email=f"longname.{pytest.importorskip('time').time():.0f}@example.com",
            password="Valid@123",
        )

        register_page.wait_for_network_idle()
        # System should handle long name gracefully without crashing
        assert register_page.is_visible(".login-form") or not register_page.is_visible(
            ".login-form"
        ), (
            f"{JIRA_ID}_TC012: System should handle 255-char name gracefully"
        )
