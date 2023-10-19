# -*- coding: utf8 -*-

from flask import jsonify


def raw():
    return jsonify(
        {
            "msg": 'RAW (Not Implemented)',
            "success": True,
            "payload": None,
            }
        ), 200
