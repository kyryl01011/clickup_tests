from src.api.api_manager import ApiManager
from src.data_models.errors import BasicErrorModel
from src.data_models.tasks import CreatedTaskModel, CreationTaskModel
from src.utils.response_validator import validate_response


class TasksScenarios:
    def __init__(self, api_manager: ApiManager):
        self.api_manager = api_manager

    def create_task(self, task_data_model) -> CreatedTaskModel:
        create_task_response = self.api_manager.tasks_api.create_new_task(task_data_model)
        create_task_response_model = validate_response(
            create_task_response,
            CreatedTaskModel,
            expected_data=task_data_model)
        created_model = self.get_task_by_id(create_task_response_model.id)
        assert created_model.name == task_data_model.name, \
            (f'Initial name not equals to created one: '
             f'Initial: {task_data_model.name}'
             f'Created: {created_model.name}')
        return create_task_response_model

    def create_task_negative(self, task_data_model, expected_status_code, error_model):
        response = self.api_manager.tasks_api.create_new_task(task_data_model)
        validate_response(response, BasicErrorModel, expected_status_code, error_model)

    def get_task_by_id(self, task_id: str) -> CreatedTaskModel:
        get_task_response = self.api_manager.tasks_api.get_task(task_id)
        get_task_response_model = validate_response(get_task_response, CreatedTaskModel)
        assert task_id == get_task_response_model.id, \
            (f'Request task ID not equals to response task ID: '
             f'Request: {task_id}'
             f'Response: {get_task_response_model.id}')
        return get_task_response_model

    def get_task_by_id_negative(
            self,
            task_id: str,
            expected_status_code: int,
            err_model
    ):
        response = self.api_manager.tasks_api.get_task(task_id)
        validate_response(response, BasicErrorModel, expected_status_code, err_model)

    def delete_task_by_id(self, task_id: str):
        delete_task_response = self.api_manager.tasks_api.delete_task(task_id)
        validate_response(delete_task_response, expected_status_code=204)
        check_existence_response = self.api_manager.tasks_api.get_task(task_id)
        validate_response(check_existence_response, BasicErrorModel, 404)

    def delete_task_by_invalid_id(self, fake_id: str):
        response = self.api_manager.tasks_api.delete_task(fake_id)
        expected_err_model = BasicErrorModel(err=('Team not authorized', 'Team(s) not authorized'), ECODE='OAUTH_027')
        validate_response(response, BasicErrorModel, 401, expected_err_model)

    def create_and_delete_task(self, task_data_model):
        created_task_model = self.create_task(task_data_model)
        self.delete_task_by_id(created_task_model.id)

    def update_task(self, task_id: str, new_task_model: CreationTaskModel):
        response = self.api_manager.tasks_api.update_task(task_id, new_task_model)
        validate_response(response, CreatedTaskModel, expected_data=new_task_model)

    def update_task_negative(
            self,
            task_id: str,
            new_task_model: CreationTaskModel | None = None,
            expected_status_code: int = 400,
            expected_error_model: BasicErrorModel | None = None
    ):
        response = self.api_manager.tasks_api.update_task(task_id, new_task_model)
        if expected_error_model is not None:
            validate_response(response, BasicErrorModel, expected_status_code, expected_error_model)
        else:
            validate_response(response, expected_status_code=expected_status_code)

    def create_and_update_task_negative(self, init_task_model: CreationTaskModel,
                                        new_task_model, expected_status_code, expected_error_model):
        created_task_model = self.create_task(init_task_model)
        self.update_task_negative(created_task_model.id, new_task_model, expected_status_code, expected_error_model)

    def create_and_update_task(self, init_task_model: CreationTaskModel, new_task_model: CreationTaskModel):
        init_task = self.create_task(init_task_model)
        self.update_task(init_task.id, new_task_model)
