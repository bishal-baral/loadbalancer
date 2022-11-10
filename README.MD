## Microservices for scalability
An attempt to test the scalability of microservices architecture in a containerized environment. 

The goal of this project is to build a microservices architecture from scratch and try different scaling techniques on the server level and simulate delivering services in a production environment. 

## Progress 
1. Familiarizing with Docker
2. Implementing a Load Balancer using Flask
  - adapted from https://medium.com/load-balancer-series
  - instructions for testing the loadbalancer
      ```
        pip install virtualenv pytest responses flask pyyaml
        virtualenv lb
        source lb/bin/activate
        docker build -t server .
        make test
      ```
3. **Load Testing with different loadbalancing algorithms**
