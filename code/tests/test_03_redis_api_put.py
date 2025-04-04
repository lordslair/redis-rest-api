# -*- coding: utf8 -*-

import requests
import os
import time

from datetime import datetime
from loguru import logger

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


def test_redis_api_put(api_url, headers):
    response = requests.put(url=f'{api_url}/query/tests:{ITEM_ID}', headers=headers, json={'claimed': False, 'archived': True})  # noqa: E501
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is True
    assert response_json['payload']['key'] == f'tests:{ITEM_ID}'
    assert response_json['payload']['value']['claimed'] is False
    assert response_json['payload']['value']['archived'] is True
    assert 'type' not in response_json['payload']['value']
    assert 'timestamp' not in response_json['payload']['value']

    # If we query non-existing key, it should return a CODE_ENOTFOUND
    response = requests.put(url=f'{api_url}/query/tests:foobar', headers=headers, json={'claimed': False, 'archived': True})  # noqa: E501
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == CODE_ENOTFOUND

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is False
    assert response_json['payload'] is None
