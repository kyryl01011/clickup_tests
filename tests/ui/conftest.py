import allure
import pytest
from playwright.sync_api import sync_playwright

from src.pages.login_page import LoginPage
from src.utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


@allure.title('Initialize playwright and browser, stop after tests done')
@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=300)
    yield browser
    browser.close()
    playwright.stop()


@allure.title('Create fresh page for tests')
@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@allure.title('Create logged-in page object')
@pytest.fixture
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)
    return page
