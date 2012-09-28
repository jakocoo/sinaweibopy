# -*- coding: utf-8 -*-

__author__ = "kuliguo"
__version__ = "0.1"

from oauth import *
from oauth_weibo import oauth_weibo
from weibo import APIClient

import time

def login():
    APP_KEY = '1865902151'
    APP_SECRET = '90ac51374b40c681c031b8981334f59d'
    APP_CALLBACK = 'http://127.0.0.1/callback'

    TOKEN_FILE = '../weibo.oauth'

    try:
        (access_token, expires_in, access_uid) = read_token_file(TOKEN_FILE)
        if time.time() - expires_in > 0:
            raise IOError

    except IOError, e:
        (access_token, expires_in, access_uid) = oauth_weibo(APP_KEY, APP_SECRET,
            APP_CALLBACK, TOKEN_FILE)

    return APIClient(
        oauth=OAuth(access_token, expires_in, access_uid,
            APP_KEY, APP_SECRET, APP_CALLBACK))

