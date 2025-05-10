import allure
from playwright.sync_api import Page, expect
from actions.page_actions import PageActions
from utils.helpers import CLICKUP_TEAM_ID

@allure.feature('Base UI actions')
class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.__base_url = 'https://app.clickup.com'
        self._endpoint = ''
        self.actions = PageActions(page)

    @property
    def _get_page_url(self):
        return self.__base_url + self._endpoint
    
    @_get_page_url.setter
    def _get_page_url(self, endpoint):
        self._endpoint = endpoint

    # @property
    # def _get_all_tasks_table_url(self):
    #     with allure.step(f'Generate all-tasks table URL'):
    #         return f'{self.__base_url}/{CLICKUP_TEAM_ID}/v/b/t/{CLICKUP_TEAM_ID}'

    def navigate_and_wait_url(self, url):
        with allure.step(f'Load URL - {url}'):
            self.page.goto(url, timeout=60000)
            self.page.wait_for_load_state('load')
            expect(self.page).to_have_url(url)

    def click_button(self, selector, button='left'):
        with allure.step(f'Click element with selector "{selector}"'):
            self.page.click(selector, button=button)

    def wait_element_appear(self, selector, timeout=30000):
        with allure.step(f'Wait element "{selector}" to appear'):
            self.page.wait_for_selector(selector, timeout=timeout)

    def wait_element_by_role_to_appear(self, role, name):
        with allure.step(f'Wait element with role {role} and name {name} to appear'):
            self.page.get_by_role(role, name=name)

    def wait_element_to_disappear(self, selector):
        with allure.step(f'Wait element "{selector}" to disappear'):
            self.page.wait_for_selector(selector, state='hidden')
        
    def wait_selector_and_fill(self, selector, text):
        with allure.step(f'Fill {selector} with "{text}"'):
            self.page.wait_for_selector(selector)
            self.page.fill(selector, text)

    def wait_selector_and_type(self, selector, text):
        with allure.step(f'Type in {selector} with "{text}"'):
            self.page.wait_for_selector(selector)
            self.page.type(selector, text)

    def wait_some_time(self, time):
        with allure.step(f'Wait for {time}ms'):
            self.page.wait_for_timeout(time)

    def assert_element_to_contain_text(self, selector, text):
        expect(self.page.locator(selector)).to_contain_text(text)

    def amount_of_elements(self, selector):
        with allure.step(f'Get amount of elements with selector {selector}'):
            return self.page.locator(selector).count()

    def assert_text_exists_on_page(self, text):
        with allure.step(f'Check if "{text}" exists on page'):
            expect(self.page.locator('body')).to_contain_text(text)

    def assert_element_exists_on_page(self, selector):
        with allure.step(f'Check if element {selector} exists on page'):
            expect(self.page.locator(selector))

    def assert_element_is_visible(self, selector):
        with allure.step(f'Check if element {selector} is visible'):
            self.page.is_visible(selector)
            