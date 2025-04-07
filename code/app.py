#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import time

from flask import Flask, jsonify, g

from prometheus_flask_exporter import PrometheusMetrics

from werkzeug.middleware.proxy_fix import ProxyFix

from variables import env_vars
from utils.gunilog import (
    InterceptHandler,
    LOG_LEVEL,
    logger,
    logging,
    StandaloneApplication,
    StubbedGunicornLogger,
    )

# Imports of endpoint functions
import routes.keys
import routes.query
import routes.scan

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # We wrap around all the app the metrics

# Setup the ProxyFix to have the Real-IP in the logs
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


@app.before_request
def before_request_time():
    g.start = time.time()


@app.after_request
def after_request_time(response):
    response.headers["X-Custom-Elapsed"] = time.time() - g.start
    return response


#
# Routes /check (k8s livenessProbe)
#
@app.route('/check', methods=['GET'])
def check():
    return jsonify(
        {
            "msg": 'UP and running',
            "success": True,
            "payload": None,
            }
        ), 200


#
# Routes /query
#
app.add_url_rule(
    '/query/<path:key>',
    methods=['GET'],
    view_func=routes.query.get
    )
app.add_url_rule(
    '/query/<path:key>',
    methods=['DELETE'],
    view_func=routes.query.delete
    )
app.add_url_rule(
    '/query/<path:key>',
    methods=['PATCH'],
    view_func=routes.query.patch
    )
app.add_url_rule(
    '/query/<path:key>',
    methods=['POST'],
    view_func=routes.query.post
    )
app.add_url_rule(
    '/query/<path:key>',
    methods=['PUT'],
    view_func=routes.query.put
    )
#
# Routes /keys
#
app.add_url_rule(
    '/keys/<path:path>',
    methods=['GET'],
    view_func=routes.keys.keys
    )
#
# Routes /raw
#
app.add_url_rule(
    '/query/raw',
    methods=['POST'],
    view_func=routes.query.raw
    )
#
# Routes /scan
#
app.add_url_rule(
    '/scan/<path:path>',
    methods=['GET'],
    view_func=routes.scan.scan
    )


if __name__ == '__main__':
    intercept_handler = InterceptHandler()
    logging.root.setLevel(LOG_LEVEL)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout}])

    options = {
        "bind": env_vars['GUNICORN_BIND'],
        "workers": env_vars['GUNICORN_WORKERS'],
        "threads": env_vars['GUNICORN_THREADS'],
        "accesslog": "-",
        "errorlog": "-",
        "logger_class": StubbedGunicornLogger,
        "reload": env_vars['GUNICORN_RELOAD'],
        "chdir": env_vars['GUNICORN_CHDIR']
    }

    StandaloneApplication(app, options).run()
