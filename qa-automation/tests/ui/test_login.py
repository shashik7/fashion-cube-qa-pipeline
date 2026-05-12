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
        page.on("console", lambda msg: print(f"[BROWSER CONSOLE] {msg.type}: {msg.text}"))
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(TEST_USER_EMAI, TEST_USER_PASSWORD)  # [AI-HEAL]

        # Wait for page reload after successful login
        login_page.wait_for_network_idle()

        # After successful login the login modal should close
        login_page.wait_for_element(login_page.LOCATOR_LOGIN_FORM, state="hidden")
        assert not login_page.is_login_form_displayed(), (
            f"{JIRA_ID}_TC001: Login modal should close after successful login"
        )

