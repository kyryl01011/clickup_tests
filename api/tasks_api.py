import allure

from custom_requester.custom_requester import CustomRequester
from utils.helpers import CLICKUP_LIST_ID


@allure.feature('Tasks Management')
class TasksApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session)

    def get_task(self, task_id) -> dict:
        response = self.send_request('GET', self._get_url(f'/task/{task_id}'))
        return response

    @allure.description(f'Fetch all tasks in list: {CLICKUP_LIST_ID}')
    def get_all_tasks(self) -> dict:
        response = self.send_request('GET', self._get_url(f'/list/{CLICKUP_LIST_ID}/task'))
        return response

    def create_new_task(self, body_json, expected_status_code=200) -> dict:
        response = self.send_request('POST', self._get_url(f'/list/{CLICKUP_LIST_ID}/task'), json=body_json, expected_status_code=expected_status_code)
        return response

    def update_task(self, task_id, body_json) -> dict:
        response = self.send_request('PUT', self._get_url(f'/task/{task_id}'), json=body_json)
        return response

    def delete_task(self, task_id):
        response = self.send_request('DELETE', self._get_url(f'/task/{task_id}'), expected_status_code=204)
        return response