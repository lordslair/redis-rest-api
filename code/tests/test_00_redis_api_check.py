# -*- coding: utf8 -*-

import json
import requests
import os

from loguru import logger

GUNICORN_PORT      = os.environ.get("GUNICORN_PORT", 5000)
API_URL            = f'http://127.0.0.1:{GUNICORN_PORT}'


def test_redis_api_check():
    url      = f'{API_URL}/check'
    response = requests.get(url)

    logger.debug(f'{response.status_code}, {response.text}')
    assert response.status_code == 200
    assert json.loads(response.text)['success'] is True
