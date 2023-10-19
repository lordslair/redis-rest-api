# -*- coding: utf8 -*-

import json
import requests
import os

from loguru import logger

GUNICORN_PORT = os.environ.get("GUNICORN_PORT", 5000)
API_URL = f'http://127.0.0.1:{GUNICORN_PORT}'
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
ITEM_ID = '00000000-0000-0000-0000-000000000000'


def test_redis_api_get():
    response = requests.get(
        url=f'{API_URL}/query/tests:{ITEM_ID}',
        headers=HEADERS,
        )

    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200

    response_json = json.loads(response.text)
    assert response_json['success'] is True

    payload_key = response_json['payload']['key']
    payload_value = response_json['payload']['value']
    assert payload_key == f'tests:{ITEM_ID}'
    assert payload_value['id'] == ITEM_ID
    assert payload_value['claimed'] is True
    assert payload_value['archived'] is False
    assert payload_value['type'] is None
    assert payload_value['timestamp'] > 0

    payload_extra = response_json['payload']['value']['extra']
    assert payload_extra['field_one'] == 'value'
    assert payload_extra['field_two']['field_nested_one'] == 'value_nested'

    # If we query non-existing key, it should return a 404
    response = requests.get(
        url=f'{API_URL}/query/tests:foobar',
        headers=HEADERS,
        )

    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 404
    assert json.loads(response.text)['success'] is False
