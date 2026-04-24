# Complete Framework Guide - Saucedemo Playwright Python Automation

## Table of Contents
1. [Introduction to Test Automation](#introduction)
2. [Understanding the Technology Stack](#technology-stack)
3. [Project Structure Overview](#project-structure)
4. [Configuration Files Explained](#configuration-files)
5. [Page Object Model Deep Dive](#page-object-model)
6. [Test Files Detailed Explanation](#test-files)
7. [How Everything Works Together](#how-it-works)
8. [Running and Debugging Tests](#running-tests)
9. [Common Scenarios and Examples](#examples)
10. [Troubleshooting Guide](#troubleshooting)

---

## 1. Introduction to Test Automation {#introduction}

### What is Test Automation?
Test automation is the practice of using software tools to run tests automatically instead of manually clicking through a website. Think of it like this:

**Manual Testing (Old Way):**
- Open browser
- Type URL
- Click login button
- Type username
- Type password
- Click submit
- Check if login worked
- Repeat for every test case
- Takes 30+ minutes

**Automated Testing (Our Way):**
- Write code once
- Run command: `pytest tests/`
- All tests run automatically
- Takes 10-15 seconds
- Can run anytime, anywhere

### Why This Project?
This project automates testing for **saucedemo.com**, a demo e-commerce website. We test:
- Login functionality
- Shopping cart operations
- Checkout process
- Product sorting
- Logout functionality

---

## 2. Understanding the Technology Stack {#technology-stack}

### What is Python?
Python is a programming language that's easy to read and write. It looks almost like English.

**Example:**
```python
# This is Python code - very readable!
username = "standard_user"
password = "secret_sauce"
login_page.login(username, password)
```

**Why Python for Testing?**
- Easy to learn (great for beginners)
- Lots of testing libraries available
- Popular in QA automation industry
- Clean, readable syntax

### What is Playwright?
Playwright is a tool that controls web browsers automatically. It can:
- Open browsers (Chrome, Firefox, Safari)
- Click buttons
- Fill forms
- Read text from pages
- Take screenshots
- Wait for elements to load

**Think of Playwright as a robot that uses your website like a human would.**

**Example:**
```python
page.goto("https://www.saucedemo.com")  # Opens website
page.click("#login-button")              # Clicks login button
page.fill("#username", "john")           # Types username
```

### What is pytest?
pytest is a testing framework that:
- Finds and runs your tests
- Reports which tests passed/failed
- Provides fixtures (setup/teardown)
- Generates reports

**Example:**
```python
def test_login():
    # pytest automatically finds functions starting with "test_"
    assert login_successful == True
```

### What is Page Object Model (POM)?
POM is a design pattern that organizes code by separating:
- **Page Objects:** Code that interacts with web pages
- **Tests:** Code that performs test scenarios

**Without POM (Bad):**
```python
# Test file has all the locators and logic mixed
def test_login():
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
```

**With POM (Good):**
```python
# Test file is clean and readable
def test_login():
    login_page.login("standard_user", "secret_sauce")
```

---

## 3. Project Structure Overview {#project-structure}

### Complete Directory Structure
```
saucedemo-playwright-python/
│
├── pages/                          # Page Object Model classes
│   ├── __init__.py                # Makes 'pages' a Python package
│   ├── base_page.py               # Parent class with common methods
│   ├── login_page.py              # Login page interactions
│   ├── inventory_page.py          # Products page interactions
│   ├── cart_page.py               # Shopping cart interactions
│   └── checkout_page.py           # Checkout process interactions
│
├── tests/                          # Test cases
│   ├── __init__.py                # Makes 'tests' a Python package
│   ├── test_login.py              # Login tests (2 tests)
│   ├── test_cart.py               # Cart tests (2 tests)
│   ├── test_checkout.py           # Checkout tests (1 test)
│   ├── test_logout.py             # Logout tests (1 test)
│   └── test_sorting.py            # Sorting tests (1 test)
│
├── conftest.py                     # pytest fixtures and configuration
├── pytest.ini                      # pytest settings
├── requirements.txt                # Python dependencies
├── .gitignore                      # Files to ignore in git
├── README.md                       # Quick start guide
├── PROJECT_FAQ.md                  # FAQs and presentation guide
└── TEST_FIXES.md                   # Documentation of bug fixes

Total: 19 files
```

### What Each Folder Does

**pages/ folder:**
- Contains all Page Object classes
- Each file represents one page or section of the website
- Stores locators (how to find elements on page)
- Stores methods (actions you can perform)

**tests/ folder:**
- Contains all test cases
- Each file tests a specific feature
- Uses page objects to perform actions
- Contains assertions to verify results

---

## 4. Configuration Files Explained {#configuration-files}

### File: conftest.py
**Location:** Root directory  
**Purpose:** Shared pytest fixtures and configuration


**Complete Code:**
```python
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
```

**Line-by-Line Explanation:**

```python
import pytest
from playwright.sync_api import Page, Browser
```
- **Line 1:** Import pytest library
- **Line 2:** Import Playwright's Page and Browser classes

```python
@pytest.fixture(scope="function")
```
- **@pytest.fixture:** Decorator that marks this as a fixture
- **scope="function":** Run this fixture before EACH test function
- Other scopes: "class", "module", "session"

```python
def page(browser: Browser) -> Page:
```
- **def page:** Function name (tests will use this name)
- **browser: Browser:** Takes browser as input (provided by playwright-pytest)
- **-> Page:** Returns a Page object

```python
context = browser.new_context()
```
- Creates a new browser context (like an incognito window)
- Isolates each test (cookies, storage, etc.)

```python
page = context.new_page()
```
- Creates a new page/tab in the context

```python
yield page
```
- **yield:** Provides the page to the test
- Test runs here
- After test completes, code continues below

```python
context.close()
```
- Cleanup: Closes the browser context
- Runs after each test automatically

**Second Fixture:**
```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        }
    }
```
- **scope="session":** Runs once for entire test session
- Sets browser window size to 1280x720 pixels
- Ensures consistent viewport across all tests

---

### File: pytest.ini
**Location:** Root directory  
**Purpose:** pytest configuration settings


**Complete Code:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

**Line-by-Line Explanation:**

```ini
[pytest]
```
- Section header for pytest configuration

```ini
testpaths = tests
```
- **testpaths:** Where to look for tests
- **tests:** Only search in the "tests" folder
- Ignores other folders, making test discovery faster

```ini
python_files = test_*.py
```
- **python_files:** Which files contain tests
- **test_*.py:** Files starting with "test_" and ending with ".py"
- Examples: test_login.py ✓, login_test.py ✗

```ini
python_classes = Test*
```
- **python_classes:** Which classes contain tests
- **Test*:** Classes starting with "Test"
- Examples: TestLogin ✓, LoginTest ✗

```ini
python_functions = test_*
```
- **python_functions:** Which functions are tests
- **test_*:** Functions starting with "test_"
- Examples: test_valid_login ✓, valid_login_test ✗

```ini
addopts = -v --tb=short
```
- **addopts:** Additional options always applied
- **-v:** Verbose output (shows each test name)
- **--tb=short:** Short traceback on failures (less clutter)

**Example Output with -v:**
```
tests/test_login.py::TestLogin::test_valid_login PASSED
tests/test_login.py::TestLogin::test_invalid_login PASSED
```

**Without -v:**
```
.. (just dots)
```

---

### File: requirements.txt
**Location:** Root directory  
**Purpose:** List of Python packages needed

**Complete Code:**
```
pytest==7.4.3
pytest-playwright==0.4.3
playwright==1.40.0
pytest-html==4.1.1
```

**Line-by-Line Explanation:**

```
pytest==7.4.3
```
- **pytest:** Testing framework
- **==7.4.3:** Specific version (ensures consistency)
- Provides test discovery, fixtures, assertions

```
pytest-playwright==0.4.3
```
- **pytest-playwright:** Plugin that integrates Playwright with pytest
- Provides browser fixtures automatically
- Handles browser lifecycle

```
playwright==1.40.0
```
- **playwright:** Browser automation library
- Controls Chrome, Firefox, Safari
- Provides page interactions

```
pytest-html==4.1.1
```
- **pytest-html:** Generates HTML test reports
- Creates beautiful, readable reports
- Usage: `pytest --html=report.html`

**How to Install:**
```bash
pip install -r requirements.txt
```
This command reads the file and installs all packages.

---

### File: .gitignore
**Location:** Root directory  
**Purpose:** Tell git which files to ignore


**Complete Code:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Pytest
.pytest_cache/
htmlcov/
.coverage
*.html
assets/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**Section-by-Section Explanation:**

**Python Section:**
- `__pycache__/`: Compiled Python files (auto-generated)
- `*.py[cod]`: Compiled Python bytecode
- `venv/`: Virtual environment folder
- These are temporary files, don't need version control

**Pytest Section:**
- `.pytest_cache/`: pytest cache folder
- `htmlcov/`: HTML coverage reports
- `*.html`: Test report files
- Generated during test runs, can be recreated

**IDE Section:**
- `.vscode/`: VS Code settings
- `.idea/`: PyCharm settings
- Personal IDE preferences, not shared

**OS Section:**
- `.DS_Store`: Mac OS folder metadata
- `Thumbs.db`: Windows thumbnail cache
- Operating system files, not needed in repo

---

### File: __init__.py
**Location:** pages/ and tests/ folders  
**Purpose:** Mark directories as Python packages

**Complete Code:**
```python
# Pages package
```
or
```python
# Tests package
```

**Explanation:**

**What is a Python Package?**
A package is a folder that can be imported in Python.

**Without __init__.py:**
```python
from pages.login_page import LoginPage  # ERROR!
```

**With __init__.py:**
```python
from pages.login_page import LoginPage  # Works!
```

**Why Empty?**
- Modern Python (3.3+) doesn't require content
- Just needs to exist
- Can contain initialization code if needed

**Example with Content:**
```python
# pages/__init__.py
from .login_page import LoginPage
from .cart_page import CartPage

# Now you can do:
# from pages import LoginPage
```

---

## 5. Page Object Model Deep Dive {#page-object-model}

### File: pages/base_page.py
**Purpose:** Parent class with common methods used by all pages


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Import Statement:**
```python
from playwright.sync_api import Page
```
- Imports the Page class from Playwright
- Page represents a browser tab/window

**Class Definition:**
```python
class BasePage:
    """Base page class with common methods"""
```
- **class BasePage:** Creates a new class named BasePage
- **"""...""":** Docstring explaining the class purpose
- This will be the parent class for all page objects

**Constructor:**
```python
def __init__(self, page: Page):
    self.page = page
```
- **__init__:** Special method called when creating an object
- **page: Page:** Takes a Playwright Page object as parameter
- **self.page = page:** Stores the page for use in other methods
- **self:** Refers to the current instance of the class

**Example Usage:**
```python
login_page = LoginPage(page)  # __init__ is called here
```

**Method 1: navigate_to**
```python
def navigate_to(self, url: str):
    """Navigate to a URL"""
    self.page.goto(url)
```
- **def navigate_to:** Method name
- **url: str:** Takes a URL string as parameter
- **self.page.goto(url):** Playwright command to open URL
- **Purpose:** Opens a webpage

**Example:**
```python
base_page.navigate_to("https://www.saucedemo.com")
```

**Method 2: click**
```python
def click(self, selector: str):
    """Click an element"""
    self.page.click(selector)
```
- **selector: str:** CSS selector to find element
- **self.page.click:** Playwright command to click
- **Purpose:** Clicks a button, link, or any clickable element

**Example:**
```python
base_page.click("#login-button")  # Clicks element with id="login-button"
```

**What is a Selector?**
A selector is a way to find elements on a webpage:
- `#login-button` → Element with id="login-button"
- `.button` → Elements with class="button"
- `button[name='submit']` → Button with name="submit"

**Method 3: fill**
```python
def fill(self, selector: str, text: str):
    """Fill input field"""
    self.page.fill(selector, text)
```
- **selector:** Which input field to fill
- **text:** What text to type
- **Purpose:** Types text into input fields

**Example:**
```python
base_page.fill("#username", "john_doe")
```

**Method 4: get_text**
```python
def get_text(self, selector: str) -> str:
    """Get text from element"""
    return self.page.locator(selector).inner_text()
```
- **-> str:** Returns a string
- **locator(selector):** Finds the element
- **inner_text():** Gets the text inside element
- **Purpose:** Reads text from webpage

**Example:**
```python
error_message = base_page.get_text(".error")
print(error_message)  # "Invalid username or password"
```

**Method 5: is_visible**
```python
def is_visible(self, selector: str) -> bool:
    """Check if element is visible"""
    return self.page.locator(selector).is_visible()
```
- **-> bool:** Returns True or False
- **is_visible():** Checks if element is displayed
- **Purpose:** Verify if element is on screen

**Example:**
```python
if base_page.is_visible(".success-message"):
    print("Success message is showing!")
```

**Why BasePage is Important:**
1. **Code Reusability:** Write once, use everywhere
2. **Consistency:** All pages use same methods
3. **Maintainability:** Update one place, affects all pages
4. **Simplicity:** Child classes inherit these methods

---

### File: pages/login_page.py
**Purpose:** Handles all interactions with the login page


**Complete Code:**
```python
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for Login Page"""
    
    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/"
    
    def open(self):
        """Open login page"""
        self.navigate_to(self.url)
    
    def login(self, username: str, password: str):
        """Perform login"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_visible(self.ERROR_MESSAGE)
```

**Detailed Explanation:**

**Import Statement:**
```python
from pages.base_page import BasePage
```
- Imports the BasePage class we created earlier
- LoginPage will inherit from BasePage

**Class Definition:**
```python
class LoginPage(BasePage):
```
- **class LoginPage:** Creates LoginPage class
- **(BasePage):** Inherits from BasePage
- Gets all methods from BasePage (click, fill, etc.)

**Locators Section:**
```python
# Locators
USERNAME_INPUT = "#user-name"
PASSWORD_INPUT = "#password"
LOGIN_BUTTON = "#login-button"
ERROR_MESSAGE = "[data-test='error']"
```
- **Class variables:** Defined at class level
- **UPPERCASE:** Convention for constants
- **Purpose:** Store selectors in one place
- **Benefit:** Easy to update if UI changes

**Why Store Locators?**
```python
# Bad: Locator repeated everywhere
def login(self):
    self.fill("#user-name", "john")
    
def clear_username(self):
    self.clear("#user-name")  # If ID changes, update everywhere!

# Good: Locator in one place
USERNAME_INPUT = "#user-name"

def login(self):
    self.fill(self.USERNAME_INPUT, "john")
    
def clear_username(self):
    self.clear(self.USERNAME_INPUT)  # Change once, works everywhere!
```

**Constructor:**
```python
def __init__(self, page):
    super().__init__(page)
    self.url = "https://www.saucedemo.com/"
```
- **super().__init__(page):** Calls BasePage's __init__
- Initializes the parent class
- **self.url:** Stores the login page URL
- Specific to LoginPage

**Method 1: open**
```python
def open(self):
    """Open login page"""
    self.navigate_to(self.url)
```
- **self.navigate_to:** Method inherited from BasePage
- Opens the login page URL
- Simple wrapper for clarity

**Usage:**
```python
login_page = LoginPage(page)
login_page.open()  # Opens https://www.saucedemo.com/
```

**Method 2: login**
```python
def login(self, username: str, password: str):
    """Perform login"""
    self.fill(self.USERNAME_INPUT, username)
    self.fill(self.PASSWORD_INPUT, password)
    self.click(self.LOGIN_BUTTON)
```
- **Takes:** username and password as parameters
- **Step 1:** Fill username field
- **Step 2:** Fill password field
- **Step 3:** Click login button
- **Purpose:** Complete login action in one method

**Usage:**
```python
login_page.login("standard_user", "secret_sauce")
```

**This is the power of POM!** Instead of writing 3 lines in every test, we write 1 line.

**Method 3: get_error_message**
```python
def get_error_message(self) -> str:
    """Get error message text"""
    return self.get_text(self.ERROR_MESSAGE)
```
- **Returns:** Error message text as string
- **Uses:** get_text method from BasePage
- **Purpose:** Read error message after failed login

**Usage:**
```python
error = login_page.get_error_message()
print(error)  # "Epic sadface: Username and password do not match"
```

**Method 4: is_error_displayed**
```python
def is_error_displayed(self) -> bool:
    """Check if error message is displayed"""
    return self.is_visible(self.ERROR_MESSAGE)
```
- **Returns:** True if error visible, False if not
- **Uses:** is_visible method from BasePage
- **Purpose:** Check if error appeared

**Usage:**
```python
if login_page.is_error_displayed():
    print("Login failed!")
```

---

### File: pages/inventory_page.py
**Purpose:** Handles product page interactions


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Dynamic Locators:**
```python
ADD_TO_CART_BUTTON = "button[data-test='add-to-cart-{}']"
REMOVE_BUTTON = "button[data-test='remove-{}']"
```
- **{}:** Placeholder for dynamic value
- **Purpose:** One locator pattern for multiple items
- **Example:** 
  - "add-to-cart-sauce-labs-backpack"
  - "add-to-cart-sauce-labs-bike-light"

**Method: is_loaded**
```python
def is_loaded(self) -> bool:
    """Check if inventory page is loaded"""
    return self.is_visible(self.INVENTORY_CONTAINER)
```
- **Purpose:** Verify we're on the inventory page
- **Returns:** True if page loaded, False if not
- **Usage:** After login, check if redirected correctly

**Method: add_item_to_cart**
```python
def add_item_to_cart(self, item_name: str):
    """Add item to cart by name"""
    item_id = item_name.lower().replace(" ", "-")
    self.click(self.ADD_TO_CART_BUTTON.format(item_id))
```

**Step-by-Step:**
1. **Input:** "Sauce Labs Backpack"
2. **lower():** "sauce labs backpack"
3. **replace(" ", "-"):** "sauce-labs-backpack"
4. **format(item_id):** "button[data-test='add-to-cart-sauce-labs-backpack']"
5. **click:** Clicks the button

**Why This Approach?**
- User-friendly: Pass readable name
- Flexible: Works for any product
- Maintainable: One method for all products

**Method: get_cart_count**
```python
def get_cart_count(self) -> str:
    """Get cart badge count"""
    if self.is_visible(self.CART_BADGE):
        return self.get_text(self.CART_BADGE)
    return "0"
```
- **Checks:** Is cart badge visible?
- **If yes:** Return the number shown
- **If no:** Return "0" (empty cart)
- **Purpose:** Verify items added to cart

**Method: logout**
```python
def logout(self):
    """Perform logout"""
    self.click(self.MENU_BUTTON)
    self.page.wait_for_timeout(500)  # Wait for menu animation
    self.click(self.LOGOUT_LINK)
```
- **Step 1:** Click hamburger menu
- **Step 2:** Wait 500ms for menu to slide open
- **Step 3:** Click logout link
- **wait_for_timeout:** Explicit wait for animation

**Method: sort_products**
```python
def sort_products(self, option: str):
    """Sort products by option"""
    self.page.select_option(self.PRODUCT_SORT, option)
```
- **select_option:** Playwright method for dropdowns
- **Options:** "az", "za", "lohi", "hilo"
- **Purpose:** Change product sorting

**Method: get_first_product_name**
```python
def get_first_product_name(self) -> str:
    """Get first product name"""
    return self.page.locator(".inventory_item_name").first.inner_text()
```
- **locator(".inventory_item_name"):** Finds all product names
- **.first:** Gets only the first one
- **inner_text():** Extracts the text
- **Purpose:** Verify sorting worked

---

### File: pages/cart_page.py
**Purpose:** Handles shopping cart page interactions


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Locators:**
```python
CART_ITEMS = ".cart_item"
```
- **Purpose:** Finds all items in cart
- **Note:** Multiple elements with same class

```python
REMOVE_BUTTON = "button[name^='remove']"
```
- **[name^='remove']:** Attribute starts with "remove"
- **^=:** CSS selector for "starts with"
- **Matches:** name="remove-sauce-labs-backpack", etc.

**Method: get_cart_items_count**
```python
def get_cart_items_count(self) -> int:
    """Get number of items in cart"""
    return self.page.locator(self.CART_ITEMS).count()
```
- **locator(self.CART_ITEMS):** Finds all cart items
- **.count():** Returns number of elements found
- **Returns:** Integer (0, 1, 2, etc.)
- **Purpose:** Verify correct number of items

**Example:**
```python
count = cart_page.get_cart_items_count()
assert count == 2  # Verify 2 items in cart
```

**Method: proceed_to_checkout**
```python
def proceed_to_checkout(self):
    """Click checkout button"""
    self.click(self.CHECKOUT_BUTTON)
```
- Simple wrapper for clarity
- Moves to checkout page

**Method: continue_shopping**
```python
def continue_shopping(self):
    """Click continue shopping button"""
    self.click(self.CONTINUE_SHOPPING)
```
- Returns to products page
- Allows adding more items

---

### File: pages/checkout_page.py
**Purpose:** Handles checkout process


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Checkout Flow:**
Saucedemo checkout has 3 steps:
1. **Step 1:** Enter personal information
2. **Step 2:** Review order
3. **Step 3:** Confirmation

**Locators Organized by Step:**
```python
# Step 1 - Information
FIRST_NAME = "#first-name"
LAST_NAME = "#last-name"
POSTAL_CODE = "#postal-code"
CONTINUE_BUTTON = "#continue"
```
- Comments help organize related locators
- Clear which step each locator belongs to

**Method: fill_information**
```python
def fill_information(self, first_name: str, last_name: str, postal_code: str):
    """Fill checkout information"""
    self.fill(self.FIRST_NAME, first_name)
    self.fill(self.LAST_NAME, last_name)
    self.fill(self.POSTAL_CODE, postal_code)
    self.click(self.CONTINUE_BUTTON)
```
- **Takes:** 3 parameters (first name, last name, postal code)
- **Fills:** All 3 fields
- **Clicks:** Continue button
- **Purpose:** Complete Step 1 in one method call

**Usage:**
```python
checkout_page.fill_information("John", "Doe", "12345")
```

**Method: finish_checkout**
```python
def finish_checkout(self):
    """Click finish button"""
    self.click(self.FINISH_BUTTON)
```
- Completes Step 2
- Places the order

**Method: is_checkout_complete**
```python
def is_checkout_complete(self) -> bool:
    """Check if checkout is complete"""
    return self.is_visible(self.COMPLETE_HEADER)
```
- **Returns:** True if on confirmation page
- **Purpose:** Verify order was placed successfully

---

## 6. Test Files Detailed Explanation {#test-files}

### File: tests/test_login.py
**Purpose:** Test login functionality


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Import Statements:**
```python
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
```
- **pytest:** Testing framework
- **LoginPage:** Page object for login page
- **InventoryPage:** Page object for products page

**Test Class:**
```python
class TestLogin:
    """Test cases for login functionality"""
```
- **class TestLogin:** Groups related tests
- **Test prefix:** Required by pytest
- **Purpose:** Organize login tests together

**Test Method 1: test_valid_login**
```python
def test_valid_login(self, page):
    """Test login with valid credentials"""
```
- **test_ prefix:** Required by pytest
- **page parameter:** Fixture from conftest.py
- **Docstring:** Describes what test does

**Test Steps:**
```python
login_page = LoginPage(page)
inventory_page = InventoryPage(page)
```
- **Step 1:** Create page objects
- Pass the page fixture to each

```python
login_page.open()
```
- **Step 2:** Open login page

```python
login_page.login("standard_user", "secret_sauce")
```
- **Step 3:** Perform login
- Uses valid credentials

```python
assert inventory_page.is_loaded(), "User should be on inventory page after login"
```
- **Step 4:** Verify success
- **assert:** Checks if condition is True
- **If False:** Test fails with message
- **Purpose:** Confirm login worked

**What is assert?**
```python
assert True   # Test passes
assert False  # Test fails
assert 2 + 2 == 4  # Test passes
assert 2 + 2 == 5  # Test fails
```

**Test Method 2: test_invalid_login**
```python
def test_invalid_login(self, page):
    """Test login with invalid credentials"""
    login_page = LoginPage(page)
    
    login_page.open()
    login_page.login("invalid_user", "wrong_password")
    
    # Verify error message is displayed
    assert login_page.is_error_displayed(), "Error message should be displayed"
    error_text = login_page.get_error_message()
    assert "Username and password do not match" in error_text
```

**Test Steps:**
1. Create login page object
2. Open login page
3. Try to login with wrong credentials
4. Verify error message appears
5. Verify error message contains expected text

**Why Test Invalid Login?**
- Ensures security works
- Verifies error messages show
- Tests negative scenarios

---

### File: tests/test_cart.py
**Purpose:** Test shopping cart functionality


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Setup Fixture:**
```python
@pytest.fixture(autouse=True)
def setup(self, page):
    """Login before each test"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
```

**Breaking it down:**
- **@pytest.fixture:** Marks this as a fixture
- **autouse=True:** Runs automatically before each test
- **Purpose:** Login once, reuse for all tests in class

**Why autouse?**
```python
# Without autouse - must specify in each test
def test_add_items(self, page, setup):
    ...

def test_remove_items(self, page, setup):
    ...

# With autouse - runs automatically
def test_add_items(self, page):
    ...  # setup already ran!

def test_remove_items(self, page):
    ...  # setup already ran!
```

**Test Flow:**
1. **setup fixture runs:** Logs in
2. **test_add_items runs:** Already logged in
3. **setup fixture runs again:** Logs in fresh
4. **test_remove_items runs:** Already logged in

**Test: test_add_items_to_cart**
```python
inventory_page.add_item_to_cart("sauce-labs-backpack")
inventory_page.add_item_to_cart("sauce-labs-bike-light")
```
- Adds 2 items to cart

```python
cart_count = inventory_page.get_cart_count()
assert cart_count == "2", f"Cart should have 2 items, but has {cart_count}"
```
- **f"...":** F-string for formatted output
- **{cart_count}:** Inserts actual value
- **Example error:** "Cart should have 2 items, but has 1"

**Test: test_remove_items_from_cart**
```python
# Add items first
inventory_page.add_item_to_cart("sauce-labs-backpack")
inventory_page.add_item_to_cart("sauce-labs-bike-light")

# Remove one item
inventory_page.remove_item_from_cart("sauce-labs-backpack")

# Verify cart count
cart_count = inventory_page.get_cart_count()
assert cart_count == "1", f"Cart should have 1 item after removal"
```
- **Setup:** Add 2 items
- **Action:** Remove 1 item
- **Verify:** 1 item remains

---

### File: tests/test_checkout.py
**Purpose:** Test checkout process


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Setup Fixture:**
```python
@pytest.fixture(autouse=True)
def setup(self, page):
    """Login and add item before each test"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    inventory_page.open_cart()
```

**Setup Steps:**
1. Login
2. Add item to cart
3. Open cart page

**Why this setup?**
- Checkout requires items in cart
- Setup ensures preconditions met
- Test focuses on checkout, not setup

**Test: test_complete_checkout**

**Step 1: Proceed to checkout**
```python
cart_page.proceed_to_checkout()
```
- Clicks checkout button
- Moves to information page

**Step 2: Fill information**
```python
checkout_page.fill_information("John", "Doe", "12345")
```
- Fills first name, last name, postal code
- Clicks continue
- Moves to overview page

**Step 3: Finish checkout**
```python
checkout_page.finish_checkout()
```
- Clicks finish button
- Places order
- Moves to confirmation page

**Step 4: Verify completion**
```python
assert checkout_page.is_checkout_complete(), "Checkout should be complete"
confirmation = checkout_page.get_confirmation_message()
assert "Thank you for your order" in confirmation
```
- **First assert:** Checks confirmation page loaded
- **Second assert:** Verifies success message

**This is an End-to-End (E2E) test:**
- Tests complete user journey
- Multiple pages involved
- Verifies entire flow works

---

### File: tests/test_logout.py
**Purpose:** Test logout functionality


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Test Flow:**
1. Login
2. Verify logged in
3. Logout
4. Verify logged out

**Verification Method:**
```python
assert page.url == "https://www.saucedemo.com/"
```
- **page.url:** Current page URL
- **Checks:** URL is login page
- **Purpose:** Confirm logout redirected correctly

**Alternative Verification:**
```python
# Could also check if login button visible
assert login_page.is_visible(login_page.LOGIN_BUTTON)
```

---

### File: tests/test_sorting.py
**Purpose:** Test product sorting


**Complete Code:**
```python
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
```

**Detailed Explanation:**

**Sort Options:**
- **"az":** A to Z (alphabetical)
- **"za":** Z to A (reverse alphabetical)
- **"lohi":** Low to High (price)
- **"hilo":** High to Low (price)

**Test Logic:**
```python
inventory_page.sort_products("za")
```
- Sorts products Z to A

```python
first_product = inventory_page.get_first_product_name()
```
- Gets the first product name after sorting

```python
assert first_product == "Test.allTheThings() T-Shirt (Red)"
```
- Verifies the first product is correct
- "Test.allTheThings()" starts with "T"
- Should be first when sorted Z to A

**Why This Test?**
- Ensures sorting feature works
- Verifies UI updates correctly
- Tests JavaScript functionality

---

## 7. How Everything Works Together {#how-it-works}

### Test Execution Flow

**When you run:** `pytest tests/test_login.py::TestLogin::test_valid_login`

**Step-by-Step Process:**

**1. pytest Initialization**
```
pytest starts
├── Reads pytest.ini configuration
├── Discovers test files in tests/ folder
└── Finds test_login.py
```

**2. Fixture Setup (from conftest.py)**
```
@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    ├── Creates new browser context
    ├── Creates new page
    └── Yields page to test
```

**3. Test Execution**
```
test_valid_login(page):
    ├── Creates LoginPage(page)
    ├── Creates InventoryPage(page)
    ├── login_page.open()
    │   └── Calls navigate_to() from BasePage
    │       └── Calls page.goto(url)
    ├── login_page.login("standard_user", "secret_sauce")
    │   ├── Calls fill() from BasePage for username
    │   ├── Calls fill() from BasePage for password
    │   └── Calls click() from BasePage for button
    └── assert inventory_page.is_loaded()
        └── Calls is_visible() from BasePage
            └── Returns True/False
```

**4. Fixture Teardown**
```
After test completes:
└── context.close() runs
    └── Closes browser
```

**5. Test Result**
```
PASSED ✓ or FAILED ✗
└── pytest reports result
```

### Class Inheritance Diagram

```
BasePage (parent)
    ├── navigate_to()
    ├── click()
    ├── fill()
    ├── get_text()
    └── is_visible()
    
    ↓ inherits from
    
LoginPage (child)
    ├── All BasePage methods ✓
    ├── USERNAME_INPUT
    ├── PASSWORD_INPUT
    ├── open()
    ├── login()
    └── get_error_message()
    
    ↓ inherits from
    
InventoryPage (child)
    ├── All BasePage methods ✓
    ├── CART_BADGE
    ├── add_item_to_cart()
    ├── get_cart_count()
    └── logout()
```

### Data Flow Example

**Test Code:**
```python
login_page.login("standard_user", "secret_sauce")
```

**What Happens:**
```
1. test_login.py calls login()
   ↓
2. login_page.py receives call
   ↓
3. login() method executes:
   self.fill(self.USERNAME_INPUT, "standard_user")
   ↓
4. fill() is in BasePage (inherited)
   ↓
5. base_page.py executes:
   self.page.fill("#user-name", "standard_user")
   ↓
6. Playwright fills the input field
   ↓
7. Returns to login()
   ↓
8. Continues with password and click
   ↓
9. Returns to test
```

---

## 8. Running and Debugging Tests {#running-tests}

### Installation Steps

**Step 1: Install Python**
```bash
# Check if Python installed
python --version

# Should show: Python 3.10+ or higher
```

**Step 2: Install Dependencies**
```bash
# Navigate to project folder
cd saucedemo-playwright-python

# Install packages
pip install -r requirements.txt
```

**Step 3: Install Browsers**
```bash
# Install Playwright browsers
playwright install
```

### Running Tests

**Run All Tests:**
```bash
pytest tests/
```

**Output:**
```
tests/test_cart.py::TestCart::test_add_items_to_cart PASSED
tests/test_cart.py::TestCart::test_remove_items_from_cart PASSED
tests/test_checkout.py::TestCheckout::test_complete_checkout PASSED
tests/test_login.py::TestLogin::test_valid_login PASSED
tests/test_login.py::TestLogin::test_invalid_login PASSED
tests/test_logout.py::TestLogout::test_logout PASSED
tests/test_sorting.py::TestSorting::test_sort_products_by_name PASSED

=================== 7 passed in 10.78s ===================
```

**Run Specific Test File:**
```bash
pytest tests/test_login.py
```

**Run Specific Test:**
```bash
pytest tests/test_login.py::TestLogin::test_valid_login
```

**Run with Different Browser:**
```bash
pytest tests/ --browser firefox
pytest tests/ --browser webkit  # Safari
```

**Run in Headed Mode (See Browser):**
```bash
pytest tests/ --headed
```

**Run with Slow Motion:**
```bash
pytest tests/ --headed --slowmo 1000
```
- Slows down by 1000ms (1 second) per action
- Great for debugging

**Generate HTML Report:**
```bash
pytest tests/ --html=report.html
```
- Creates report.html file
- Open in browser to view

**Run Tests in Parallel:**
```bash
pytest tests/ -n 4
```
- Runs 4 tests simultaneously
- Requires: `pip install pytest-xdist`

**Stop on First Failure:**
```bash
pytest tests/ -x
```

**Show Print Statements:**
```bash
pytest tests/ -s
```

**Verbose Output:**
```bash
pytest tests/ -v
```

**Very Verbose:**
```bash
pytest tests/ -vv
```

### Debugging Tips

**Add Print Statements:**
```python
def test_login(self, page):
    login_page = LoginPage(page)
    print("Opening login page...")
    login_page.open()
    print("Logging in...")
    login_page.login("standard_user", "secret_sauce")
    print("Login complete!")
```

**Take Screenshots:**
```python
def test_login(self, page):
    login_page = LoginPage(page)
    login_page.open()
    page.screenshot(path="before_login.png")
    login_page.login("standard_user", "secret_sauce")
    page.screenshot(path="after_login.png")
```

**Add Waits:**
```python
# Wait for element
page.wait_for_selector("#login-button")

# Wait for timeout
page.wait_for_timeout(2000)  # 2 seconds

# Wait for URL
page.wait_for_url("**/inventory.html")
```

**Use Playwright Inspector:**
```bash
PWDEBUG=1 pytest tests/test_login.py
```
- Opens Playwright Inspector
- Step through test line by line
- Inspect elements

---

## 9. Common Scenarios and Examples {#examples}

### Scenario 1: Adding a New Test

**Goal:** Add test for empty cart

**Step 1: Choose test file**
```
tests/test_cart.py (cart-related test)
```

**Step 2: Add test method**
```python
def test_empty_cart(self, page):
    """Test that cart starts empty"""
    inventory_page = InventoryPage(page)
    cart_count = inventory_page.get_cart_count()
    assert cart_count == "0", "Cart should be empty initially"
```

**Step 3: Run test**
```bash
pytest tests/test_cart.py::TestCart::test_empty_cart
```

### Scenario 2: Adding a New Page Object

**Goal:** Add page object for product details page

**Step 1: Create file**
```
pages/product_details_page.py
```

**Step 2: Write page object**
```python
from pages.base_page import BasePage

class ProductDetailsPage(BasePage):
    """Page Object for Product Details Page"""
    
    # Locators
    PRODUCT_NAME = ".inventory_details_name"
    PRODUCT_PRICE = ".inventory_details_price"
    ADD_TO_CART = "#add-to-cart"
    
    def get_product_name(self) -> str:
        """Get product name"""
        return self.get_text(self.PRODUCT_NAME)
    
    def get_product_price(self) -> str:
        """Get product price"""
        return self.get_text(self.PRODUCT_PRICE)
    
    def add_to_cart(self):
        """Add product to cart"""
        self.click(self.ADD_TO_CART)
```

**Step 3: Use in test**
```python
from pages.product_details_page import ProductDetailsPage

def test_product_details(self, page):
    # ... navigate to product ...
    details_page = ProductDetailsPage(page)
    name = details_page.get_product_name()
    assert name == "Sauce Labs Backpack"
```

### Scenario 3: Parameterized Tests

**Goal:** Test login with multiple users

```python
import pytest

class TestLogin:
    @pytest.mark.parametrize("username,password", [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
    ])
    def test_multiple_users(self, page, username, password):
        """Test login with different users"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        login_page.open()
        login_page.login(username, password)
        
        assert inventory_page.is_loaded()
```

**This runs 3 tests:**
- test_multiple_users[standard_user-secret_sauce]
- test_multiple_users[problem_user-secret_sauce]
- test_multiple_users[performance_glitch_user-secret_sauce]

---

## 10. Troubleshooting Guide {#troubleshooting}

### Common Errors and Solutions

**Error 1: ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'playwright'
```

**Solution:**
```bash
pip install -r requirements.txt
playwright install
```

**Error 2: Timeout**
```
TimeoutError: Timeout 30000ms exceeded
```

**Solutions:**
```python
# Increase timeout
page.click("#button", timeout=60000)  # 60 seconds

# Add explicit wait
page.wait_for_selector("#button")
page.click("#button")

# Check if element exists
if page.is_visible("#button"):
    page.click("#button")
```

**Error 3: Element Not Found**
```
Error: Element not found: #login-button
```

**Solutions:**
```python
# Check selector is correct
# Use Playwright Inspector
PWDEBUG=1 pytest tests/test_login.py

# Wait for element
page.wait_for_selector("#login-button")

# Check if on correct page
print(page.url)
```

**Error 4: Strict Mode Violation**
```
Error: strict mode violation: locator resolved to 2 elements
```

**Solution:**
```python
# Use .first, .last, or .nth()
page.locator(".button").first.click()
page.locator(".button").nth(1).click()

# Or use more specific selector
page.click("#specific-button")
```

**Error 5: Tests Pass Locally, Fail in CI**
```
Tests work on my machine but fail in CI/CD
```

**Solutions:**
```python
# Add explicit waits
page.wait_for_load_state("networkidle")

# Use headless mode locally to test
pytest tests/ --browser chromium --headless

# Check viewport size
# Set in conftest.py
```

### Best Practices

**1. Keep Tests Independent**
```python
# Bad: Tests depend on each other
def test_1_login():
    login()

def test_2_add_to_cart():  # Assumes test_1 ran
    add_item()

# Good: Each test is independent
def test_login():
    login()
    assert logged_in

def test_add_to_cart():
    login()  # Setup in this test
    add_item()
    assert item_added
```

**2. Use Meaningful Names**
```python
# Bad
def test_1():
    ...

# Good
def test_valid_login_redirects_to_inventory_page():
    ...
```

**3. One Assert Per Concept**
```python
# Acceptable
def test_login():
    login()
    assert inventory_page.is_loaded()
    assert inventory_page.get_cart_count() == "0"

# Better: Split into two tests
def test_login_redirects_to_inventory():
    login()
    assert inventory_page.is_loaded()

def test_cart_starts_empty():
    login()
    assert inventory_page.get_cart_count() == "0"
```

**4. Use Setup Fixtures**
```python
# Avoid repetition
@pytest.fixture(autouse=True)
def setup(self, page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
```

**5. Keep Page Objects Simple**
```python
# Page objects should not have assertions
# Bad
def login(self, username, password):
    self.fill(self.USERNAME, username)
    self.fill(self.PASSWORD, password)
    self.click(self.LOGIN_BUTTON)
    assert self.is_logged_in()  # No!

# Good
def login(self, username, password):
    self.fill(self.USERNAME, username)
    self.fill(self.PASSWORD, password)
    self.click(self.LOGIN_BUTTON)
    # Test will do assertions
```

---

## Summary

This framework demonstrates:
- **Modern automation:** Playwright + Python
- **Design pattern:** Page Object Model
- **Best practices:** Fixtures, inheritance, organization
- **Real-world testing:** E-commerce application
- **Maintainability:** Easy to extend and modify

**Key Takeaways:**
1. Page objects separate UI logic from tests
2. BasePage provides reusable methods
3. Fixtures handle setup/teardown
4. Tests are independent and focused
5. Configuration files control behavior

**Next Steps:**
- Add more test cases
- Implement data-driven testing
- Add API testing
- Integrate with CI/CD
- Add visual testing
- Implement parallel execution

---

**Document Version:** 1.0  
**Created:** For learning and demonstration  
**Total Pages:** Comprehensive guide covering all aspects  
**Audience:** Beginners to intermediate QA engineers
