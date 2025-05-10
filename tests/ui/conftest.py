from playwright.sync_api import sync_playwright, Page
import pytest
import allure

from pages.login_page import LoginPage
from utils.helpers import CLICKUP_PASSWORD, CLICKUP_EMAIL
from faker import Faker

fake = Faker()



# @pytest.fixture
# def random_task_title():
#     return  fake.user_name()