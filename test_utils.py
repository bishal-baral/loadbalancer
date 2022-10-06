from utils import get_healthy_server, transform_backends_from_config
from models import Server
import pytest
import yaml

def test_transform_backends_from_config():
    input = yaml.safe_load('''
        hosts:
          - host: www.appA.com
            servers:
              - localhost:8081
              - localhost:8082
          - host: www.appB.com
            servers:
              - localhost:9081
              - localhost:9082
        paths:
          - path: /appA
            servers:
              - localhost:8081
              - localhost:8082
          - path: /appB
            servers:
              - localhost:9081
              - localhost:9082
    ''')
    output = transform_backends_from_config(input)
    assert list(output.keys()) == ["www.appA.com", "www.appB.com", "/appA", "/appB"]
    assert output["www.appA.com"][0] == Server("localhost:8081")
    assert output["www.appA.com"][1] == Server("localhost:8082")
    assert output["www.appB.com"][0] == Server("localhost:9081")
    assert output["www.appB.com"][1] == Server("localhost:9082")
    assert output["/appA"][0] == Server("localhost:8081")
    assert output["/appA"][1] == Server("localhost:8082")
    assert output["/appB"][0] == Server("localhost:9081")
    assert output["/appB"][1] == Server("localhost:9082")

def test_get_healthy_server():
    host = "www.appB.com"
    healthy_server = Server("localhost:8081")
    unhealthy_server = Server("localhost:8082")
    unhealthy_server.healthy = False
    register = {"www.appA.com": [healthy_server, unhealthy_server], 
                "www.appB.com": [healthy_server, healthy_server],
                "www.random.com": [unhealthy_server, unhealthy_server],
                "/appA": [healthy_server, unhealthy_server],
                "/appB": [unhealthy_server, unhealthy_server]}
    assert get_healthy_server("www.appA.com", register) == healthy_server
    assert get_healthy_server("www.appB.com", register) == healthy_server
    assert get_healthy_server("www.random.com", register) == None
    assert get_healthy_server("/appA", register) == healthy_server
    assert get_healthy_server("/appB", register) == None