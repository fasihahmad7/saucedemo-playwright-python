from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Shopping Cart Page"""
    
    # Locators
    CART_ITEMS = ".cart_item"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING = "#continue-shopping"
    REMOVE_BUTTON = "button[name^='remove']"
    
    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        return self.page.locator(self.CART_ITEMS).count()
    
    def proceed_to_checkout(self):
        """Click checkout button"""
        self.click(self.CHECKOUT_BUTTON)
    
    def continue_shopping(self):
        """Click continue shopping button"""
        self.click(self.CONTINUE_SHOPPING)
