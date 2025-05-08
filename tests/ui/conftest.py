from playwright.sync_api import sync_playwright, Page
import pytest
import allure

from pages.login_page import LoginPage
from utils.helpers import CLICKUP_PASSWORD, CLICKUP_EMAIL
from faker import Faker

fake = Faker()

@pytest.fixture(scope='session')
#@allure.step('Initialize playwright and browser, stop after tests done')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
#@allure.step('Create fresh page for tests')
def page(browser):
    page = browser.new_page()
    yield(page)
    page.close()

@pytest.fixture
#@allure.step('Create logged-in page object')
def logged_in_page(page: Page):
    login_page = LoginPage(page)
    login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)
    return page

@pytest.fixture
def random_task_title():
    return  fake.user_name()