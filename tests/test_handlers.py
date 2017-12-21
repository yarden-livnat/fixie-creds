"""Tests handlers object."""
import pytest
import tornado.web
import tornado.escape
from tornado.httpclient import HTTPError

from fixie_creds.handlers import HANDLERS


APP = tornado.web.Application(HANDLERS)


@pytest.fixture
def app():
    return APP


@pytest.mark.gen_test
def test_register_valid(credsdir, http_client, base_url):
    body = '{"user": "inigo", "email": "montoya@gmail.com"}'
    url = base_url + '/register'
    response = yield http_client.fetch(url, method="POST", body=body)
    assert response.code == 200
    exp = {'token': '46685257bdd640fb06671ad11c80317fa3b1799d', 'status': True}
    obs = tornado.escape.json_decode(response.body)
    assert exp == obs


@pytest.mark.gen_test
def test_register_invalid(http_client, base_url):
    body = '{"name": 42}'
    url = base_url + '/register'
    try:
        response = yield http_client.fetch(url, method="POST", body=body)
    except HTTPError as e:
        response = e.response
    assert response.code == 400
    assert b'not valid' in response.body

