import pytest
from playwright.sync_api import Page, Browser

@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """Create a new page for each test"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        }
    }
