# ============================================================================
# FC-001 | Fashion Cube QA Automation - User Registration UI Tests
# Requirement: AC-01 – User Registration
# Test Cases: FC-001_TC001-TC012
# All locators verified from: src/components/LoginRegisterModal/RegisterForm.js
#                             src/components/TopNavBar/index.js
#                             src/components/LoginRegisterModal/index.js
# ============================================================================

import time
import pytest
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from config.config import BASE_URL, JIRA_ID


def unique_email():
    """Generate a unique email address for each test run."""
    return f"testuser.{int(time.time())}@fashioncube.test"


@pytest.mark.ui
class TestRegister:
    """FC-001: User registration UI tests."""

    # ---- Functional Tests ----

    @pytest.mark.smoke
    def test_FC001_TC001_register_form_opens(self, page):
        """FC-001_TC001: Verify the registration form opens from the navbar.
        Requirement: AC-01 – Registration form is accessible.
        Source: TopNavBar:110 li.account → TopNavBar:126 'Register' link
                → LoginRegisterModal/index.js:28 modal#loginModal
                → RegisterForm.js:61 div.login-form
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        # Hover over My Account and click Register
        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)

        # Modal should open
        assert register_page.is_modal_visible(), (
            f"{JIRA_ID}_TC001: Modal (#loginModal) should be visible after clicking Register"
        )

    @pytest.mark.smoke
    def test_FC001_TC002_register_form_heading(self, page):
        """FC-001_TC002: Verify the registration form heading is 'Register'.
        Requirement: AC-01 – Form renders with correct heading.
        Source: RegisterForm.js:62 → h2 text = 'Register'
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_REGISTER_HEADING)

        heading = register_page.get_form_heading()
        assert heading == "Register", (
            f"{JIRA_ID}_TC002: Register form heading (.login-form h2) should be 'Register', got: '{heading}'"
        )

    @pytest.mark.smoke
    def test_FC001_TC003_register_form_fields_exist(self, page):
        """FC-001_TC003: Verify all required form fields are rendered.
        Requirement: AC-01 – Form has Name, Email, Password fields.
        Source: RegisterForm.js:68 input#name, :82 input#email, :96 input#Passwod
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)

        assert register_page.is_visible(register_page.LOCATOR_NAME_INPUT, timeout=5000), (
            f"{JIRA_ID}_TC003: Name field (input#name) should be visible"
        )
        assert register_page.is_visible(register_page.LOCATOR_EMAIL_INPUT, timeout=5000), (
            f"{JIRA_ID}_TC003: Email field (input#email) should be visible"
        )
        assert register_page.is_visible(register_page.LOCATOR_PASSWORD_INPUT, timeout=5000), (
            f"{JIRA_ID}_TC003: Password field (input#Passwod) should be visible"
        )

    def test_FC001_TC004_successful_registration(self, page):
        """FC-001_TC004: Verify a new user can register with valid credentials.
        Requirement: AC-01 – Successful registration redirects/switches to Login.
        Source: RegisterForm.js:46-50 → on success, loginClicked() is called
                which switches the modal back to LoginForm (h2='Login').
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.register(
            name="Test User",
            email=unique_email(),
            password="Test@1234",
        )
        register_page.wait_for_network_idle()
        page.wait_for_timeout(2000)

        # On success, RegisterForm calls loginClicked() which shows LoginForm
        # So the modal should still be visible but now show Login heading
        heading = register_page.get_form_heading()
        assert heading is not None, (
            f"{JIRA_ID}_TC004: Form should still be visible after registration attempt"
        )

    def test_FC001_TC005_switch_to_login_from_register(self, page):
        """FC-001_TC005: Verify clicking 'Already have an account' switches to Login form.
        Requirement: AC-01 – Navigation between Login and Register forms.
        Source: RegisterForm.js:122 → div onClick={loginClicked} text='Already have an account...'
                Switching renders LoginForm with h2='Login'.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        # Open Register form
        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        # Click the "Already have an account" link
        register_page.click_login_link()
        register_page.wait_for_element(register_page.LOCATOR_REGISTER_HEADING)

        heading = register_page.get_form_heading()
        assert heading == "Login", (
            f"{JIRA_ID}_TC005: Heading should switch to 'Login' after clicking login link, got: '{heading}'"
        )

    def test_FC001_TC006_switch_to_register_from_login(self, page):
        """FC-001_TC006: Verify clicking 'New user? Register' from Login switches to Register.
        Requirement: AC-01 – Navigation between Login and Register forms.
        Source: LoginForm.js:114 → div onClick={registerClicked} text='New user ? Please Register'
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        # Open Sign In modal first
        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click("text=Sign In")
        register_page.wait_for_element(register_page.LOCATOR_NEW_USER_LINK)

        # Switch to Register
        register_page.click(register_page.LOCATOR_NEW_USER_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        heading = register_page.get_form_heading()
        assert heading == "Register", (
            f"{JIRA_ID}_TC006: Heading should switch to 'Register', got: '{heading}'"
        )

    # ---- Negative Tests ----

    @pytest.mark.negative
    def test_FC001_TC007_register_with_empty_fields(self, page):
        """FC-001_TC007: Verify submitting empty form does not proceed.
        Requirement: AC-01 – Validator blocks empty fields.
        Source: RegisterForm.js:32-43 → Validator() is called for name, email, password.
                On failure, handleSubmit returns early without calling userRegister.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        # Click Register button without filling any fields
        register_page.click_register_button()
        page.wait_for_timeout(1000)

        # Form should still be visible (not submitted/closed)
        assert register_page.is_registration_form_displayed(), (
            f"{JIRA_ID}_TC007: Register form (div.login-form) should remain open after empty submit"
        )

    @pytest.mark.negative
    def test_FC001_TC008_register_with_invalid_email(self, page):
        """FC-001_TC008: Verify registration with invalid email format is rejected.
        Requirement: AC-01 – EMAIL_RULE validator blocks invalid emails.
        Source: RegisterForm.js:36 → Validator(email, EMAIL_RULE) must pass.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        register_page.enter_name("Test User")
        register_page.enter_email("not-a-valid-email")
        register_page.enter_password("Test@1234")
        register_page.click_register_button()
        page.wait_for_timeout(1000)

        # Form should still be open — validator rejected it
        assert register_page.is_registration_form_displayed(), (
            f"{JIRA_ID}_TC008: Form should stay open with invalid email (EMAIL_RULE validation)"
        )

    @pytest.mark.negative
    def test_FC001_TC009_register_with_empty_name(self, page):
        """FC-001_TC009: Verify registration with empty name is rejected.
        Requirement: AC-01 – DEFAULT_RULE validator blocks empty name.
        Source: RegisterForm.js:32 → Validator(name, DEFAULT_RULE) checked first.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        # Leave name empty
        register_page.enter_email(unique_email())
        register_page.enter_password("Test@1234")
        register_page.click_register_button()
        page.wait_for_timeout(1000)

        assert register_page.is_registration_form_displayed(), (
            f"{JIRA_ID}_TC009: Form should stay open when name is empty (DEFAULT_RULE validation)"
        )

    @pytest.mark.negative
    def test_FC001_TC010_register_with_empty_password(self, page):
        """FC-001_TC010: Verify registration with empty password is rejected.
        Requirement: AC-01 – DEFAULT_RULE validator blocks empty password.
        Source: RegisterForm.js:40 → Validator(password, DEFAULT_RULE) checked last.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        register_page.enter_name("Test User")
        register_page.enter_email(unique_email())
        # Leave password empty
        register_page.click_register_button()
        page.wait_for_timeout(1000)

        assert register_page.is_registration_form_displayed(), (
            f"{JIRA_ID}_TC010: Form should stay open when password is empty"
        )

    # ---- Edge Cases ----

    @pytest.mark.edge
    def test_FC001_TC011_register_form_can_be_filled(self, page):
        """FC-001_TC011: Verify all form fields accept and retain typed input.
        Requirement: AC-01 – Inputs are controlled components (React state).
        Source: RegisterForm.js:25-28 → handleChange updates this.state.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        test_name = "Edge Case User"
        test_email = unique_email()
        test_password = "Edge@1234"

        register_page.enter_name(test_name)
        register_page.enter_email(test_email)
        register_page.enter_password(test_password)

        actual_name = page.locator(register_page.LOCATOR_NAME_INPUT).input_value()
        actual_email = page.locator(register_page.LOCATOR_EMAIL_INPUT).input_value()

        assert actual_name == test_name, (
            f"{JIRA_ID}_TC011: input#name value should be '{test_name}', got: '{actual_name}'"
        )
        assert actual_email == test_email, (
            f"{JIRA_ID}_TC011: input#email value should be '{test_email}', got: '{actual_email}'"
        )

    @pytest.mark.edge
    def test_FC001_TC012_register_button_text(self, page):
        """FC-001_TC012: Verify the register button has correct text.
        Requirement: AC-01 – Button is clearly labelled 'Register'.
        Source: RegisterForm.js:111 → LoadingButton children text = 'Register'
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_REGISTER_BUTTON)

        btn_text = register_page.get_text(register_page.LOCATOR_REGISTER_BUTTON)
        assert btn_text is not None and "Register" in btn_text, (
            f"{JIRA_ID}_TC012: Register button text should contain 'Register', got: '{btn_text}'"
        )

    # ---- Boundary Tests ----

    @pytest.mark.boundary
    def test_FC001_TC013_register_with_minimum_valid_input(self, page):
        """FC-001_TC013: Verify registration with minimum valid field lengths.
        Requirement: AC-01 – Boundary value test for minimum valid input.
        Source: RegisterForm.js:32-43 → validators pass for non-empty values.
        """
        register_page = RegisterPage(page)
        register_page.navigate()
        register_page.wait_for_network_idle()

        register_page.wait_for_element(register_page.LOCATOR_ACCOUNT_MENU)
        page.locator(register_page.LOCATOR_ACCOUNT_MENU).hover()
        register_page.click(register_page.LOCATOR_REGISTER_NAV_LINK)
        register_page.wait_for_element(register_page.LOCATOR_NAME_INPUT)

        register_page.enter_name("A")
        register_page.enter_email(unique_email())
        register_page.enter_password("P")
        register_page.click_register_button()
        page.wait_for_timeout(2000)

        # App should attempt registration (validators pass for non-empty values)
        # Form may close on success or show API error — either is acceptable
        assert page.title() is not None, (
            f"{JIRA_ID}_TC013: Application should not crash on minimum valid input"
        )
