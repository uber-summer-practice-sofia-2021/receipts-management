## How to run?
### unix based 

Run as usual ---------------> ```docker-compose.yml up -d```.

Don't forget to clean up ---> ```docker-compose.yml down```.

Curl command for requesting our 'main' tripID receiving endpoint.
```
curl -H "Content-type: application/json" -d '{"tripId":"trip"}' 'http://localhost:5000/receive_trip_id'

curl -H "Content-type: application/json" -d '{"tripID":"5f6fd161-6b4d-462b-be85-89a26ec699a7"}' 'http://recei-publi-mgbjqgr3kcf-121656833.eu-west-1.elb.amazonaws.com/receive_trip_id'
curl -H "Content-type: application/json" -d '{"tripID":"97df8470-1a84-49fa-9164-92dcf4135b99"}' 'http://recei-publi-mgbjqgr3kcf-121656833.eu-west-1.elb.amazonaws.com/receive_trip_id'

```
### windows
The service simulation through Docker:
 - All the docker compose files use an external network called 'receipt-net' which is also the default one.
 - The network is created, so the isolated containers can communicate with each other, in order to simulate the activity of the other services. Otherwise, the communication through local ports would have to be done by using direct ip's and ports, instead of references.
 - Also, if the network is created during the compose phase, if we were to run multiple compose services at once, a network of the same name would be created simulatenously which will result in a total mess.
 - Without the network, communication between the containers wouldn't be possible.
 - The network is automatically created and destroyed with the images and containers through using the 'dockStart.bat' and 'dockStop.bat' (for Windows users).
______________
#### NOTE : 
 - If you are on any other system, you'd have to create the network manually by using 'docker network create receipt-net' and then compose each DockerFile separately or adapt the automated '.bat' files to your system.

### Example HTTP requests:
    - http://receipts:5000/...
    - http://couriers:8000/...
    - http://orders:9000/...
