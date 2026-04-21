import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestLogout:
    """Test cases for logout functionality"""
    
    def test_logout(self, page):
        """Test logout functionality"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        # Login first
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        
        # Verify on inventory page
        assert inventory_page.is_loaded()
        
        # Logout
        inventory_page.logout()
        
        # Verify back on login page
        assert page.url == "https://www.saucedemo.com/"
