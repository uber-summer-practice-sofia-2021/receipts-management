# receipts-management
The service simulation through Docker:
 - All the docker compose files use an external network called 'receipt-net' which is also the default one.
 - The networks is created, so the isolated containers can communicate with each other, in order to simulate the activity of the other services. Otherwise, the communication through local ports would have to be done by using direct ip's and ports, instead of references.
 - The network is automatically created and destroyed with the images and containers through using the 'dockStart.bat' and 'dockStop.bat' (for Windows users).
______________
# NOTE : 
 - If you are on any other system, you'd have to create the network manually by using 'docker network create receipt-net' and then compose each DockerFile separately or adapt the automated '.bat' files to your system.
