# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = "kuliguo"
__version__ = "0.1"


def write_token_file(filename, access_token, expires_in, access_uid):
    """
    Write a token file to hold the oauth token and oauth token secret.
    """
    oauth_file = open(filename, 'w')
    print(access_token, file=oauth_file)
    print(expires_in, file=oauth_file)
    print(access_uid, file=oauth_file)
    oauth_file.close()


def read_token_file(filename):
    """
    Read a token file and return the oauth token and oauth token secret.
    """
    f = open(filename)
    return f.readline().strip(), f.readline().strip(), f.readline().strip()


class OAuth(object):
    """
    An OAuth authenticator.
    """

    def __init__(self, access_token, expires_in, access_uid, app_key, app_secret, app_callback):
        """
        Create the authenticator. If you are in the initial stages of
        the OAuth dance and don't yet have a token or token_secret,
        pass empty strings for these params.
        """
        self.access_token = access_token
        self.expires_in = expires_in
        self.access_uid = access_uid
        self.app_key = app_key
        self.app_secret = app_secret
        self.app_callback = app_callback

    def generate_headers(self):
        return {'Authorization': 'OAuth2 %s' % self.access_token}
