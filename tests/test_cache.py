"""Tests for cache."""

from fixie_creds.cache import CACHE


def test_register(credsdir):
    token, flag = CACHE.register('grammaticus', 'john@notaspy.com')
    assert flag
    assert token == '46685257bdd640fb06671ad11c80317fa3b1799d'
