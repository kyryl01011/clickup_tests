import allure
import pytest

from tests.conftest import task_data
from src.utils.data_generator import DataGenerator


@allure.title('Manage tasks API')
@allure.feature('Manage tasks')
class TestTasks:

    def test_create_task(self, tasks_scenarios, task_data):
        generated_task_data = task_data()
        tasks_scenarios.create_task(generated_task_data)

    @allure.description('Personal setup, get all existing tasks and delete them one by one using ID')
    def test_delete_all_tasks(self, authed_session):
        all_tasks = self.test_get_all_tasks(authed_session)
        for task in all_tasks:
            authed_session.tasks_api.delete_task(task['id'])
        second_check = self.test_get_all_tasks(authed_session)
        assert len(second_check) == 0, f'Tasks list is not empty: {len(second_check)} elements exists, {second_check}'

    @allure.description('Get all existing tasks')
    def test_get_all_tasks(self, authed_session):
        all_tasks = authed_session.tasks_api.get_all_tasks()
        print(all_tasks.json())
        assert type(all_tasks.json()[
                        'tasks']) is list, f'Unexpected type of response: {type(all_tasks.json()['tasks'])}, expected list'
        return all_tasks.json()['tasks']

    @allure.description('Generates new task and check if task with such data exists using ID')
    def test_get_task(self, authed_session, task_data):
        init_task_data = self.test_successful_create_new_task(authed_session, task_data)
        task = authed_session.tasks_api.get_task(init_task_data['id'])
        task_json = task.json()
        assert init_task_data['id'] == task_json[
            'id'], f'Unexpected task id: {task_json['id']}, expected {init_task_data['id']}'
        assert init_task_data['name'] == task_json[
            'name'], f'Unexpected task name: {task_json['name']}, expected {init_task_data['name']}'

    @allure.description('Generates random ID and check if error message and code equals to expected')
    @pytest.mark.parametrize(
        'expected_err_message, expected_err_code',
        [
            (('Team not authorized', 'Team(s) not authorized'), ('OAUTH_023', 'OAUTH_027'))
        ]
    )
    def test_negative_get_task(self, authed_session, task_data, expected_err_message, expected_err_code):
        task_id = DataGenerator.generate_random_int()
        task = authed_session.tasks_api.get_task(task_id, expected_status_code=401)
        task_json = task.json()
        assert task_json['err'] in expected_err_message, f'Unexpected error message: {task_json['err']}'
        assert task_json['ECODE'] in expected_err_code, f'Unexpected error code: {task_json['ECODE']}'

    @allure.description('Generates random task data and create task with it, verify if data matches')
    def test_successful_create_new_task(self, authed_session, task_data):
        generated_task_data = task_data()
        with allure.step(f'Create new task with data: {generated_task_data}'):
            created_task = authed_session.tasks_api.create_new_task(generated_task_data)
            created_task_json = created_task.json()
        with allure.step(f'Verify created task with ID: {created_task_json['id']} exists'):
            verify_response_json = authed_session.tasks_api.get_task(created_task_json['id']).json()
        assert verify_response_json['name'] == generated_task_data[
            'name'], f'Unexpected task name: {verify_response_json['name']}, expected {generated_task_data['name']}'
        assert created_task_json['name'] == generated_task_data[
            'name'], f'Unexpected task name: {created_task_json['name']}, expected {generated_task_data['name']}'
        return created_task_json

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
    def test_negative_create_new_task(self, authed_session, invalid_data, expected_status_code, expected_err_message,
                                      expected_err_code):
        created_task = authed_session.tasks_api.create_new_task(invalid_data, expected_status_code)
        created_task_json = created_task.json()
        assert created_task_json['err'] == expected_err_message, f'Unexpected error message: {created_task_json['err']}'
        assert created_task_json['ECODE'] == expected_err_code, f'Unexpected error code: {created_task_json['ECODE']}'

    @allure.description(
        'Create new task with generated data, updates it and validate if not equal to initial and equal to newly generated')
    def test_successful_update_task(self, authed_session, task_data):
        initial_task_data = self.test_successful_create_new_task(authed_session, task_data)
        new_task_data = task_data()
        updated_task_json = authed_session.tasks_api.update_task(initial_task_data['id'], new_task_data).json()
        assert new_task_data['name'] == updated_task_json[
            'name'], f'Unexpected updated name: {updated_task_json['name']}, expected {new_task_data['name']}'
        assert initial_task_data['name'] != updated_task_json[
            'name'], f'Initial data did not change: expected {new_task_data['name']}, got {updated_task_json['name']}'

    @allure.description(
        'Generates random task ID and to access it with update request, validate to receive expected error message and code')
    def test_negative_update_task(self, authed_session, task_data):
        task_id = DataGenerator.generate_random_int()
        new_task_data = None
        updated_task = authed_session.tasks_api.update_task(task_id, new_task_data, 401)
        updated_task_json = updated_task.json()
        assert updated_task_json['err'] in ('Team not authorized',
                                            'Team(s) not authorized'), f'Unexpected error message: {updated_task_json['err']}'
        assert updated_task_json['ECODE'] in ('OAUTH_023',
                                              'OAUTH_027'), f'Unexpected error code: {updated_task_json['ECODE']}'

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
