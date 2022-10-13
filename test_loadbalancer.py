from loadbalancer import loadbalancer

import pytest
import re

@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client

def test_host_routing_appA(client):
    result = client.get('/', headers={"Host":"www.appA.com"}, query_string={"RemoveMe": "Remove"})
    assert re.match("This is the appA application. Serving on localhost:\d+. Custom Header: Test, Host Header: localhost:\d+, Custom Param: Test", result.data.decode('utf-8')) != None

def test_host_routing_appB(client):
    result = client.get('/', headers={"Host":"www.appB.com"})
    assert b'This is the appB application. Serving on localhost:9082. Custom Header: None, Host Header: www.appB.com, Custom Param: None' == result.data

def test_host_routing_notfound(client):
    result = client.get('/', headers={"Host":"www.random.com"})
    assert b'Not Found' in result.data
    assert 404 == result.status_code

def test_server_bad_servers(client):
    result = client.get('/', headers={"Host":"www.appB.com"})
    assert b'This is the appB application. Serving on localhost:9082. Custom Header: None, Host Header: www.appB.com, Custom Param: None' == result.data

def test_server_no_servers(client):
    result = client.get('/', headers={"Host":"www.appC.com"})
    assert 503 == result.status_code

def test_path_routing_appA(client):
    result = client.get('/appA')
    assert re.match("This is the appA application. Serving on localhost:\d+. Custom Header: None, Host Header: localhost:\d+, Custom Param: None", result.data.decode('utf-8')) != None

def test_path_routing_appB(client):
    result = client.get('/appB')
    assert b'This is the appB application. Serving on localhost:9082. Custom Header: None, Host Header: localhost:9082, Custom Param: None' == result.data

def test_path_routing_notfound(client):
    result = client.get('/random')
    assert b'Not Found' in result.data
    assert 404 == result.status_code