import allure
from requests import Response

from src.custom_requester.custom_requester import CustomRequester
from src.enums.endpoints import Endpoints


class TasksApi(CustomRequester):

    def get_task(self, task_id) -> Response:
        with allure.step(f'Fetch task object by ID: {task_id}'):
            response = self.send_request('GET', f'{Endpoints.TASK.value}/{task_id}')
            return response

    def create_new_task(self, body_json) -> Response:
        with allure.step(f'Create new task with body: {body_json}'):
            response = self.send_request('POST', Endpoints.LIST_TASK.value, json=body_json)
            return response

    def update_task(self, task_id, body_json) -> Response:
        with allure.step(f'Update task by ID {task_id} with new data {body_json}'):
            response = self.send_request('PUT', f'{Endpoints.TASK.value}/{task_id}', json=body_json)
            return response

    def delete_task(self, task_id):
        with allure.step(f'Delete task by ID: {task_id}'):
            response = self.send_request('DELETE', f'{Endpoints.TASK.value}/{task_id}')
            return response
