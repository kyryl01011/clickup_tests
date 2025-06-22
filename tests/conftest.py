import allure
import pytest
import requests

from src.api.api_manager import ApiManager
from src.data_models.tasks import CreatedTaskModel
from src.consts.request_components import BASE_HEADERS
from src.scenarios.tasks.tasks import TasksScenarios
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
@pytest.fixture
def task_data(tasks_scenarios):

    def _generate_task_data():
        generated_task_data = DataGenerator.generate_task_data()
        allure.attach(
            str(generated_task_data.model_dump()),
            name='Generated data',
            attachment_type=allure.attachment_type.JSON)
        return generated_task_data

    yield _generate_task_data

    # Teardown / Delete all existing initialized tasks by ids
    for task_id in CreatedTaskModel.created_tasks_set:
        tasks_scenarios.delete_task_by_id(task_id)
