
import base64
import functools

from fixie_creds.cache import CACHE


# def authenticated(method):
#     """Decorate methods with this to require that the user be logged in.
#
#     Ensure use is logged in. Otherwise, sends Unauthorized reply.
#     """
#     @functools.wraps(method)
#     def wrapper(self, *args, **kwargs):
#         if not self.current_user:
#             self.set_status(401)
#             self.finish('Unauthorized')
#             raise tornado.web.Finish
#         return method(self, *args, **kwargs)
#     return wrapper


def authenticated(auth):
    def decore(f):
        def _request_auth(handler):
            handler.set_header('WWW-Authenticate', 'Basic realm=JSL')
            handler.set_status(401)
            handler.finish()
            return False

        def _verify(user, token):
            valid, msg, status = CACHE.verify(user, token)
            return valid

        def _temp_auth(handler, kwargs):
            user = kwargs.get('user')
            token = kwargs.get('token')
            if user and token:
                return _verify(user, token)
            elif user or token:
                _request_auth(handler)
            return False

        def _authenticated(handler):
            return handler.get_current_user()

        def _basic_auth(handler, kwargs):
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None:
                return _request_auth(handler)
            if not auth_header.to_lower().startswith('basic '):
                return _request_auth(handler)

            auth_decoded = base64.b64decode(auth_header[6:]).decode('ascii')
            username, token = str(auth_decoded).split(':', 1)
            if _verify(username, token):
                kwargs['user'] = username

        @functools.wraps(f)
        def wrapper(handler, *args, **kwargs):
            if _temp_auth(kwargs) or _authenticated(handler) or _basic_auth(handler, kwargs):
                f(*args)
            else:
                _request_auth(handler)

        return wrapper

    return decore
