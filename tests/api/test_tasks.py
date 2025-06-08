import allure
import pytest

from src.data_models.errors import BasicErrorModel
from tests.conftest import task_data
from src.utils.data_generator import DataGenerator


@allure.title('Manage tasks API')
@allure.feature('Manage tasks')
class TestTasks:

    @allure.description('Generates new task and check if task with such data exists using ID')
    def test_get_task(self, tasks_scenarios, task_data):
        generated_task_data = task_data()
        created_task_model = tasks_scenarios.create_task(generated_task_data)
        tasks_scenarios.get_task_by_id(created_task_model.id)

    @allure.description('Generates random ID and check if error message and code equals to expected')
    @pytest.mark.parametrize(
        'expected_status_code, expected_err_message, expected_err_code',
        [
            (401, ('Team not authorized', 'Team(s) not authorized'), ('OAUTH_023', 'OAUTH_027'))
        ]
    )
    def test_negative_get_task(self, tasks_scenarios, task_data, expected_status_code,
                               expected_err_message, expected_err_code):
        random_id = DataGenerator.generate_random_int()
        err_model = BasicErrorModel(err=expected_err_message, ECODE=expected_err_code)
        tasks_scenarios.get_task_by_id_negative(random_id, expected_status_code, err_model)

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
                                      expected_err_message, expected_err_code):
        valid_data_model = task_data()
        invalid_data_model = valid_data_model.model_copy(update=invalid_data, deep=True)
        err_model = BasicErrorModel(err=expected_err_message, ECODE=expected_err_code)
        tasks_scenarios.create_task_negative(
            invalid_data_model,
            expected_status_code,
            err_model
        )

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
            ({"parent": DataGenerator.generate_random_int()}, 504, None, None)
        ]
    )
    def test_negative_update_task(self, tasks_scenarios, task_data, invalid_data, expected_status_code,
                                  expected_err_message, expected_err_code):
        init_task_model = task_data()
        new_task_model = task_data()
        invalid_data_model = new_task_model.model_copy(update=invalid_data, deep=True)
        error_model = None
        if expected_err_message is not None and expected_status_code is not None:
            error_model = BasicErrorModel(err=expected_err_message, ECODE=expected_err_code)
        tasks_scenarios.create_and_update_task_negative(
            init_task_model,
            invalid_data_model,
            expected_status_code,
            error_model)

    @allure.description(
        'Create new task with generated data and delete it by ID, validate status code and that response body is empty')
    def test_delete_task_by_id(self, tasks_scenarios, task_data):
        test_model = task_data()
        tasks_scenarios.create_and_delete_task(test_model)

    @allure.description(
        'Generate random task ID and try to delete it without permission, '
        'validate that received error message and code equal to expected')
    def test_negative_delete_task_by_id(self, tasks_scenarios):
        fake_id = DataGenerator.generate_random_word()
        tasks_scenarios.delete_task_by_invalid_id(fake_id)
