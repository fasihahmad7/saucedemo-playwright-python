from pages.base_page import BasePage

class InventoryPage(BasePage):
    """Page Object for Inventory/Products Page"""
    
    # Locators
    INVENTORY_CONTAINER = "[data-test='inventory-container']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    PRODUCT_SORT = ".product_sort_container"
    
    # Dynamic locators
    ADD_TO_CART_BUTTON = "button[data-test='add-to-cart-{}']"
    REMOVE_BUTTON = "button[data-test='remove-{}']"
    
    def is_loaded(self) -> bool:
        """Check if inventory page is loaded"""
        return self.is_visible(self.INVENTORY_CONTAINER)
    
    def add_item_to_cart(self, item_name: str):
        """Add item to cart by name"""
        item_id = item_name.lower().replace(" ", "-")
        self.click(self.ADD_TO_CART_BUTTON.format(item_id))
    
    def remove_item_from_cart(self, item_name: str):
        """Remove item from cart"""
        item_id = item_name.lower().replace(" ", "-")
        self.click(self.REMOVE_BUTTON.format(item_id))
    
    def get_cart_count(self) -> str:
        """Get cart badge count"""
        if self.is_visible(self.CART_BADGE):
            return self.get_text(self.CART_BADGE)
        return "0"
    
    def open_cart(self):
        """Click on cart icon"""
        self.click(self.CART_LINK)
    
    def logout(self):
        """Perform logout"""
        self.click(self.MENU_BUTTON)
        self.page.wait_for_timeout(500)  # Wait for menu animation
        self.click(self.LOGOUT_LINK)
    
    def sort_products(self, option: str):
        """Sort products by option"""
        self.page.select_option(self.PRODUCT_SORT, option)
    
    def get_first_product_name(self) -> str:
        """Get first product name"""
        return self.page.locator(".inventory_item_name").first.inner_text()
