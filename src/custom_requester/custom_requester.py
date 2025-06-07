import allure
from pydantic import BaseModel
from requests import Session

from src.enums.consts import BASE_URL


class CustomRequester:
    def __init__(self, session: Session):
        self.session = session
        self._base_url = BASE_URL
        self.endpoint = ''

    def _get_url(self, endpoint):
        with allure.step(f'Create url with base url and endpoint: {endpoint}\nResult URL: {self._base_url + endpoint}'):
            return self._base_url + endpoint

    def send_request(self, method, endpoint, json=None, data=None):
        with allure.step(f'Send {method} request to {self._get_url(endpoint)} with json={json} and data={data}'):
            if isinstance(json, BaseModel):
                json = json.model_dump()
            url = self._get_url(endpoint)
            response = self.session.request(method, url, json=json, data=data)

            print(f'''\n\nREQUEST
{response.request.url}
{response.request.method}
RESPONSE
{response.status_code}
{response.text}''')

            return response
