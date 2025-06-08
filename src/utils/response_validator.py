from typing import Type, TypeVar

import pytest
from pydantic import BaseModel
from requests import Response


ModelType = TypeVar('ModelType', bound=BaseModel)


def validate_response(response: Response, model: Type[ModelType] | None = None, expected_status_code: int = 200,
                      expected_data: ModelType | None = None) -> ModelType | None:
    """
    Validates received response object:
    check if response status code is expected, parse JSON, serialise it to pydantic model
    :param response: requests Response object
    :param model: expected pydantic model
    :param expected_status_code: default = 200
    :param expected_data: data from request to compare
    :return: expected pydantic model
    """
    if response.status_code != expected_status_code:
        pytest.fail(f'Unexpected status code: {response.status_code}, expected: {expected_status_code}')

    if model is not None:
        try:
            response_payload_dict = response.json()
        except Exception as e:
            pytest.fail(f'Failed to parse response to dict: {response.text}'
                        f'\n{e}')

        try:
            response_model = model(**response_payload_dict)
        except Exception as e:
            pytest.fail(
                f'Failed to serialise received json to pydantic model: '
                f'\nReceived JSON: {response_payload_dict}'
                f'\nExpected schema: {model.model_json_schema()}'
                f'\nError: {e}')

        if expected_data:
            response_dict = response_model.model_dump()
            for key, value in expected_data.model_dump().items():
                if key in response_dict:
                    assert response_dict[key] == value or response_dict[key] in value, \
                        (f'Unexpected value for initial data "{key}": {response_dict[key]}\n'
                         f'Expected: {value}')

        return response_model
    return None
