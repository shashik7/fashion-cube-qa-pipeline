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
    LOCATOR_USER_ICON = ".navbar_user li:nth-child(2) a"
    LOCATOR_EMAIL_INPUT = "#UserName"
    LOCATOR_PASSWORD_INPUT = "#Passwod"
    LOCATOR_LOGIN_BUTTON = ".login-form .log-btn"
    LOCATOR_LOGIN_FORM = ".login-form"
    LOCATOR_LOGIN_HEADING = ".login-form h2"
    LOCATOR_REGISTER_LINK = "text=New user ? Please Register"
    LOCATOR_FORGOT_PASSWORD_LINK = "text=Lost your password?"
    LOCATOR_ERROR_ALERT = ".login-form .alert"
    LOCATOR_LOADING_SPINNER = ".login-form .log-btn .spinner-border"

    def __init__(self, page):
        super().__init__(page)
        self.url = BASE_URL

    def navigate(self):
        """FC-001: Navigate to the home page."""
        super().navigate(self.url)

    def open_login_modal(self):
        """FC-001: Open the login modal by clicking the user icon."""
        self.click(self.LOCATOR_USER_ICON)
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
