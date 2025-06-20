from enum import Enum

from src.utils.helpers import CLICKUP_TEAM_ID, CLICKUP_LIST_ID


class Endpoints(Enum):
    LOGIN = '/login'
    BOARD = f'/{CLICKUP_TEAM_ID}/v/b/t/{CLICKUP_TEAM_ID}'
    TASK = '/task'
    LIST_TASK = f'/list/{CLICKUP_LIST_ID}/task'
