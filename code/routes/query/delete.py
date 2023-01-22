# -*- coding: utf8 -*-

from flask import jsonify, request
from loguru import logger

from utils.redis import r
from utils.routehelper import (
    request_check_token,
    )
from variables import ACCESS_TOKEN, CODE_ENOTFOUND


def delete(key):
    if ACCESS_TOKEN:
        request_check_token(request, f'Bearer {ACCESS_TOKEN}')

    if r.exists(key):
        logger.trace(f'[{key}] KEY found')
    else:
        msg = f'[{key}] KEY not found'
        logger.warning(msg)
        return jsonify(
            {
                "msg": msg,
                "success": False,
                "payload": None,
                }
            ), CODE_ENOTFOUND

    try:
        r.delete(key)
    except Exception as e:
        logger.error(f'[{key}] KEY DELETE KO [{e}]')
    else:
        logger.trace(f'[{key}] KEY DELETE OK')
        msg = f'[{key}] Query OK'
        logger.debug(msg)
        return jsonify(
            {
                "msg": msg,
                "success": True,
                "payload": None,
                }
            ), 200
