import allure
import pytest

from src.data_models.errors import BasicErrorModel
from tests.conftest import task_data
from src.utils.data_generator import DataGenerator


@allure.title('Manage tasks API')
@allure.feature('Manage tasks')
class TestTasks:

    def test_create_task(self, tasks_scenarios, task_data):
        generated_task_data = task_data()
        tasks_scenarios.create_task(generated_task_data)

    @allure.description('Get all existing tasks')
    def test_get_all_tasks(self, authed_session):
        all_tasks = authed_session.tasks_api.get_all_tasks()
        print(all_tasks.json())
        assert type(all_tasks.json()[
                        'tasks']) is list, f'Unexpected type of response: {type(all_tasks.json()['tasks'])}, expected list'
        return all_tasks.json()['tasks']

    @allure.description('Generates new task and check if task with such data exists using ID')
    def test_get_task(self, tasks_scenarios, task_data):
        generated_task_data = task_data()
        created_task_model = tasks_scenarios.create_task(generated_task_data)
        tasks_scenarios.get_task_by_id(created_task_model.id)

    @allure.description('Generates random ID and check if error message and code equals to expected')
    @pytest.mark.parametrize(
        'expected_err_message, expected_err_code',
        [
            (('Team not authorized', 'Team(s) not authorized'), ('OAUTH_023', 'OAUTH_027'))
        ]
    )
    def test_negative_get_task(self, tasks_scenarios, task_data, expected_err_message, expected_err_code):
        random_id = DataGenerator.generate_random_int()
        tasks_scenarios.negative_get_task_by_id(
            random_id,
            expected_error_msg=expected_err_message,
            expected_error_code=expected_err_code)

    @allure.description('Generates random task data and create task with it, verify if data matches')
    def test_successful_create_new_task(self, tasks_scenarios, task_data):
        generated_task_data = task_data()
        tasks_scenarios.create_task(generated_task_data)

    @allure.description(
        'Create task with wrong name, parent ID, link ID and validate that errors are equal to expected')
    @pytest.mark.parametrize(
        'invalid_data, expected_status_code, expected_err_message, expected_err_code',
        [
            ({'name': ''}, 400, 'Task name invalid', 'INPUT_005'),
            ({'name': DataGenerator.generate_random_word(), "parent": DataGenerator.generate_random_int()}, 400,
             'Parent not child of list', 'ITEM_137'),
            ({'name': DataGenerator.generate_random_word(), "links_to": DataGenerator.generate_random_int()}, 401,
             'You do not have access to this task', 'ACCESS_083')
        ]
    )
    def test_negative_create_new_task(self, tasks_scenarios, task_data, invalid_data, expected_status_code,
                                      expected_err_message,
                                      expected_err_code):
        generate_data_model = task_data()
        generate_data_model.model_copy(update=invalid_data, deep=True)
        tasks_scenarios.negative_create_task(
            invalid_data,
            expected_status_code,
            expected_err_message,
            expected_err_code)

    @allure.description(
        'Create new task with generated data, '
        'updates it and validate if not equal to initial and equal to newly generated')
    def test_successful_update_task(self, tasks_scenarios, task_data):
        init_task_model = task_data()
        new_task_data = task_data()
        tasks_scenarios.create_and_update_task(init_task_model, new_task_data)

    @allure.description(
        'Generates random task ID and to access it with update request, '
        'validate to receive expected error message and code')
    @pytest.mark.parametrize(
        'invalid_data, expected_status_code, expected_err_message, expected_err_code',
        [
            ({'name': ''}, 401, 'Team not authorized', 'OAUTH_027'),
            ({'name': DataGenerator.generate_random_word(), "parent": DataGenerator.generate_random_int()}, 401,
             'Team not authorized', 'OAUTH_027'),
            ({'name': DataGenerator.generate_random_word(), "links_to": DataGenerator.generate_random_int()}, 401,
             'Team not authorized', 'OAUTH_027')
        ]
    )
    def test_negative_update_task(self, tasks_scenarios, task_data, invalid_data, expected_status_code,
                                  expected_err_message, expected_err_code):
        init_task_model = task_data()
        new_task_model = task_data()
        invalid_data_model = new_task_model.model_copy(update=invalid_data, deep=True)
        error_model = BasicErrorModel(err=expected_err_message, ECODE=expected_err_code)
        tasks_scenarios.negative_update_task(init_task_model, invalid_data_model, expected_status_code, error_model)

    @allure.description(
        'Create new task with generated data and delete it by ID, validate status code and that response body is empty')
    def test_delete_task_by_id(self, authed_session, task_data):
        task_id = self.test_successful_create_new_task(authed_session, task_data)['id']
        delete_task_response = authed_session.tasks_api.delete_task(task_id)
        assert not delete_task_response.text, f'Unexpected body in response: {delete_task_response.text}'

    @allure.description(
        'Generate random task ID and try to delete it without permission, validate that received error message and code equal to expected')
    def test_negative_delete_task_by_id(self, authed_session, task_data):
        task_id = DataGenerator.generate_random_int()
        delete_task_response = authed_session.tasks_api.delete_task(task_id, 401)
        delete_task_response_json = delete_task_response.json()
        assert delete_task_response_json['err'] in ('Team not authorized',
                                                    'Team(s) not authorized'), f'Unexpected error message: {delete_task_response_json['err']}'
        assert delete_task_response_json['ECODE'] in ('OAUTH_023',
                                                      'OAUTH_027'), f'Unexpected error code: {delete_task_response_json['ECODE']}'
