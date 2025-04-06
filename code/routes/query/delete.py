# -*- coding: utf8 -*-

from flask import jsonify
from loguru import logger

from routes._decorators import exists
from utils.redis import r


# Custom decorators
@exists.token
@exists.key
def delete(key):
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
