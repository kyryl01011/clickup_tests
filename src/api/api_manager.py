from requests import Session

from src.api.tasks_client_api import TasksApi


class ApiManager:
    def __init__(self, session: Session):
        self.session = session
        self.tasks_api = TasksApi(session)
