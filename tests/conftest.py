import allure
import requests
import pytest
from playwright.sync_api import sync_playwright

from api.api_manager import ApiManager
from enums.consts import BASE_HEADERS
from pages.login_page import LoginPage
from utils.data_generator import DataGenerator
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD

# API FIXTURES

@pytest.fixture(scope='session')
@allure.title('Create authorized session')
def authed_session():
    new_session = ApiManager(requests.Session())
    new_session.session.headers.update(BASE_HEADERS)
    allure.attach(str(BASE_HEADERS), name='Auth session headers', attachment_type=allure.attachment_type.JSON)
    yield new_session
    new_session.session.close()

@pytest.fixture()
@allure.title('Generate task data')
def task_data(authed_session):
    created_tasks = []

    def _generate_task_data():
        generated_task_data = {'name': f'{DataGenerator.generate_random_word()}{DataGenerator.generate_random_int()}'}
        allure.attach(str(generated_task_data), name='Generated data', attachment_type=allure.attachment_type.JSON)
        created_tasks.append(generated_task_data['name'])
        return generated_task_data

    yield _generate_task_data

    all_tasks_list = authed_session.tasks_api.get_all_tasks().json()['tasks']
    allure.attach(str(all_tasks_list), name='Tasks to remove', attachment_type=allure.attachment_type.JSON)
    for task_name in created_tasks:
        for task in all_tasks_list:
            if task['name'] == task_name:
                authed_session.tasks_api.delete_task(task['id'])
                allure.attach(str(task['id']), name='ID of removed task', attachment_type=allure.attachment_type.JSON)

@pytest.fixture()
@allure.title('Create new task with fixture')
def created_task(authed_session,task_data):
    def _create_task():
        random_task_data = task_data()
        created_task_response = authed_session.tasks_api.create_new_task(random_task_data)
        allure.attach(str(created_task_response.text), name='Created task data', attachment_type=allure.attachment_type.JSON)
        return created_task_response
    return _create_task

# UI FIXTURES

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
