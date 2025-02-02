import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def mock_browser():
    """Fixture for mocked browser instance"""
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()
