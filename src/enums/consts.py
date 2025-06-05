from src.utils.helpers import CLICKUP_API_KEY

BASE_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': CLICKUP_API_KEY
}

BASE_URL = 'https://api.clickup.com/api/v2'