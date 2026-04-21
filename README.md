# Saucedemo Automation Project

This is my learning project for Playwright with Python using Page Object Model (POM) pattern.

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Running Tests

Run all tests:
```bash
pytest tests/
```

Run with HTML report:
```bash
pytest tests/ --html=report.html
```

Run specific test:
```bash
pytest tests/test_login.py
```

## Project Structure

- `pages/` - Page Object Model classes
- `tests/` - Test cases
- `conftest.py` - Pytest fixtures and configuration
- `requirements.txt` - Project dependencies

## Test Cases Covered

1. Valid login
2. Invalid login
3. Add items to cart
4. Remove items from cart
5. Checkout process
6. Logout functionality
7. Product sorting

## Notes

- Using standard_user credentials for most tests
- Tests are independent and can run in any order
