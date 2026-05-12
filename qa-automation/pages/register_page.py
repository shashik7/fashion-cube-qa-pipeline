# ============================================================================
# FC-001 | Fashion Cube QA Automation - Register Page Object
# Requirement: AC-01 – User Registration
# Locators derived from: src/components/LoginRegisterModal/RegisterForm.js
# ============================================================================

from pages.base_page import BasePage
from config.config import BASE_URL


class RegisterPage(BasePage):
    """FC-001: Page Object for the Registration Form."""

    # ---- Locators ----
    LOCATOR_USER_ICON = ".navbar_user li:nth-child(2) a"
    LOCATOR_NAME_INPUT = "#name"
    LOCATOR_EMAIL_INPUT = "#email"
    LOCATOR_PASSWORD_INPUT = "#Passwod"
    LOCATOR_REGISTER_BUTTON = ".login-form .log-btn"
    LOCATOR_LOGIN_FORM = ".login-form"
    LOCATOR_REGISTER_HEADING = ".login-form h2"
    LOCATOR_LOGIN_LINK = "text=Already have an account ? Please login."
    LOCATOR_NEW_USER_LINK = "text=New user ? Please Register"
    LOCATOR_ERROR_ALERT = ".login-form .alert"

    def __init__(self, page):
        super().__init__(page)
        self.url = BASE_URL

    def navigate(self):
        """FC-001: Navigate to the home page."""
        super().navigate(self.url)

    def open_registration_form(self):
        """FC-001: Open login modal then switch to registration form."""
        self.click(self.LOCATOR_USER_ICON)
        self.wait_for_element(self.LOCATOR_LOGIN_FORM)
        self.click(self.LOCATOR_NEW_USER_LINK)
        self.wait_for_element(self.LOCATOR_NAME_INPUT)

    def enter_name(self, name):
        """FC-001: Enter name in the registration form."""
        self.fill(self.LOCATOR_NAME_INPUT, name)

    def enter_email(self, email):
        """FC-001: Enter email in the registration form."""
        self.fill(self.LOCATOR_EMAIL_INPUT, email)

    def enter_password(self, password):
        """FC-001: Enter password in the registration form."""
        self.fill(self.LOCATOR_PASSWORD_INPUT, password)

    def click_register_button(self):
        """FC-001: Click the Register button."""
        self.click(self.LOCATOR_REGISTER_BUTTON)

    def register(self, name, email, password):
        """FC-001: Perform complete registration flow."""
        self.open_registration_form()
        self.enter_name(name)
        self.enter_email(email)
        self.enter_password(password)
        self.click_register_button()

    def click_login_link(self):
        """FC-001: Click the 'Already have an account' link."""
        self.click(self.LOCATOR_LOGIN_LINK)

    def get_error_message(self):
        """FC-001: Get the error alert text."""
        return self.get_text(self.LOCATOR_ERROR_ALERT)

    def is_registration_form_displayed(self):
        """FC-001: Check if the registration form is displayed."""
        if not self.is_visible(self.LOCATOR_LOGIN_FORM):
            return False
        heading = self.get_text(self.LOCATOR_REGISTER_HEADING)
        return "Register" in heading

    def get_form_heading(self):
        """FC-001: Get the form heading text."""
        return self.get_text(self.LOCATOR_REGISTER_HEADING)
