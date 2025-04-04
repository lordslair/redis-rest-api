# -*- coding: utf8 -*-

import requests
import os

from loguru import logger

ITEM_ID = '00000000-0000-0000-0000-000000000000'
CODE_ENOTFOUND = int(os.environ.get('CODE_ENOTFOUND', 404))


def test_redis_api_get(api_url, headers):
    response = requests.delete(url=f'{api_url}/query/tests:{ITEM_ID}', headers=headers)
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is True

    # If we try to delete a non-existing key, it should return a CODE_ENOTFOUND
    response = requests.delete(url=f'{api_url}/query/tests:{ITEM_ID}', headers=headers)
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == CODE_ENOTFOUND

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is False
    assert response_json['payload'] is None
