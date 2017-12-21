"""Tests handlers object."""
import pytest
import tornado.web
from tornado.escape import json_decode, json_encode
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
    obs = json_decode(response.body)
    assert exp == obs


@pytest.mark.gen_test
def test_verify_valid(credsdir, http_client, base_url):
    # register user
    body = '{"user": "inigo", "email": "montoya@gmail.com"}'
    url = base_url + '/register'
    response = yield http_client.fetch(url, method="POST", body=body)
    token = json_decode(response.body)['token']

    # verify user
    body = json_encode({"user": "inigo", "token": token})
    url = base_url + '/verify'
    response = yield http_client.fetch(url, method="POST", body=body)
    exp = {'verified': True, "message": 'User verified', "status": True}
    obs = json_decode(response.body)
    assert exp == obs


@pytest.mark.gen_test
def test_deregister_valid(credsdir, http_client, base_url):
    # register user
    body = '{"user": "inigo", "email": "montoya@gmail.com"}'
    url = base_url + '/register'
    response = yield http_client.fetch(url, method="POST", body=body)
    token = json_decode(response.body)['token']

    # deregister user
    body = json_encode({"user": "inigo", "token": token})
    url = base_url + '/deregister'
    response = yield http_client.fetch(url, method="POST", body=body)
    exp = {"message": 'inigo deregistered', "status": True}
    obs = json_decode(response.body)
    assert exp == obs


@pytest.mark.gen_test
def test_reset_valid(credsdir, http_client, base_url):
    # register user
    body = '{"user": "inigo", "email": "montoya@gmail.com"}'
    url = base_url + '/register'
    response = yield http_client.fetch(url, method="POST", body=body)
    token = json_decode(response.body)['token']

    # reset user token
    url = base_url + '/reset'
    response = yield http_client.fetch(url, method="POST", body=body)
    obs = json_decode(response.body)
    assert obs['status']
    assert token != obs['token']


@pytest.mark.parametrize('name', [x[0] for x in HANDLERS])
@pytest.mark.gen_test
def test_register_invalid(credsdir, http_client, base_url, name):
    body = '{"name": 42}'
    url = base_url + name
    try:
        response = yield http_client.fetch(url, method="POST", body=body)
    except HTTPError as e:
        response = e.response
    assert response.code == 400
    assert b'not valid' in response.body
