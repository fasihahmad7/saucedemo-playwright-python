from playwright.sync_api import Page

class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str):
        """Navigate to a URL"""
        self.page.goto(url)
    
    def click(self, selector: str):
        """Click an element"""
        self.page.click(selector)
    
    def fill(self, selector: str, text: str):
        """Fill input field"""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text from element"""
        return self.page.locator(selector).inner_text()
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return self.page.locator(selector).is_visible()
