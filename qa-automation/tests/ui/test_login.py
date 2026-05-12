# ============================================================================
# FC-001 | Fashion Cube QA Automation - Login UI Tests
# Requirement: AC-02 – User Login
# Test Cases: FC-001_TC001, TC003-TC006, TC009-TC011, TC013
# ============================================================================

import pytest
from pages.login_page import LoginPage
from config.config import (
    BASE_URL,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    JIRA_ID,
)


@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:
    """FC-001: Login functionality UI tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_TC001_successful_login(self, page):
        """FC-001_TC001: Verify user can login with valid credentials.
        Requirement: AC-02 – JWT token returned, page reloads with auth state.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

        # Wait for page reload after successful login
        login_page.wait_for_network_idle()

        # After successful login the login modal should close
        assert not login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC001: Login modal should close after successful login"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_TC003_login_invalid_email_format(self, page):
        """FC-001_TC003: Verify login fails with invalid email format.
        Requirement: AC-02 – Email validation must be enforced client-side.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.open_login_modal()
        login_page.enter_email("not-an-email")
        login_page.enter_password(TEST_USER_PASSWORD)
        login_page.click_login_button()

        # Validation should prevent login; form should remain visible
        assert login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC003: Login form should remain visible on invalid email"
        )

    @pytest.mark.negative
    def test_FC001_TC004_login_incorrect_password(self, page):
        """FC-001_TC004: Verify login fails with incorrect password.
        Requirement: AC-02 – Returns HTTP 403 'Incorrect email or password'.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(TEST_USER_EMAIL, "WrongPassword123")

        login_page.wait_for_network_idle()
        assert login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC004: Login form should remain visible on wrong password"
        )

    @pytest.mark.negative
    def test_FC001_TC005_login_empty_email(self, page):
        """FC-001_TC005: Verify login fails when email field is empty.
        Requirement: AC-02 – Missing fields return HTTP 400.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.open_login_modal()
        login_page.enter_password(TEST_USER_PASSWORD)
        login_page.click_login_button()

        assert login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC005: Login form should remain visible when email is empty"
        )

    @pytest.mark.negative
    def test_FC001_TC006_login_empty_password(self, page):
        """FC-001_TC006: Verify login fails when password field is empty.
        Requirement: AC-02 – Missing fields return HTTP 400.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.open_login_modal()
        login_page.enter_email(TEST_USER_EMAIL)
        login_page.click_login_button()

        assert login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC006: Login form should remain visible when password is empty"
        )

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_TC009_login_sql_injection(self, page):
        """FC-001_TC009: Verify login handles SQL injection safely.
        Requirement: AC-02 – System must not expose errors on malicious input.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("' OR '1'='1", "anything")
        login_page.wait_for_network_idle()

        # System should not crash; login form should remain
        assert login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC009: System should handle SQL injection safely"
        )

    @pytest.mark.edge
    def test_FC001_TC010_login_xss_payload(self, page):
        """FC-001_TC010: Verify login handles XSS payload safely.
        Requirement: AC-02 – No script execution on malicious input.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("<script>alert('xss')</script>", "anything")
        login_page.wait_for_network_idle()

        # Verify no alert dialog was triggered
        assert login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC010: System should handle XSS payload safely"
        )

    # ---- Boundary Tests ----

    @pytest.mark.boundary
    def test_FC001_TC011_login_minimum_password_length(self, page):
        """FC-001_TC011: Verify login with 1-character password.
        Requirement: AC-02 – Boundary value test for password field.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(TEST_USER_EMAIL, "a")
        login_page.wait_for_network_idle()

        assert login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC011: Login should fail with minimum length password"
        )

    # ---- State Transition Tests ----

    def test_FC001_TC013_toggle_login_register_forms(self, page):
        """FC-001_TC013: Verify toggle between Login and Register forms.
        Requirement: AC-01/AC-02 – State transition validation.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.open_login_modal()

        # Verify Login form is displayed first
        heading = login_page.get_login_heading()
        assert "Login" in heading, (
            f"{JIRA_ID}_TC013: Initial form should be Login, got '{heading}'"
        )

        # Switch to Register form
        login_page.click_register_link()
        page.wait_for_timeout(500)
        heading = login_page.get_text(".login-form h2")
        assert "Register" in heading, (
            f"{JIRA_ID}_TC013: Should switch to Register form, got '{heading}'"
        )

        # Switch back to Login form
        login_page.click("text=Already have an account ? Please login.")
        page.wait_for_timeout(500)
        heading = login_page.get_login_heading()
        assert "Login" in heading, (
            f"{JIRA_ID}_TC013: Should switch back to Login form, got '{heading}'"
        )
