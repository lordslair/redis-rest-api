# -*- coding: utf8 -*-

import os

# Token used restrictes access
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)

# Gunicorn variables
GUNICORN_CHDIR = os.environ.get("GUNICORN_CHDIR", '/code')
GUNICORN_HOST = os.environ.get("GUNICORN_HOST", "0.0.0.0")
GUNICORN_PORT = os.environ.get("GUNICORN_PORT", 5000)
GUNICORN_BIND = f'{GUNICORN_HOST}:{GUNICORN_PORT}'
GUNICORN_WORKERS = os.environ.get("GUNICORN_WORKERS", 1)
GUNICORN_THREADS = os.environ.get("GUNICORN_THREADS", 2)
GUNICORN_RELOAD = os.environ.get("GUNICORN_RELOAD", True)
