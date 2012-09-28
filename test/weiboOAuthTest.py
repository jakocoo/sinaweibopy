# -*- coding: utf-8 -*-

__author__ = 'kuliguo'
__version__ = '0.2'

import unittest
from oauth import OAuth, read_token_file
import oauth_weibo

class weiboOAuthTest(unittest.TestCase):
    def setUp(self):
        self.APP_KEY = '1865902151'
        self.APP_SECRET = '90ac51374b40c681c031b8981334f59d'
        self.APP_CALLBACK = 'http://127.0.0.1/callback'
        self.TOKEN_FILE = '../weibo.oauth'

    def test_get_authorize_url(self):
        oauth = OAuth('', '', '', self.APP_KEY, self.APP_SECRET, self.APP_CALLBACK)
        url = oauth_weibo.get_authorize_url(oauth)
        self.assertEqual(url,
            'https://api.weibo.com/oauth2/authorize?redirect_uri=http%3A//127.0.0.1/callback&response_type=code&client_id=1865902151&display=default')

    def test_expires(self):
        import time

        (access_token, expires_in, access_uid) = read_token_file(self.TOKEN_FILE)
        self.assertEqual(type(expires_in), float)
        self.assertTrue(expires_in - time.time() > 0)

    def test_read_token_file(self):
        (access_token, expires_in, access_uid) = read_token_file(self.TOKEN_FILE)
        self.assertTrue(access_token)
        self.assertEqual(access_uid, '2133898242')

if __name__ == "__main__":
    unittest.main()
