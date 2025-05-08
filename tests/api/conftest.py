import requests
import pytest

from api.api_manager import ApiManager
from enums.consts import BASE_HEADERS
from utils.data_generator import DataGenerator


@pytest.fixture(scope='session')
def authed_session():
    new_session = ApiManager(requests.Session())
    new_session.session.headers.update(BASE_HEADERS)
    yield new_session
    new_session.session.close()

@pytest.fixture()
def task_data(authed_session):
    created_tasks = []

    def _generate_task_data():
        generated_task_data = {'name': f'{DataGenerator.generate_random_word()}{DataGenerator.generate_random_int()}'}
        created_tasks.append(generated_task_data['name'])
        return generated_task_data

    yield _generate_task_data

    all_tasks_list = authed_session.tasks_api.get_all_tasks().json()['tasks']
    for task_name in created_tasks:
        for task in all_tasks_list:
            if task['name'] == task_name:
                authed_session.tasks_api.delete_task(task['id'])