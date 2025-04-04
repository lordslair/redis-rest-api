# -*- coding: utf8 -*-

import requests
import time

from datetime import datetime
from loguru import logger

ITEM_ID = '00000000-0000-0000-0000-000000000000'
EVENT_BODY = {
    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "id": ITEM_ID,
    "timestamp": time.time_ns() // 1000000,
    "extra": {
        "field_one": 'value',
        "field_two": {
            "field_nested_one": 'value_nested',
            "field_nested_two": None,
            "field_nested_three": False,
        }
    },
    "type": None,
    "archived": False,
    "claimed": True,
}


def test_redis_api_post(api_url, headers):
    response = requests.post(url=f'{api_url}/query/tests:{ITEM_ID}', headers=headers, json=EVENT_BODY)  # noqa: E501
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 201

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is True

    # If we POST again, it should fail as the key already exists
    response = requests.post(url=f'{api_url}/query/tests:{ITEM_ID}', headers=headers, json=EVENT_BODY)  # noqa: E501
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is False
