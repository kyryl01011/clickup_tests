import allure
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD
from pages.login_page import LoginPage

class TestLoginUI:

    @allure.description('Successfully login with creds')
    def test_successful_login(self, page):
        login_page = LoginPage(page)
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    @allure.description('Login with wrong password and validate expected error appears')
    def test_negative_login(self, page):
        password = '1111ssss'
        login_page = LoginPage(page)
        login_page.login(CLICKUP_EMAIL, password, 'negative')
