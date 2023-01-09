# -*- coding: utf8 -*-

from .delete import delete
from .get import get
from .post import post
from .put import put_one, put_multi
from .raw import raw

__all__ = [
    'delete',
    'get',
    'post',
    'put_one',
    'put_multi',
    'raw',
    ]
