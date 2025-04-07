# -*- coding: utf8 -*-

from flask import jsonify
from loguru import logger

from routes._decorators import exists
from utils.redis import r
from variables import env_vars


# Custom decorators
@exists.token
def keys(path):
    try:
        keys = r.keys(path)
    except Exception as e:
        msg = f'[{path}] KEYS Query [{e}]'
        logger.error(msg)
        return jsonify(
            {
                "success": False,
                "msg": msg,
                "payload": None,
            }
        ), 500

    msg = f'[{path}] Query OK'
    logger.debug(msg)

    if len(keys) == 0:
        msg = f'[{path}] PATH is empty'
        logger.warning(msg)
        return jsonify(
            {
                "msg": msg,
                "success": False,
                "payload": [],
                }
            ), env_vars['CODE_ENOTFOUND']
    else:
        return jsonify(
            {
                "msg": msg,
                "success": True,
                "payload": keys
                }
            ), 200
