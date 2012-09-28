#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.2'
__author__ = 'kuliguo (kuliguo@gmail.com)'

'''
Python client SDK for sina weibo API using OAuth 2.
'''

POST_ACTIONS = [

    # Status Methods
    'update', 'retweet',

    # Direct Message Methods
    'new',

    # Account Methods
    'update_profile_image', 'update_delivery_device', 'update_profile',
    'update_profile_background_image', 'update_profile_colors',
    'update_location', 'end_session',

    # Notification Methods
    'leave', 'follow',

    # Status Methods, Block Methods, Direct Message Methods,
    # Friendship Methods, Favorite Methods
    'destroy',

    # Block Methods, Friendship Methods, Favorite Methods
    'create',
]

try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib
import urllib2
import re

def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o


class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''

    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)


class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

    def __getstate__(self):
        return self.copy()

    def __setstate__(self, state):
        self.update(state)


def _encode_params(**kw):
    '''
    Encode parameters.
    '''
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    if not args:
        return None
    else:
        return '&'.join(args)


def _encode_multipart(**kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            ext = ''
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            if n != (-1):
                ext = filename[n:].lower()
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = {'.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                  '.jpe': 'image/jpeg'}

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')

_HTTP_GET = "GET"
_HTTP_POST = "POST"
_HTTP_UPLOAD = "_POST"

class HttpCall(object):
    def __init__(self, api_url, format, oauth, callablecls, uriparts=None):
        self.api_url = api_url
        self.format = format
        self.oauth = oauth
        self.callable_cls = callablecls
        self.uriparts = uriparts

    def is_expires(self):
        if not self.oauth:
            return False
        else:
            return not self.oauth.access_token or time.time() > self.oauth.expires_in

    def __getattr__(self, attr):
        try:
            return object.__getattr__(self, attr)
        except AttributeError:
            def extend_call(arg):
                if self.is_expires():
                    raise APIError('21327', 'expired_token', arg)
                return self.callable_cls(api_url=self.api_url, format=self.format, oauth=self.oauth,
                    callablecls=self.callable_cls, uriparts=self.uriparts + (arg,))

            return extend_call(attr)

    def __call__(self, **kwargs):
        '''
        send an http request and expect to return a json object if no error.
        '''
        params = None
        boundary = None

        # Build the uri.
        uriparts = []
        for uripart in self.uriparts:
            # If this part matches a keyword argument, use the
            # supplied value otherwise, just use the part.
            uriparts.append(str(kwargs.pop(uripart, uripart)))
        uri = '/'.join(uriparts)
        if self.format:
            the_url = '%s%s.%s' % (self.api_url, uri, self.format)
        else:
            the_url = '%s%s' % (self.api_url, uri)

        method = kwargs.pop('_method', None)
        if not method:
            method = "GET"
            for action in POST_ACTIONS:
                if re.search("%s(/\d+)?$" % action, uri):
                    method = "POST"
                    break

        if method == _HTTP_UPLOAD:
            params, boundary = _encode_multipart(**kwargs)
        else:
            params = _encode_params(**kwargs)

        if params and method == _HTTP_GET:
            http_url = '%s?%s' % (the_url, params)
        else:
            http_url = the_url

        http_body = None if method == _HTTP_GET else params
        req = urllib2.Request(http_url, data=http_body)
        if self.oauth and self.oauth.access_token:
            req.add_header('Authorization', 'OAuth2 %s' % self.oauth.access_token)
        if boundary:
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        resp = urllib2.urlopen(req)
        body = resp.read()
        r = json.loads(body, object_hook=_obj_hook)
        if hasattr(r, 'error_code'):
            raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        return r


class APIClient(HttpCall):
    '''
    API client using synchronized invocation.
    '''

    def __init__(self, oauth=None, domain='api.weibo.com', apitype='2', format='json'):
        self.oauth = oauth
        self.api_url = 'https://%s/%s/' % (domain, apitype)
        self.format = format
        uriparts = ()
        HttpCall.__init__(self, api_url=self.api_url, format=self.format, oauth=self.oauth, callablecls=HttpCall,
            uriparts=uriparts)
