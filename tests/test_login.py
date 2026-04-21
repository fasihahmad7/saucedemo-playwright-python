import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestLogin:
    """Test cases for login functionality"""
    
    def test_valid_login(self, page):
        """Test login with valid credentials"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        
        # Verify user is on inventory page
        assert inventory_page.is_loaded(), "User should be on inventory page after login"
    
    def test_invalid_login(self, page):
        """Test login with invalid credentials"""
        login_page = LoginPage(page)
        
        login_page.open()
        login_page.login("invalid_user", "wrong_password")
        
        # Verify error message is displayed
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text
