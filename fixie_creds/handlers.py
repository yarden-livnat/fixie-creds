"""Tornado handlers for interfacing with fixie credentials."""

from fixie.request_handler import RequestHandler

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


HANDLERS = [
    ('/register', Register),
]