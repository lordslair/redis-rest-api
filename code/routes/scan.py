# -*- coding: utf8 -*-

from flask import jsonify, request
from loguru import logger

from utils.redis import r
from utils.routehelper import request_check_token
from variables import ACCESS_TOKEN, CODE_ENOTFOUND


def scan(path):
    if ACCESS_TOKEN:
        request_check_token(request, f'Bearer {ACCESS_TOKEN}')

    try:
        keys = list(r.scan_iter(path))
    except Exception as e:
        msg = f'[{path}] SCAN Query [{e}]'
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
            ), CODE_ENOTFOUND
    else:
        return jsonify(
            {
                "msg": msg,
                "success": True,
                "payload": keys
                }
            ), 200
