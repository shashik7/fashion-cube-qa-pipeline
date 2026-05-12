# ============================================================================
# FC-001 | Fashion Cube QA Automation - Login Page Object
# Requirement: AC-02 – User Login
# Locators derived from: src/components/LoginRegisterModal/LoginForm.js
# ============================================================================

from pages.base_page import BasePage
from config.config import BASE_URL


class LoginPage(BasePage):
    """FC-001: Page Object for the Login Modal/Form."""

    # ---- Locators (stable strategy: ID > CSS class > text) ----
    LOCATOR_ACCOUNT_MENU = ".account > a"
    LOCATOR_SIGN_IN_LINK = "text=Sign In"
    LOCATOR_EMAIL_INPUT = "#UserName"
    LOCATOR_PASSWORD_INPUT = "#Passwod"  # Note: Original code has 'Passwod' typo
    LOCATOR_LOGIN_BUTTON = ".log-btn"
    LOCATOR_LOGIN_FORM = "#loginModal"
    LOCATOR_LOGIN_HEADING = "#loginModal h2"
    LOCATOR_REGISTER_LINK = "text=New user ? Please Register"
    LOCATOR_FORGOT_PASSWORD_LINK = "text=Lost your password?"
    LOCATOR_ERROR_ALERT = ".alert-danger"
    LOCATOR_LOADING_SPINNER = ".spinner-border"

    def __init__(self, page):
        super().__init__(page)
        self.url = BASE_URL

    def navigate(self):
        """FC-001: Navigate to the home page."""
        super().navigate(self.url)

    def open_login_modal(self):
        """FC-001: Open the login modal via TopNavBar account menu."""
        # Ensure the page is loaded
        self.wait_for_element(self.LOCATOR_ACCOUNT_MENU)
        # The menu might need a hover or just direct click on the Sign In link
        self.page.locator(self.LOCATOR_ACCOUNT_MENU).hover()
        self.click(self.LOCATOR_SIGN_IN_LINK)
        self.wait_for_element(self.LOCATOR_LOGIN_FORM)

    def enter_email(self, email):
        """FC-001: Enter email in the login form."""
        self.fill(self.LOCATOR_EMAIL_INPUT, email)

    def enter_password(self, password):
        """FC-001: Enter password in the login form."""
        self.fill(self.LOCATOR_PASSWORD_INPUT, password)

    def click_login_button(self):
        """FC-001: Click the Log in button."""
        self.click(self.LOCATOR_LOGIN_BUTTON)

    def login(self, email, password):
        """FC-001: Perform complete login flow."""
        self.open_login_modal()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def click_register_link(self):
        """FC-001: Click the 'New user ? Please Register' link."""
        self.click(self.LOCATOR_REGISTER_LINK)

    def click_forgot_password(self):
        """FC-001: Click the 'Lost your password?' link."""
        self.click(self.LOCATOR_FORGOT_PASSWORD_LINK)

    def get_error_message(self):
        """FC-001: Get the error alert text."""
        return self.get_text(self.LOCATOR_ERROR_ALERT)

    def is_login_form_displayed(self):
        """FC-001: Check if the login form is displayed."""
        return self.is_visible(self.LOCATOR_LOGIN_FORM)

    def get_login_heading(self):
        """FC-001: Get the login form heading text."""
        return self.get_text(self.LOCATOR_LOGIN_HEADING)

    def is_loading(self):
        """FC-001: Check if the login button is in loading state."""
        return self.is_visible(self.LOCATOR_LOADING_SPINNER, timeout=2000)

    def get_email_value(self):
        """FC-001: Get the current email input value."""
        return self.get_input_value(self.LOCATOR_EMAIL_INPUT)

    def get_password_value(self):
        """FC-001: Get the current password input value."""
        return self.get_input_value(self.LOCATOR_PASSWORD_INPUT)
