# ============================================================================
# FC-001 | Fashion Cube QA Automation - Register Page Object
# Requirement: AC-01 – User Registration
# Locators derived from: src/components/LoginRegisterModal/RegisterForm.js
#                        src/components/TopNavBar/index.js
#                        src/components/LoginRegisterModal/index.js
# ============================================================================
# SOURCE VERIFICATION:
#   TopNavBar/index.js:110   → li.account > a  ("My Account" hover trigger)
#   TopNavBar/index.js:126   → a:has-text('Register')  (opens register modal)
#   LoginRegisterModal/index.js:28 → modal id="loginModal"
#   RegisterForm.js:61       → div.login-form  (form container)
#   RegisterForm.js:62       → h2 text = "Register"
#   RegisterForm.js:68       → input#name  (name field)
#   RegisterForm.js:82       → input#email  (email field)
#   RegisterForm.js:96       → input#Passwod  (password field — typo in source)
#   RegisterForm.js:107      → button.log-btn  (submit button, text="Register")
#   RegisterForm.js:122      → "Already have an account ? Please login." (link text)
#   LoginForm.js:114         → "New user ? Please Register" (switch to register link)
#   RegisterForm.js:104      → span.alert  (error message)
# ============================================================================

from pages.base_page import BasePage
from config.config import BASE_URL


class RegisterPage(BasePage):
    """FC-001: Page Object for the Registration Form."""

    # ---- Locators (verified from React source) ----
    # TopNavBar:110 – "My Account" dropdown trigger (unauthenticated state)
    LOCATOR_ACCOUNT_MENU = ".account > a"
    # TopNavBar:126 – "Register" link in account dropdown
    LOCATOR_REGISTER_NAV_LINK = "text=Register"
    # LoginRegisterModal/index.js:28 – the modal wrapper
    LOCATOR_MODAL = "#loginModal"
    # RegisterForm.js:61 – form container div
    LOCATOR_REGISTER_FORM = ".login-form"
    # RegisterForm.js:62 – heading h2 text="Register"
    LOCATOR_REGISTER_HEADING = ".login-form h2"
    # RegisterForm.js:68 – name input id="name"
    LOCATOR_NAME_INPUT = "#name"
    # RegisterForm.js:82 – email input id="email"
    LOCATOR_EMAIL_INPUT = "#email"
    # RegisterForm.js:96 – password input id="Passwod" (typo preserved from source)
    LOCATOR_PASSWORD_INPUT = "#Passwod"
    # RegisterForm.js:107 – submit button class="log-btn", text="Register"
    LOCATOR_REGISTER_BUTTON = ".login-form .log-btn"
    # RegisterForm.js:122 – "Already have an account?" text link (switch to login)
    LOCATOR_LOGIN_LINK = "text=Already have an account ? Please login."
    # LoginForm.js:114 – "New user ? Please Register" text link (switch to register)
    LOCATOR_NEW_USER_LINK = "text=New user ? Please Register"
    # RegisterForm.js:104 – error alert span.alert
    LOCATOR_ERROR_ALERT = ".login-form .alert"

    def __init__(self, page):
        super().__init__(page)
        self.url = BASE_URL

    def navigate(self):
        """FC-001: Navigate to the home page."""
        super().navigate(self.url)

    def open_registration_form(self):
        """FC-001: Open register modal via TopNavBar 'My Account' → 'Register'.
        Source: TopNavBar:110 li.account; TopNavBar:126 Register link.
        """
        self.wait_for_element(self.LOCATOR_ACCOUNT_MENU)
        self.page.locator(self.LOCATOR_ACCOUNT_MENU).hover()
        self.click(self.LOCATOR_REGISTER_NAV_LINK)
        self.wait_for_element(self.LOCATOR_NAME_INPUT)

    def open_login_modal_then_switch(self):
        """FC-001: Alternative flow – open Sign In then click 'New user? Register'.
        Source: LoginForm.js:114.
        """
        self.wait_for_element(self.LOCATOR_ACCOUNT_MENU)
        self.page.locator(self.LOCATOR_ACCOUNT_MENU).hover()
        self.click("text=Sign In")
        self.wait_for_element(self.LOCATOR_NEW_USER_LINK)
        self.click(self.LOCATOR_NEW_USER_LINK)
        self.wait_for_element(self.LOCATOR_NAME_INPUT)

    def enter_name(self, name):
        """FC-001: Enter name in the registration form (input#name)."""
        self.fill(self.LOCATOR_NAME_INPUT, name)

    def enter_email(self, email):
        """FC-001: Enter email in the registration form (input#email)."""
        self.fill(self.LOCATOR_EMAIL_INPUT, email)

    def enter_password(self, password):
        """FC-001: Enter password in the registration form (input#Passwod)."""
        self.fill(self.LOCATOR_PASSWORD_INPUT, password)

    def click_register_button(self):
        """FC-001: Click the Register button (button.log-btn)."""
        self.click(self.LOCATOR_REGISTER_BUTTON)

    def register(self, name, email, password):
        """FC-001: Perform complete registration flow."""
        self.open_registration_form()
        self.enter_name(name)
        self.enter_email(email)
        self.enter_password(password)
        self.click_register_button()

    def click_login_link(self):
        """FC-001: Click 'Already have an account? Please login.' link."""
        self.click(self.LOCATOR_LOGIN_LINK)

    def get_error_message(self):
        """FC-001: Get the error alert text (span.alert)."""
        return self.get_text(self.LOCATOR_ERROR_ALERT)

    def is_registration_form_displayed(self):
        """FC-001: Check if registration form is shown by verifying h2='Register'."""
        if not self.is_visible(self.LOCATOR_REGISTER_FORM):
            return False
        heading = self.get_text(self.LOCATOR_REGISTER_HEADING)
        return heading is not None and "Register" in heading

    def is_login_form_displayed(self):
        """FC-001: Check if the form switched back to Login (h2='Login')."""
        if not self.is_visible(self.LOCATOR_REGISTER_FORM):
            return False
        heading = self.get_text(self.LOCATOR_REGISTER_HEADING)
        return heading is not None and "Login" in heading

    def get_form_heading(self):
        """FC-001: Get the form heading text (.login-form h2)."""
        return self.get_text(self.LOCATOR_REGISTER_HEADING)

    def is_modal_visible(self):
        """FC-001: Check if the login/register modal (#loginModal) is visible."""
        return self.is_visible(self.LOCATOR_MODAL)
