# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = "kuliguo"
__version__ = "0.1"

import webbrowser
import time

from weibo import APIClient
from oauth import OAuth, write_token_file

try:
    _input = raw_input
except NameError:
    _input = input


def oauth_weibo(app_key, app_secret, app_callback, token_filename=None):
    """
    Perform the OAuth dance with some command-line prompts. Return the
    oauth_token and oauth_token_secret.

    Provide the name of your app in `app_name`, your consumer_key, and
    consumer_secret. This function will open a web browser to let the
    user allow your app to access their Twitter account. PIN
    authentication is used.

    If a token_filename is given, the oauth tokens will be written to
    the file.
    """
    print("Hi there! We're gonna get you all set up to use %s." % app_key)
    client = APIClient(oauth=OAuth('', '', '', app_key, app_secret, app_callback))
    #    oauth_token, oauth_token_secret = parse_oauth_tokens(
    #        client.oauth.request_token())
    print("""
In the web browser window that opens please choose to Allow
access. Copy the PIN number that appears on the next page and paste or
type it here:
""")
    oauth_url = client.get_authorize_url()

    print("Opening: %s\n" % oauth_url)

    try:
        r = webbrowser.open(oauth_url)
        time.sleep(2) # Sometimes the last command can print some
        # crap. Wait a bit so it doesn't mess up the next
        # prompt.
        if not r:
            raise Exception()
    except:
        print("""
Uh, I couldn't open a browser on your computer. Please go here to get
your PIN:

""" + oauth_url)
    oauth_verifier = _input("Please enter the PIN: ").strip()
    client = APIClient(oauth=OAuth('', '', '', app_key, app_secret, app_callback))
    access_token, expires_in, access_uid = parse_oauth_tokens(
        client.request_access_token(code=oauth_verifier))
    if token_filename:
        write_token_file(
            token_filename, access_token, expires_in, access_uid)
        print()
        print("That's it! Your authorization keys have been written to %s." % (
            token_filename))
    return access_token, expires_in, access_uid


def parse_oauth_tokens(result):
    access_token = result.access_token
    expires_in = result.expires_in
    access_uid = result.uid

    return access_token, expires_in, access_uid
