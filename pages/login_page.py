from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for Login Page"""
    
    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/"
    
    def open(self):
        """Open login page"""
        self.navigate_to(self.url)
    
    def login(self, username: str, password: str):
        """Perform login"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_visible(self.ERROR_MESSAGE)
