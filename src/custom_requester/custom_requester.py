import allure
from pydantic import BaseModel
from requests import Session

from src.enums.consts import BASE_URL
from src.enums.url_components import UrlComponents


class CustomRequester:
    _BASE_URL = UrlComponents.CURRENT_API_DOMAIN.value + UrlComponents.API_V2.value

    def __init__(self, session: Session):
        self.session = session

    def _get_url(self, endpoint):
        with allure.step(f'Create url with base url and endpoint: {endpoint}\nResult URL: {self._BASE_URL + endpoint}'):
            return self._BASE_URL + endpoint

    def send_request(self, method, endpoint, json=None, data=None):
        with allure.step(f'Send {method} request to {self._get_url(endpoint)} with json={json} and data={data}'):
            if isinstance(json, BaseModel):
                json = json.model_dump()
            url = self._get_url(endpoint)
            response = self.session.request(method, url, json=json, data=data)
            return response
