from typing import Type, TypeVar

import pytest
from pydantic import BaseModel
from requests import Response


ModelType = TypeVar('ModelType', bound=BaseModel)


def validate_response(response: Response, model: Type[ModelType], expected_status_code: int = 200) -> ModelType:
    """
    Validates received response object: check if response status code is expected, parse JSON, serialise it to pydantic model
    :param response: requests Response object
    :param model: expected pydantic model
    :expected_status_code: default = 200
    :return: expected pydantic model
    """
    if response.status_code != expected_status_code:
        pytest.fail(f'Unexpected status code: {response.status_code}, expected: {expected_status_code}')

    try:
        response_payload_dict = response.json()
    except Exception as e:
        pytest.fail(f'Failed to parse response to dict: {e}')

    try:
        response_model = model(**response_payload_dict)
    except Exception as e:
        pytest.fail(
            f'Failed to serialise received json to pydantic model: '
            f'\nReceived JSON: {response_payload_dict}'
            f'\nExpected schema: {model.model_json_schema()}'
            f'\nError: {e}')

    return response_model
