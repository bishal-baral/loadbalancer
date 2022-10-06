from loadbalancer import loadbalancer
import pytest
import re

@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client

def test_host_routing_appA(client):
    result = client.get('/', headers={"Host":"www.appA.com"})
    assert re.match("This is the appA application. Serving on localhost:\d+.", result.data.decode('utf-8')) != None

def test_host_routing_appB(client):
    result = client.get('/', headers={"Host":"www.appB.com"})
    assert b'This is the appB application. Serving on localhost:9082.' == result.data

def test_host_routing_notfound(client):
    result = client.get('/', headers={"Host":"www.random.com"})
    assert b'Not Found' in result.data
    assert 404 == result.status_code

def test_server_bad_servers(client):
    result = client.get('/', headers={"Host":"www.appB.com"})
    assert b'This is the appB application. Serving on localhost:9082.' == result.data

def test_server_no_servers(client):
    result = client.get('/', headers={"Host":"www.appC.com"})
    assert 503 == result.status_code

def test_path_routing_appA(client):
    result = client.get('/appA')
    assert re.match("This is the appA application. Serving on localhost:\d+.", result.data.decode('utf-8')) != None

def test_path_routing_appB(client):
    result = client.get('/appB')
    assert b'This is the appB application. Serving on localhost:9082.' == result.data

def test_path_routing_notfound(client):
    result = client.get('/random')
    assert b'Not Found' in result.data
    assert 404 == result.status_code