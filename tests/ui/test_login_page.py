import allure
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD
from pages.login_page import LoginPage

def test_login(page):
    login_page = LoginPage(page)
    login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

def test_negative_login(page):
    password = '1111ssss'
    login_page = LoginPage(page)
    login_page.login(CLICKUP_EMAIL, password, 'negative')
