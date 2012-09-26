# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = "kuliguo"
__version__ = "0.1"

import webbrowser
import time

from weibo import APIClient, APIError, _encode_params, JsonObject
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
    oauth = OAuth('', '', '', app_key, app_secret, app_callback)
    #    client = APIClient()
    #    oauth_token, oauth_token_secret = parse_oauth_tokens(
    #        client.oauth.request_token())
    print("""
In the web browser window that opens please choose to Allow
access. Copy the PIN number that appears on the next page and paste or
type it here:
""")
    oauth_url = get_authorize_url(oauth)

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

    access_token, expires_in, access_uid = parse_oauth_tokens(
        request_access_token(code=oauth_verifier, oauth=oauth))
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


def get_authorize_url(oauth, redirect_uri=None, display='default'):
    '''
    return the authroize url that should be redirect.
    '''
    redirect = redirect_uri if redirect_uri else oauth.app_callback
    if not redirect:
        raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
    return '%s%s?%s' % (oauth.auth_url, 'authorize',
                        _encode_params(client_id=oauth.app_key,
                            response_type=oauth.response_type,
                            display=display,
                            redirect_uri=redirect))


def request_access_token(code, oauth, redirect_uri=None):
    '''
    return access token as object: {"access_token":"your-access-token","expires_in":12345678,"uid":1234}, expires_in is standard unix-epoch-time
    '''

    client = APIClient(apitype='oauth2', format=None)
    redirect = redirect_uri if redirect_uri else oauth.app_callback
    if not redirect:
        raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
    r = client.access_token(
        client_id=oauth.app_key,
        client_secret=oauth.app_secret,
        redirect_uri=redirect,
        code=code, grant_type='authorization_code',
        _method='POST'
    )

    current = int(time.time())
    expires = r.expires_in + current
    remind_in = r.get('remind_in', None)
    if remind_in:
        rtime = int(remind_in) + current
        if rtime < expires:
            expires = rtime
    jo = JsonObject(access_token=r.access_token, expires_in=expires)
    uid = r.get('uid', None)
    if uid:
        jo.uid = uid
    return jo
