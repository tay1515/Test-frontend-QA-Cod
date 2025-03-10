import pytest
from playwright.sync_api import sync_playwright

#@pytest.fixture()
#def set_up_tear_down(page) -> None:
#    page.goto('https://www.saucedemo.com/')
#    yield page

@pytest.fixture(scope="session")
def set_up_tear_down():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel='chrome', slow_mo=1000)
        page = browser.new_page()
        yield page
        browser.close()