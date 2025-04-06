# -*- coding: utf8 -*-

from flask import jsonify

from routes._decorators import exists


# Custom decorators
@exists.token
def raw():
    return jsonify(
        {
            "msg": 'RAW (Not Implemented)',
            "success": True,
            "payload": None,
            }
        ), 200
