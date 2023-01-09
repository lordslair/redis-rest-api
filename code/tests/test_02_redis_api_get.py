# -*- coding: utf8 -*-

import json
import requests
import os

from loguru import logger

GUNICORN_PORT      = os.environ.get("GUNICORN_PORT", 5000)
API_URL            = f'http://127.0.0.1:{GUNICORN_PORT}'
ACCESS_TOKEN       = os.environ.get('ACCESS_TOKEN', None)
HEADERS            = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
ITEM_ID            = '00000000-0000-0000-0000-000000000000'


def test_redis_api_get():
    url      = f'{API_URL}/query/tests:{ITEM_ID}'
    response = requests.get(
        url,
        headers=HEADERS,
        )

    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200
    assert json.loads(response.text)['success'] is True
    assert json.loads(response.text)['payload']['key'] == f'tests:{ITEM_ID}'
    assert json.loads(response.text)['payload']['value']['id'] == ITEM_ID
    assert json.loads(response.text)['payload']['value']['claimed'] is True
    assert json.loads(response.text)['payload']['value']['archived'] is False
    assert json.loads(response.text)['payload']['value']['type'] is None
    assert json.loads(response.text)['payload']['value']['timestamp'] > 0
