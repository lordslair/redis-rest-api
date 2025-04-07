# -*- coding: utf8 -*-

import os

from loguru import logger


# Grab the environment variables
env_vars = {
    "ACCESS_TOKEN": os.environ.get("ACCESS_TOKEN", None),
    "CODE_ENOTFOUND": int(os.environ.get('CODE_ENOTFOUND', 404)),
    "GUNICORN_CHDIR": os.environ.get("GUNICORN_CHDIR", '/code'),
    "GUNICORN_BIND": f'{os.environ.get("GUNICORN_HOST", "0.0.0.0")}:{os.environ.get("GUNICORN_PORT", 5000)}',  # noqa: E501
    "GUNICORN_WORKERS": int(os.environ.get("GUNICORN_WORKERS", 1)),
    "GUNICORN_THREADS": int(os.environ.get("GUNICORN_THREADS", 2)),
    "GUNICORN_RELOAD": os.environ.get("GUNICORN_RELOAD", True),
}
# Print the environment variables for debugging
for var, value in env_vars.items():
    if var == "ACCESS_TOKEN":
        if value is None:
            logger.warning('Config: ACCESS_TOKEN not set. API not protected')
        else:
            logger.success('Config: ACCESS_TOKEN set. API protected')
            value = value[:5] + '*' * (len(value) - 5)
    logger.debug(f"{var}: {value}")
