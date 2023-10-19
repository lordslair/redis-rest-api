# -*- coding: utf8 -*-

import json
import requests
import os
import time

from datetime import datetime
from loguru import logger

GUNICORN_PORT = os.environ.get("GUNICORN_PORT", 5000)
API_URL = f'http://127.0.0.1:{GUNICORN_PORT}'
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
ITEM_ID = '00000000-0000-0000-0000-000000000000'
EVENT_BODY = {
    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "id": ITEM_ID,
    "timestamp": time.time_ns() // 1000000,
    "type": None,
    "archived": False,
    "claimed": True,
}
# Return code used when a KEY is nor found in Redis
CODE_ENOTFOUND = int(os.environ.get('CODE_ENOTFOUND', 404))


def test_redis_api_put():
    response = requests.put(
        url=f'{API_URL}/query/tests:{ITEM_ID}',
        headers=HEADERS,
        json={'claimed': False, 'archived': True},
        )

    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200
    assert json.loads(response.text)['success'] is True
    assert json.loads(response.text)['payload']['key'] == f'tests:{ITEM_ID}'
    assert json.loads(response.text)['payload']['value']['claimed'] is False
    assert json.loads(response.text)['payload']['value']['archived'] is True
    assert 'type' not in json.loads(response.text)['payload']['value']
    assert 'timestamp' not in json.loads(response.text)['payload']['value']

    # If we query non-existing key, it should return a CODE_ENOTFOUND
    response = requests.put(
        url=f'{API_URL}/query/tests:foobar',
        headers=HEADERS,
        json={'claimed': False, 'archived': True},
        )

    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == CODE_ENOTFOUND
    assert json.loads(response.text)['success'] is False
    assert json.loads(response.text)['payload'] is None
