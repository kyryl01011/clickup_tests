import allure
from src.pages.base_page import BasePage
from playwright.sync_api import TimeoutError as PWTimeoutError

@allure.feature('Base UI login page actions')
class LoginPage(BasePage):
    EMAIL_INPUT_SELECTOR = 'input#login-email-input'
    PASSWORD_INPUT_SELECTOR = 'input#login-password-input'
    LOGIN_BUTTON_SELECTOR = 'button >> span:has-text("Log In")'
    DROPDOWN_USER_MENU_SELECTOR = 'cu3-icon >> svg >> use'
    ERROR_MESSAGE_SELECTOR = 'span[data-test="form__error"]'
    CAPTCHA_SELECTOR = 'div.login-page-new__main-form-recaptcha-inner'

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/login'

    @allure.description('Check if login through UI works properly')
    def login(self, email, password, test_type='positive'):
        self.navigate_and_wait_url(self._get_page_url)
        self.wait_selector_and_fill(self.EMAIL_INPUT_SELECTOR, email)
        self.wait_selector_and_type(self.PASSWORD_INPUT_SELECTOR, password)
        self.click_button(self.LOGIN_BUTTON_SELECTOR)
        try:
            self.wait_element_appear(self.CAPTCHA_SELECTOR, timeout=5555)
        except PWTimeoutError:
            pass
        # in case captcha appear to solve manually
        if self.page.locator(self.CAPTCHA_SELECTOR).is_visible():
            self.page.pause()
        if test_type == 'positive':
            self.wait_element_appear(self.DROPDOWN_USER_MENU_SELECTOR)
        else:
            self.assert_element_is_visible(self.ERROR_MESSAGE_SELECTOR)
