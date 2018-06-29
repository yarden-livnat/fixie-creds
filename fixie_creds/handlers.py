"""Tornado handlers for interfacing with fixie credentials."""
from base64 import b64decode
from fixie.request_handler import RequestHandler
import fixie_creds

from fixie_creds.cache import CACHE


class Register(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'email': {'type': 'string', 'empty': False},
              }

    def post(self):
        token, flag = CACHE.register(**self.request.arguments)
        if flag:
            response = {'token': token, 'status': True}
        else:
            response = {'token': '<not-a-token>', 'status': False, 'message': token}
        self.write(response)


class Verify(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'token': {'type': 'string', 'regex': '[0-9a-fA-F]+'},
              }
    response_keys = ('verified', 'message', 'status')

    def post(self):
        resp = CACHE.verify(**self.request.arguments)
        response = dict(zip(self.response_keys, resp))
        self.write(response)


class Deregister(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'token': {'type': 'string', 'regex': '[0-9a-fA-F]+'},
              }
    response_keys = ('message', 'status')

    def post(self):
        resp = CACHE.deregister(**self.request.arguments)
        response = dict(zip(self.response_keys, resp))
        self.write(response)


class Reset(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'email': {'type': 'string', 'empty': False},
              }

    def post(self):
        token, flag = CACHE.reset(**self.request.arguments)
        if flag:
            response = {'token': token, 'status': True}
        else:
            response = {'token': '<not-a-token>', 'status': False, 'message': token}
        self.write(response)


import re
class Login(RequestHandler):
    """Authorize user.
    Must be a separate call because setting the secure cookie takes effect only on the next call"""
    schema = {}

    def post(self):
        valid, msg, status = -1, 'Unknown Authentication', False
        if 'Authorization' in self.request.headers:
            m = re.search('Basic (.+)', self.request.headers['Authorization'])
            if m:
                user, token = b64decode(m.group(1)).decode('UTF-8').split(':')
                valid, msg, status = CACHE.verify(user, token)
                if valid:
                    self.set_secure_cookie('user', user)
        self.write({'status': valid, 'msg': msg})


class Echo(RequestHandler):
    schema = {'msg': {'type': 'string', 'empty': False}}

    @fixie_creds.authenticated
    def post(self):
        msg = self.request.arguments['msg']
        self.write({'echo': msg})


HANDLERS = [
    ('/verify', Verify),
    ('/register', Register),
    ('/deregister', Deregister),
    ('/reset', Reset),
    ('/login', Login),
    ('/echo', Echo)
]