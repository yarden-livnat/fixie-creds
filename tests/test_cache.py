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


def test_verify(credsdir):
    user = 'saiid'
    email = 'rukhsana@geno52.cl'

    # make sure verification fails when we haven't registered
    valid, msg, flag = CACHE.verify(user, '0' * CACHE.nbytes)
    assert not valid
    assert not flag
    assert msg == "User '" + user + "' not registered"

    # test a registered user with correct token
    token, flag = CACHE.register(user, email)
    assert flag
    valid, msg, flag = CACHE.verify(user, token)
    assert valid
    assert flag
    assert msg == 'User verified'

    # test a registered user with incorrect token
    valid, msg, flag = CACHE.verify(user, '424242')
    assert not valid
    assert flag
    assert msg == 'Invalid token for user ' + user

