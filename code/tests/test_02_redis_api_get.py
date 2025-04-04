# -*- coding: utf8 -*-

import requests
import os

from loguru import logger

ITEM_ID = '00000000-0000-0000-0000-000000000000'
# Return code used when a KEY is nor found in Redis
CODE_ENOTFOUND = int(os.environ.get('CODE_ENOTFOUND', 404))


def test_redis_api_get(api_url, headers):
    response = requests.get(url=f'{api_url}/query/tests:{ITEM_ID}', headers=headers)
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is True

    assert response_json['payload']['key'] == f'tests:{ITEM_ID}'
    assert response_json['payload']['value']['id'] == ITEM_ID
    assert response_json['payload']['value']['claimed'] is True
    assert response_json['payload']['value']['archived'] is False
    assert response_json['payload']['value']['type'] is None
    assert response_json['payload']['value']['timestamp'] > 0

    payload_extra = response_json['payload']['value']['extra']
    assert payload_extra['field_one'] == 'value'
    assert payload_extra['field_two']['field_nested_one'] == 'value_nested'

    # If we query non-existing key, it should return a CODE_ENOTFOUND
    response = requests.get(url=f'{api_url}/query/tests:foobar', headers=headers)
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == CODE_ENOTFOUND

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is False
    assert response_json['payload'] is None
