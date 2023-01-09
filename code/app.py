#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import time

from flask                         import Flask, jsonify, g

from prometheus_flask_exporter     import PrometheusMetrics

from werkzeug.middleware.proxy_fix import ProxyFix

from variables import (
    ACCESS_TOKEN,
    GUNICORN_BIND,
    GUNICORN_CHDIR,
    GUNICORN_RELOAD,
    GUNICORN_THREADS,
    GUNICORN_WORKERS,
    )
from utils.gunilog import (
    InterceptHandler,
    LOG_LEVEL,
    logger,
    logging,
    StandaloneApplication,
    StubbedGunicornLogger,
    )


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

if __name__ == '__main__':
    intercept_handler = InterceptHandler()
    logging.root.setLevel(LOG_LEVEL)

    if ACCESS_TOKEN is None:
        logger.warning('ENV var ACCESS_TOKEN not set. API not protected')
    else:
        logger.success('ENV var ACCESS_TOKEN set. API protected')

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
        "bind": GUNICORN_BIND,
        "workers": GUNICORN_WORKERS,
        "threads": GUNICORN_THREADS,
        "accesslog": "-",
        "errorlog": "-",
        "logger_class": StubbedGunicornLogger,
        "reload": GUNICORN_RELOAD,
        "chdir": GUNICORN_CHDIR
    }

    StandaloneApplication(app, options).run()
