## Microservices for scalability
- an attempt to test scalability of a microservices architecture style in a containerized environment. 

The goal of this project is to build a microservices architecture from scratch and try different scaling techniques on the server level and simulate delivering services in a production environment. 

## Progress 
1. Familiarizing with Docker
2. Implementing a Load Balancer using Flask
  - adapted from https://medium.com/load-balancer-series
  - instructions for testing the loadbalancer
      ```
        pip install virtualenv
        virtualenv lb
        source lb/bin/activate
        pip install pytest responses flask pyyaml
        docker build -t server .
        make test
      ```
3. **Load Testing with different loadbalancing algorithms**