import time

import allure
from pages.base_page import BasePage
from utils.helpers import CLICKUP_TEAM_ID


class BoardTasksTableFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)

    BOARD_SELECTOR = 'ul.board-division__group-list' # selector of general board that contains board groups in it
    BOARD_GROUP_SELECTOR = 'div.board-group' # for example 'to-do' or 'completed' list is board group
    TASKS_SELECTOR = f'{BOARD_SELECTOR} >> {BOARD_GROUP_SELECTOR} >> li[data-source="task"]'
    DELETE_TASK_BUTTON_SELECTOR = 'a[data-test="quick-actions-menu__delete-task"]'
    ASSIGN_ICON_IN_TASK_SELECTOR = f'{TASKS_SELECTOR} >> cu-board-task-field-layout'
    NEW_TASK_BUTTON_SELECTOR = 'button[data-test="board-group__create-task-button__Add Task"]'
    NEW_TASK_TITLE_INPUT_SELECTOR = 'input[data-test="quick-create-task-panel__panel-board__input"]'
    CONFIRM_NEW_TASK_CREATION_SELECTOR = 'button[data-test="quick-create-task-panel__panel-board__enter-button"]'

    @allure.description('Wait tasks to load')
    def wait_tasks_load(self):
        self.wait_element_appear(self.ASSIGN_ICON_IN_TASK_SELECTOR)

    @allure.description('Open task options with RMB')
    def open_task_options(self):
        self.click_button(self.TASKS_SELECTOR, 'right')
        self.assert_element_exists_on_page(self.DELETE_TASK_BUTTON_SELECTOR)
        time.sleep(1)

    @allure.description('Create new task in to-do list from board page')
    def create_new_task_in_todo_list(self, random_task_title):
        new_task_selector = f'a[data-test="board-task__name-link__{random_task_title}"]'
        amount_of_tasks = self.amount_of_elements(self.TASKS_SELECTOR)
        self.click_button(self.NEW_TASK_BUTTON_SELECTOR)
        self.wait_selector_and_type(self.NEW_TASK_TITLE_INPUT_SELECTOR, random_task_title)
        self.click_button(self.CONFIRM_NEW_TASK_CREATION_SELECTOR)
        self.wait_element_appear(new_task_selector)

    @allure.description('Remove existing task from board page')
    def remove_task_with_options_menu_and_verify(self):
        amount_of_tasks = self.amount_of_elements(self.TASKS_SELECTOR)
        self.click_button(self.DELETE_TASK_BUTTON_SELECTOR)
        time.sleep(3)
        assert amount_of_tasks - 1 == self.amount_of_elements(self.TASKS_SELECTOR)


@allure.feature('UI Board page actions')
class BoardPage(BasePage):


    def __init__(self, page):
        super().__init__(page)
        self._endpoint = f'/{CLICKUP_TEAM_ID}/v/b/t/{CLICKUP_TEAM_ID}'
        self.board_tasks_table = BoardTasksTableFragment(page)

    @allure.description('Open Board page')
    def open_board_page(self):
        self.navigate_and_wait_url(self._get_page_url)

