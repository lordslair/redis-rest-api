# -*- coding: utf8 -*-

import functools

from flask import jsonify, request
from loguru import logger

from utils.redis import r
from variables import env_vars


def json(func):
    """ Decorator to check if received body is well formated JSON. """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            msg = '[API] Missing JSON in request'
            logger.warning(msg)
            return jsonify(
                {
                    "success": False,
                    "msg": msg,
                    "payload": None,
                }
            ), 400
        else:
            return func(*args, **kwargs)

    return wrapper


def key(func):
    """ Decorator to check if a KEY exists in Redis or not. """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = kwargs.get('key')
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
                ), env_vars['CODE_ENOTFOUND']

    return wrapper


def token(func):
    """ Decorator to check if the token received is valid or not. """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if request.headers.get('Authorization') != f"Bearer {env_vars['ACCESS_TOKEN']}":
                msg = '[API] Token not authorized'
                logger.warning(msg)
                return jsonify(
                    {
                        "success": False,
                        "msg": msg,
                        "payload": None,
                    }
                ), 401
        except Exception as e:
            logger.error(f'[API] Token validation KO [{e}]')
            return jsonify(
                {
                    "success": False,
                    "msg": msg,
                    "payload": None,
                }
            ), 500
        else:
            logger.trace('[API] Token validation OK')

    return wrapper
