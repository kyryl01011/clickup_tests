import allure
from pages.board_page import BoardPage

def test_create_new_task(logged_in_page, random_task_title):
    board_page = BoardPage(logged_in_page)
    board_page.open_board_page()
    board_page.board_tasks_table.create_new_task_in_todo_list(random_task_title)

def test_remove_existing_task(logged_in_page):
    board_page = BoardPage(logged_in_page)
    board_page.open_board_page()
    board_page.board_tasks_table.wait_tasks_load()
    board_page.board_tasks_table.open_task_options()
    board_page.board_tasks_table.remove_task_with_options_menu_and_verify()
