from flask import Flask, request
import requests
from utils import load_configuration, transform_backends_from_config, get_healthy_server, process_header_rules
from tasks import healthcheck

loadbalancer = Flask(__name__)
config = load_configuration('loadbalancer.yaml')
register = transform_backends_from_config(config)

@loadbalancer.route("/")
@loadbalancer.route("/<path>")
def router(path="/"):
    updated_register = healthcheck(register)
    host_header = request.headers["Host"]
    for entry in config["hosts"]:
        if host_header == entry["host"]:
            healthy_server = get_healthy_server(entry["host"], updated_register)
            if not healthy_server:
                return "No Backends servers available", 503
            headers = process_header_rules(config, host_header, {k:v for k,v in request.headers.items()}, "header" )
            response = requests.get("http://{}".format(healthy_server.endpoint), headers=headers)
            return response.content, response.status_code
    
    for entry in config["paths"]:
        if ("/" + path) == entry["path"]:
            healthy_server = get_healthy_server(entry["path"], register)
            if not healthy_server:
                return "No Backends servers available", 503
            response = requests.get("http://{}".format(healthy_server.endpoint))
            return response.content, response.status_code
            
    return "Not Found", 404