import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestCheckout:
    """Test cases for checkout process"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Login and add item before each test"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        
        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        inventory_page.open_cart()
    
    def test_complete_checkout(self, page):
        """Test complete checkout process"""
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Fill information
        checkout_page.fill_information("John", "Doe", "12345")
        
        # Finish checkout
        checkout_page.finish_checkout()
        
        # Verify order completion
        assert checkout_page.is_checkout_complete(), "Checkout should be complete"
        confirmation = checkout_page.get_confirmation_message()
        assert "Thank you for your order" in confirmation
