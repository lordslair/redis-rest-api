# -*- coding: utf8 -*-

from flask import jsonify, request
from loguru import logger

from utils.redis import r
from utils.routehelper import (
    request_check_token,
    request_check_json,
    str2typed,
    typed2str,
    )
from variables import ACCESS_TOKEN, CODE_ENOTFOUND


def put(key):
    request_check_json(request)
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

    # We assume the JSON is valid, as it is parsed by Flask
    # We need to transform the values from Typed to STR
    # Especially for True/False/None
    hashdict = {}
    for property, value in request.json.items():
        hashdict[property] = typed2str(value)

    # If we are here, all checks have been passed
    # We can HMSET
    try:
        r.delete(key)
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

    # We check if TTL is given, to SET EXPIRE on the key
    try:
        expire = request.headers.get('X-Custom-Redis-Expire')
        if expire:
            r.expire(key, expire)
    except Exception as e:
        msg = f'[{key}] KEY EXPIRE KO [{e}]'
        logger.error(msg)
        return jsonify(
            {
                "success": False,
                "msg": msg,
                "payload": None,
            }
        ), 200
    else:
        logger.trace(f'[{key}] KEY EXPIRE OK')

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
