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


def test_deregister(credsdir):
    user = 'soneka'
    email = 'peto@nurth.net'
    token, flag = CACHE.register(user, email)

    # test that we can't deregister someone who doesn't exist
    msg, flag = CACHE.deregister('grammaticus', '0' * CACHE.nbytes)
    assert not flag

    # test that we can't deregister with an incorrect token
    msg, flag = CACHE.deregister(user, '424242')
    assert not flag

    # test a successful deregister
    msg, flag = CACHE.deregister(user, token)
    assert flag
    assert msg == user + ' deregistered'
    assert not CACHE.user_exists(user)


def test_reset(credsdir):
    user = 'bronzi'
    email = 'hurtado@670th.org'
    token, flag = CACHE.register(user, email)

    # test that we can't reset someone who doesn't exist
    msg, flag = CACHE.reset('saiid', 'rukhsana@geno52.cl')
    assert not flag
    assert msg == 'User {0!r} not registered'.format('saiid')

    # test that we can't reset with wrong email address
    msg, flag = CACHE.reset(user, 'hurtado@alpha.legion')
    assert not flag
    assert msg == 'User email does not match registered email address'

    # test that we can actually reset
    new_token, flag = CACHE.reset(user, email)
    assert flag
    assert new_token != token
    new_hashed_token = CACHE.hash_token(new_token)
    u = CACHE.get_user(user)
    assert new_hashed_token == u.hashed_token
    fname = CACHE.user_cred_file(user)
    with open(fname, 'r') as f:
        u_from_file = json.load(f)
    u_from_cache = u._asdict()
    assert u_from_file == u_from_cache
