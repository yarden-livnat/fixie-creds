"""Represents a credentials cache that is backed by the file system. This cache
is the underlying registration and verification engine for credentials.

Importantly, while the credtials may generate a token for a user, that token is
NEVER stored. Instead, the hash of the token is stored.  Verification compares
the hash of token provided by the user to the stored hashed token.
"""
import json
import random
import hashlib

from fixie.environ import expand_and_make_dir


User = namedtuple('User', ['user', 'email', 'hashed_token'])


class Cache:
    """A cache for fixie credentials."""

    __inst = None

    def __new__(cls):
        # make the cache a singleton
        if Cache.__inst is None:
            Cache.__inst = object.__new__(cls)
        return Cache.__inst

    def __init__(self, credsdir=None, seed=None, nbytes=20):
        """
        Parameters
        ----------
        credsdir : str or None, optional
            Path to credentials directory, if None, defaults to $FIXIE_CREDS_DIR.
        seed : int, bytes, or None, optional
            Value to seed to Pythons RNG. This is provided for testing purpose,
            For production, this should be set to None so that reseeding is
            done based on system time and other parameters.
        nbytes : int, optional
            Number of bits to use when generating for tokens.
        """
        random.seed(seed)
        self.nbytes = nbytes
        self.nbits = nbytes * 8
        self._credsdir = None
        self._dirty = True
        self._users = {}  # maps usernames to named tuples of
        self.credsdir = credsdir

    @property
    def credsdir(self):
        value = self._credsdir
        if value is None:
            value = ENV['FIXIE_CREDS_DIR']
        return value

    @credsdir.setter
    def credsdir(self, value):
        self._dirty = True
        self._users.clear()
        if value is None:
            self._credsdir = value
        else:
            self._credsdir = expand_and_make_dir(value)

    def user_cred_file(self, user):
        """Returns the credential filename for a user."""'
        return os.path.join(self.credsdir, user + '.json')

    def user_exists(self, user):
        """Returns whether or not a user exists (ie has been registered)."""
        if user in self._users:
            return True
        return os.path.isfile(self.user_cred_file(user))

    def hash_token(self, token):
        """Hashes a token."""
        i = int(token, 16)
        b = i.to_bytes(self.nbytes, 'little')
        h = hashlib.sha256(b)
        return h.hexdigest()

    def write_user(self, user, email, hashed_token):
        """Writes a user's credential file."""
        data = {'user': user, 'email': email, 'hashed_token': hashed_token}
        fname = self.user_cred_file(user)
        with open(fname, 'w') as f:
            json.dump(data, f, sort_keys=True, separators=(',', ':'))
        self._users[user] = User(**data)

    def register(self, user, email):
        """Registers a new user and provides their token.

        Parameters
        ----------
        user : str
            Name of the user to register.
        email : str
            Email address for the user.

        Returns
        -------
        token or message : str
            The token if the registration was successful, and an error message
            if it wasn't.
        flag : bool
            Whether or not the registration was successful.
        """
        if self.user_exists(user):
            return 'User {0!r} already registered'.format(user), False
        token = hex(random.getrandbits(self.nbits))[2:]
        hashed_token = self.hash_token(token)
        self.write_user(user, email, hashed_token)
        return token, True


CACHE = Cache()
