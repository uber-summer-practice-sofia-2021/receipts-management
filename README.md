# receipts-management
The service simulation through Docker:
 - All the docker compose files use an external network called 'receipt-net' which is also the default one.
 - The network is created, so the isolated containers can communicate with each other, in order to simulate the activity of the other services. Otherwise, the communication through local ports would have to be done by using direct ip's and ports, instead of references.
 - Also, if the network is created during the compose phase, if we were to run multiple compose services at once, a network of the same name would be created simulatenously which will result in a total mess.
 - Without the network, communication between the containers wouldn't be possible.
 - The network is automatically created and destroyed with the images and containers through using the 'dockStart.bat' and 'dockStop.bat' (for Windows users).
______________
# NOTE : 
 - If you are on any other system, you'd have to create the network manually by using 'docker network create receipt-net' and then compose each DockerFile separately or adapt the automated '.bat' files to your system.
