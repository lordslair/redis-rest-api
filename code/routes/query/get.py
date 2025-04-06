# -*- coding: utf8 -*-

from flask import jsonify
from loguru import logger

from routes._decorators import exists
from routes.query._tools import str2typed
from utils.redis import r


# Custom decorators
@exists.token
@exists.key
def get(key):
    key_type = r.type(key)
    if key_type == 'hash':
        # We hill need to use HGET and send back a dict()
        try:
            hash = r.hgetall(key)
            value = {}
            for field_name, field_value in hash.items():
                value[field_name] = str2typed(field_value)
        except Exception as e:
            logger.error(f'[{key}] KEY HGET KO [{e}]')
        else:
            logger.trace(f'[{key}] KEY HGET OK')
    elif key_type == 'string':
        # We hill need to use GET and send back a str()
        try:
            value = str2typed(r.get(key))
        except Exception as e:
            logger.error(f'[{key}] KEY GET KO [{e}]')
        else:
            logger.trace(f'[{key}] KEY GET OK')
    else:
        msg = f'[{key}] KEY TYPE not handled (TYPE:{key_type})'
        logger.warning(msg)
        return jsonify(
            {
                "msg": msg,
                "success": False,
                "payload": None
                }
            ), 400

    # We grab the TTL to return it in headers later
    try:
        ttl = r.ttl(key)
    except Exception as e:
        msg = f'[{key}] KEY TTL KO [{e}]'
        logger.error(msg)
        return jsonify(
            {
                "success": False,
                "msg": msg,
                "payload": None,
            }
        ), 200
    else:
        logger.trace(f'[{key}] KEY TTL OK')

    msg = f'[{key}] Query OK'
    logger.debug(msg)
    return jsonify(
        {
            "msg": msg,
            "success": True,
            "payload": {
                "value": value,
                "key": key,
                }
            }
        ), 200, {"X-Custom-Redis-TTL": ttl}
