# -*- coding: utf8 -*-

import requests

from loguru import logger


def test_redis_api_keys(api_url, headers):
    response = requests.get(url=f'{api_url}/keys/tests:*', headers=headers)
    logger.debug(f'{response.status_code}, {response.text}')

    assert response.status_code == 200

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is True
    assert isinstance(response_json['payload'], list)
    assert len(response_json['payload']) == 1
