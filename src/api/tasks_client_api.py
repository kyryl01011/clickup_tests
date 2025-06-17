import allure
from requests import Response

from src.custom_requester.custom_requester import CustomRequester
from src.utils.helpers import CLICKUP_LIST_ID


class TasksApi(CustomRequester):

    def get_task(self, task_id) -> Response:
        with allure.step(f'Fetch task object by ID: {task_id}'):
            response = self.send_request('GET', f'/task/{task_id}')
            return response

    @allure.description(f'Fetch all tasks in list: {CLICKUP_LIST_ID}')
    def get_all_tasks(self) -> Response:
        with allure.step(f'Fetch all tasks in list: {CLICKUP_LIST_ID}'):
            response = self.send_request('GET', f'/list/{CLICKUP_LIST_ID}/task')
            return response

    def create_new_task(self, body_json) -> Response:
        with allure.step(f'Create new task with body: {body_json}'):
            response = self.send_request('POST', f'/list/{CLICKUP_LIST_ID}/task', json=body_json)
            return response

    def update_task(self, task_id, body_json) -> Response:
        with allure.step(f'Update task by ID {task_id} with new data {body_json}'):
            response = self.send_request('PUT', f'/task/{task_id}', json=body_json)
            return response

    def delete_task(self, task_id):
        with allure.step(f'Delete task by ID: {task_id}'):
            response = self.send_request('DELETE', f'/task/{task_id}')
            return response
