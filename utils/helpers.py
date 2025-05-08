import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable '{name}' is not set")
    return value


CLICKUP_API_KEY = get_env_variable("CLICKUP_API_KEY")
CLICKUP_EMAIL = get_env_variable("CLICKUP_EMAIL")
CLICKUP_PASSWORD= get_env_variable("CLICKUP_PASSWORD")
CLICKUP_TEAM_ID= get_env_variable('CLICKUP_TEAM_ID')
CLICKUP_SPACE_ID=get_env_variable('CLICKUP_SPACE_ID')
CLICKUP_FOLDER_ID=get_env_variable('CLICKUP_FOLDER_ID')
CLICKUP_LIST_ID=get_env_variable('CLICKUP_LIST_ID')