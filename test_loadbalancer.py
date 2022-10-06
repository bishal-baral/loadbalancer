from loadbalancer import loadbalancer

import pytest

@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client

def test_host_routing_appA(client):
    result = client.get('/', headers={"Host":"www.appA.com"})
    assert b'This is the appA application.' in result.data

def test_host_routing_appB(client):
    result = client.get('/', headers={"Host":"www.appB.com"})
    assert b'This is the appB application.' in result.data

def test_host_routing_notfound(client):
    result = client.get('/', headers={"Host":"www.random.com"})
    assert b'Not Found' in result.data
    assert 404 == result.status_code

def test_path_routing_appA(client):
    result = client.get('/appA')
    assert b'This is the appA application.' in result.data

def test_path_routing_appB(client):
    result = client.get('/appB')
    assert b'This is the appB application.' in result.data

def test_path_routing_notfound(client):
    result = client.get('/random')
    assert b'Not Found' in result.data
    assert 404 == result.status_code