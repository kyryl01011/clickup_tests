import allure
import pytest
import requests

from src.api.api_manager import ApiManager
from src.enums.consts import BASE_HEADERS
from src.scenarios.tasks import TasksScenarios
from src.utils.data_generator import DataGenerator


@allure.title('Create session')
@pytest.fixture(scope='session')
def session():
    new_session = requests.Session()
    new_session.headers.update(BASE_HEADERS)
    allure.attach(str(BASE_HEADERS), name='Auth session headers', attachment_type=allure.attachment_type.JSON)

    yield new_session

    new_session.close()


@allure.title('Create API manager object')
@pytest.fixture(scope='session')
def api_manager(session):
    api_manager = ApiManager(session)
    return api_manager


@allure.title('Create Tasks Scenarios object')
@pytest.fixture(scope='session')
def tasks_scenarios(api_manager):
    scenarios = TasksScenarios(api_manager)
    return scenarios


@allure.title('Generate task data')
@pytest.fixture()
def task_data(tasks_scenarios):
    created_tasks = []

    def _generate_task_data():
        generated_task_data = DataGenerator.generate_task_data()
        allure.attach(
            str(generated_task_data.model_dump()),
            name='Generated data',
            attachment_type=allure.attachment_type.JSON)
        created_tasks.append(generated_task_data.name)
        return generated_task_data

    yield _generate_task_data

    # all_tasks_list = authed_session.tasks_api.get_all_tasks().json()['tasks']
    # allure.attach(str(all_tasks_list), name='Tasks to remove', attachment_type=allure.attachment_type.JSON)
    # for task_name in created_tasks:
    #     for task in all_tasks_list:
    #         if task['name'] == task_name:
    #             authed_session.tasks_api.delete_task(task['id'])
    #             allure.attach(str(task['id']), name='ID of removed task', attachment_type=allure.attachment_type.JSON)
