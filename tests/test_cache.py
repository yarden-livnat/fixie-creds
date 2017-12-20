"""Tests for cache."""
import json

from fixie_creds.cache import CACHE


def test_register(credsdir):
    user = 'grammaticus'
    email = 'john@notaspy.com'

    assert not CACHE.user_exists(user)

    token, flag = CACHE.register(user, email)
    assert flag
    assert token == '46685257bdd640fb06671ad11c80317fa3b1799d'
    assert CACHE.user_exists(user)

    fname = CACHE.user_cred_file(user)
    with open(fname, 'r') as f:
        u_from_file = json.load(f)
    u_from_cache = CACHE.get_user(user)._asdict()
    assert u_from_file == u_from_cache

    # make sure that a reregister fails
    msg, flag = CACHE.register(user, email)
    assert not flag
    assert msg == "User '" + user + "' already registered"
