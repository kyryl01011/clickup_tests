import allure
from requests import Session

from enums.consts import BASE_URL


class CustomRequester:
    def __init__(self, session: Session):
        self.session = session
        self._base_url = BASE_URL
        self.endpoint = ''

    def _get_url(self, endpoint):
        with allure.step(f'Create url with base url and endpoint: {endpoint}\nResult URL: {self._base_url + endpoint}'):
            return self._base_url + endpoint

    def send_request(self, method, url, json=None, data=None, expected_status_code=200):
        with allure.step(f'Send {method} request to {url} with json={json} and data={data}, expected status code {expected_status_code}'):
            response = self.session.request(method, url, json=json, data=data)
            assert response.status_code == expected_status_code, f'Expected status code {expected_status_code}, got {response.status_code}'
            return response