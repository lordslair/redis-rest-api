# -*- coding: utf8 -*-

from flask import jsonify, request
from loguru import logger

from routes._decorators import exists
from routes.query._tools import str2typed, typed2str
from utils.redis import r
from variables import CODE_ENOTFOUND


# Custom decorators
@exists.token
@exists.json
@exists.key
def patch(key):
    key_type = r.type(key)
    if key_type != 'hash':
        # The request try to update a KEY which is not a HASH
        # We refuse that
        msg = f'[{key}] KEY TYPE should be HASH (TYPE:{key_type})'
        logger.warning(msg)
        return jsonify(
            {
                "success": False,
                "msg": msg,
                "payload": None,
            }
        ), 400

    for field_name, field_value in request.json.items():
        if r.hexists(key, field_name):
            logger.trace(f'[{key}] FIELD <{field_name}> found in HKEY')
        else:
            msg = f'[{key}] FIELD  <{field_name}> not found in HKEY'
            logger.warning(msg)
            return jsonify(
                {
                    "msg": msg,
                    "success": False,
                    "payload": None,
                    }
                ), CODE_ENOTFOUND

    # We assume the JSON is valid, as it is parsed by Flask
    # We need to transform the values from Typed to STR
    # Especially for True/False/None
    hashdict = {}
    for property, value in request.json.items():
        hashdict[property] = typed2str(value)

    # If we are here, all checks have been passed
    # We can HMSET
    try:
        r.hmset(key, hashdict)
        hash = r.hgetall(key)
        value = {}
        for field_name, field_value in hash.items():
            value[field_name] = str2typed(field_value)
    except Exception as e:
        msg = f'[{key}] KEY HMSET KO [{e}]'
        logger.error(msg)
        return jsonify(
            {
                "success": False,
                "msg": msg,
                "payload": None,
            }
        ), 200
    else:
        logger.trace(f'[{key}] KEY HMSET OK')

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
