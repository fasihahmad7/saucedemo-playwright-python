import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

class TestCart:
    """Test cases for shopping cart functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Login before each test"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
    
    def test_add_items_to_cart(self, page):
        """Test adding multiple items to cart"""
        inventory_page = InventoryPage(page)
        
        # Add items to cart
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        inventory_page.add_item_to_cart("sauce-labs-bike-light")
        
        # Verify cart count
        cart_count = inventory_page.get_cart_count()
        assert cart_count == "2", f"Cart should have 2 items, but has {cart_count}"
    
    def test_remove_items_from_cart(self, page):
        """Test removing items from cart"""
        inventory_page = InventoryPage(page)
        
        # Add items first
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        inventory_page.add_item_to_cart("sauce-labs-bike-light")
        
        # Remove one item
        inventory_page.remove_item_from_cart("sauce-labs-backpack")
        
        # Verify cart count
        cart_count = inventory_page.get_cart_count()
        assert cart_count == "1", f"Cart should have 1 item after removal"
