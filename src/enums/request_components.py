from enum import Enum

from src.utils.helpers import CLICKUP_API_KEY


class RequestComponents(Enum):
    BASE_HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': CLICKUP_API_KEY
    }
