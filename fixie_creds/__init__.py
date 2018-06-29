import functools
import tornado.web
import re
from base64 import b64decode

from fixie_creds import environ
from fixie_creds.cache import CACHE
from fixie_creds.auth import authenticated

del environ

__version__ = '0.0.2'


# def authenticated(method):
#     """Decorate methods with this to require that the user be logged in.
#
#     Ensure use is logged in. Otherwise, sends Unauthorized reply.
#     """
#     @functools.wraps(method)
#     def wrapper(self, *args, **kwargs):
#         if self.get_current_user():
#             return method(self, *args, **kwargs)
#         self.set_status(401)
#         self.finish('Unauthorized')
#         raise tornado.web.Finish
#
#     return wrapper