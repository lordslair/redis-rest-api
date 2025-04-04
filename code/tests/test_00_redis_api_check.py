# -*- coding: utf8 -*-

import requests

from loguru import logger


def test_redis_api_check(api_url):
    response = requests.get(url=f'{api_url}/check')
    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200

    response_json = response.json()  # Use the built-in .json() method
    assert response_json['success'] is True
