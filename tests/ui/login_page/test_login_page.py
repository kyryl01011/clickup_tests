import allure
import pytest

from src.pages.login_page import LoginPage
from src.utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


@allure.feature('Login page')
@pytest.mark.ui
class TestLoginUI:

    @allure.title('Successful login with UI')
    @allure.description('Successfully login with creds')
    def test_successful_login(self, page):
        login_page = LoginPage(page)
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    @allure.title('Negative login with UI')
    @allure.description('Login with wrong password and validate expected error appears')
    def test_negative_login(self, page):
        password = '1111ssss'
        login_page = LoginPage(page)
        login_page.login(CLICKUP_EMAIL, password, 'negative')
