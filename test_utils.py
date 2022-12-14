from utils import get_healthy_server, transform_backends_from_config, process_rules, process_rewrite_rules, least_connections, process_firewall_rules_flag, round_robin
from models import Server
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
    
def test_process_header_rules():
    input = yaml.safe_load('''
        hosts:
          - host: www.appA.com
            header_rules:
              add: 
                MyCustomHeader: Test
              remove: 
                Host: www.appA.com
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
    headers = {"Host": "www.appA.com"}
    results = process_rules(input, "www.appA.com", headers, "header")
    assert results == {"MyCustomHeader": "Test"}
    

def test_process_param_rules():
    input = yaml.safe_load('''
        hosts:
          - host: www.appA.com
            param_rules:
              add:
                MyCustomParam: Test
              remove:
                RemoveMe: Remove
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
    params = {"RemoveMe": "Remove"}
    results = process_rules(input, "www.appA.com", params, "param")
    assert results == {"MyCustomParam": "Test"}

def test_process_rewrite_rules():
    input = yaml.safe_load('''
        hosts:
          - host: www.appA.com
            rewrite_rules:
              replace:
                v1: v2
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
    path = "localhost:8081/v1"
    results = process_rewrite_rules(input, "www.appA.com", path)
    assert results == "localhost:8081/v2"

def test_least_connections_empty_list():
    result = least_connections([])
    assert result == None  

def test_least_connections():
    backend1 = Server("localhost:8081")
    backend1.open_connections = 10
    backend2 = Server("localhost:8082")
    backend2.open_connections = 5
    backend3 = Server("localhost:8083")
    backend3.open_connections = 2
    servers = [backend1, backend2, backend3]
    result = least_connections(servers)
    assert result == backend3

def test_process_firewall_rules_reject():
    input = yaml.safe_load('''
        hosts:
          - host: www.appA.com
            firewall_rules:
              ip_reject:
                - 10.192.0.1
                - 10.192.0.2
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
    results = process_firewall_rules_flag(input, "www.appA.com", "10.192.0.1")
    assert results == False  
    

def test_process_firewall_rules_accept():
    input = yaml.safe_load('''
        hosts:
          - host: www.appA.com
            firewall_rules:
              ip_reject:
                - 10.192.0.1
                - 10.192.0.2
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
    results = process_firewall_rules_flag(input, "www.appA.com", "55.55.55.55")
    assert results == True

def test_least_connections():
    backend1 = Server("localhost:8081")
    backend2 = Server("localhost:8082")
    backend3 = Server("localhost:8083")
    servers = [backend1, backend2, backend3]
    result1 = round_robin(servers)
    assert result1 == backend1
    result2 = round_robin(servers)
    assert result2 == backend2
    result3 = round_robin(servers)
    assert result3 == backend3
    result1 = round_robin(servers)
    assert result1 == backend1
    result2 = round_robin(servers)
    assert result2 == backend2
    result3 = round_robin(servers)
    assert result3 == backend3