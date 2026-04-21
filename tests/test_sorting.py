import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestSorting:
    """Test cases for product sorting"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Login before each test"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
    
    def test_sort_products_by_name(self, page):
        """Test sorting products by name Z to A"""
        inventory_page = InventoryPage(page)
        
        # Sort by name Z to A
        inventory_page.sort_products("za")
        
        # Get first product name
        first_product = inventory_page.get_first_product_name()
        
        # Verify it starts with a letter from end of alphabet
        # Test Allure Labs Onesie should be last when sorted Z-A
        assert first_product == "Test.allTheThings() T-Shirt (Red)"
