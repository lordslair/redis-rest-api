# -*- coding: utf8 -*-

import re

from flask                      import jsonify
from loguru                     import logger


def request_check_token(request, bearer):
    try:
        if request.headers.get('Authorization') != bearer:
            msg = '[API] Token not authorized'
            logger.warning(msg)
            return jsonify(
                {
                    "success": False,
                    "msg": msg,
                    "payload": None,
                }
            ), 403
    except Exception as e:
        logger.error(f'[API] Token validation KO [{e}]')
        return jsonify(
            {
                "success": False,
                "msg": msg,
                "payload": None,
            }
        ), 200
    else:
        logger.trace('[API] Token validation OK')


def request_check_json(request):
    try:
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
    except Exception as e:
        logger.error(f'[API] JSON validation KO [{e}]')
        return jsonify(
            {
                "success": False,
                "msg": msg,
                "payload": None,
            }
        ), 200
    else:
        logger.trace('[API] JSON validation OK')


def str2typed(string):
    # BOOLEAN False
    if string == 'False':
        return False
    # BOOLEAN True
    elif string == 'True':
        return True
    # None
    elif string == 'None':
        return None
    # Date
    elif re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', string):
        return string
    # INT
    elif string.isdigit():
        return int(string)
    else:
        return string


def typed2str(string):
    # None
    if string is None:
        return 'None'
    # BOOLEAN True
    elif string is True:
        return 'True'
    # BOOLEAN False
    elif string is False:
        return 'False'
    else:
        return string
