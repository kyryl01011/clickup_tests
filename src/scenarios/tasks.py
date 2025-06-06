from src.api.api_manager import ApiManager
from src.data_models.errors import AuthErrorModel
from src.data_models.tasks import CreatedTaskModel
from src.utils.response_validator import validate_response


class TasksScenarios:
    def __init__(self, api_manager: ApiManager):
        self.api_manager = api_manager

    def create_task(self, task_data_model) -> CreatedTaskModel:
        create_task_response = self.api_manager.tasks_api.create_new_task(task_data_model)
        create_task_response_model = validate_response(create_task_response, CreatedTaskModel)
        created_model = self.get_task_by_id(create_task_response_model.id)
        assert created_model.name == task_data_model.name, \
            (f'Initial name not equals to created one: '
             f'Initial: {task_data_model.name}'
             f'Created: {created_model.name}')
        return create_task_response_model

    def get_task_by_id(self, task_id: str) -> CreatedTaskModel:
        get_task_response = self.api_manager.tasks_api.get_task(task_id)
        get_task_response_model = validate_response(get_task_response, CreatedTaskModel)
        assert task_id == get_task_response_model.id, \
            (f'Request task ID not equals to response task ID: '
             f'Request: {task_id}'
             f'Response: {get_task_response_model.id}')
        return get_task_response_model

    def negative_get_task_by_id(self, task_id: str,
                                expected_error_msg: set,
                                expected_error_code: set,
                                expected_status_code=401):
        response = self.api_manager.tasks_api.get_task(task_id)
        response_model: AuthErrorModel = validate_response(response, AuthErrorModel, expected_status_code)
        assert response_model.err in expected_error_msg, \
            (f'Unexpected error message: {response_model.err}'
             f'Expected: {expected_error_msg}')
        assert response_model.ECODE in expected_error_code, \
            (f'Unexpected error ECODE: {response_model.ECODE}'
             f'Expected: {expected_error_code}')

    def delete_task_by_id(self, task_id: str):
        delete_task_response = self.api_manager.tasks_api.delete_task(task_id)
        assert delete_task_response.status_code == 204, \
            (f'Unexpected status code: {delete_task_response.status_code}'
             f'Expected: 204')
        assert delete_task_response.text == '', f'Unexpected response body: {delete_task_response.text}'
        check_existence_response = self.api_manager.tasks_api.get_task(task_id)
        assert check_existence_response.status_code == 404, \
            (f'Unexpected status code: '
             f'Expected: 404'
             f'Got: {check_existence_response.status_code}')

