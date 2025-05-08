from requests import Session

from api.tasks_api import TasksApi


class ApiManager:
    def __init__(self, session: Session):
        self.session = session
        self.tasks_api = TasksApi(session)