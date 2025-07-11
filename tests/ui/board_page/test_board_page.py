import allure
import pytest

from src.pages.board_page import BoardPage


@pytest.mark.ui
class TestTasksUI:

    @allure.title('Create new task with random data with UI')
    @allure.description('Create new task with generated random data and verify creation with UI')
    def test_create_new_task(self, logged_in_page, task_data):
        random_task_title = task_data().name
        board_page = BoardPage(logged_in_page)
        board_page.open_board_page()
        board_page.board_tasks_table.create_new_task_in_todo_list(random_task_title)

    @allure.title('Remove existing task with UI')
    @allure.description('Remove newly created task')
    def test_remove_existing_task(self, logged_in_page, tasks_scenarios, task_data):
        generated_data = task_data()
        tasks_scenarios.create_task(generated_data)
        board_page = BoardPage(logged_in_page)
        board_page.open_board_page()
        board_page.board_tasks_table.wait_tasks_load()
        board_page.board_tasks_table.open_task_options()
        board_page.board_tasks_table.remove_task_with_options()
