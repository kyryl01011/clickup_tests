from src.api.api_manager import ApiManager
from src.data_models.tasks import CreatedTaskModel
from src.utils.response_validator import validate_response


class TasksScenarios:
    def __init__(self, api_manager: ApiManager):
        self.api_manager = api_manager

    def create_task(self, task_data_model) -> CreatedTaskModel:
        create_task_response = self.api_manager.tasks_api.create_new_task(task_data_model)
        create_task_response_model = validate_response(create_task_response, CreatedTaskModel)
        return create_task_response_model
