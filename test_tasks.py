from tasks import healthcheck
from utils import transform_backends_from_config

import yaml

def test_healthcheck():
    config = yaml.safe_load('''
        hosts:
          - host: www.appA.com
            servers:
              - localhost:8081
              - localhost:8888
          - host: www.appB.com
            servers:
              - localhost:9081
              - localhost:4444
    ''')
    register = healthcheck(transform_backends_from_config(config))

    assert register["www.appB.com"][0].healthy == True
    assert register["www.appB.com"][1].healthy == False
    assert register["www.appA.com"][0].healthy == True
    assert register["www.appA.com"][1].healthy == False