from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """Page Object for Checkout Pages"""
    
    # Step 1 - Information
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    
    # Step 2 - Overview
    FINISH_BUTTON = "#finish"
    
    # Confirmation
    COMPLETE_HEADER = ".complete-header"
    
    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        """Fill checkout information"""
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)
    
    def finish_checkout(self):
        """Click finish button"""
        self.click(self.FINISH_BUTTON)
    
    def get_confirmation_message(self) -> str:
        """Get order confirmation message"""
        return self.get_text(self.COMPLETE_HEADER)
    
    def is_checkout_complete(self) -> bool:
        """Check if checkout is complete"""
        return self.is_visible(self.COMPLETE_HEADER)
