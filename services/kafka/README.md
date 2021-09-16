# kafka

## set-up
0. run kafka in docker container and create single partition topic

1. feed the kafka topic with producer.py to mock data 

2. read from kafka topic with faust stream - consumer.py

3. send async request from faust stream handler to our main server endpoint

## references:
- kafka
  - documentation: 
    - https://kafka.apache.org/
  - paper:
    - https://link.springer.com/referenceworkentry/10.1007/978-3-319-63962-8_196-1
  - wurstmeister's kafka docker set-up:
    - https://github.com/wurstmeister/kafka-docker

- faust
  - https://github.com/robinhood/faust

- flask
  - https://github.com/pallets/flask
   
- aiohttp
  - https://github.com/aio-libs/aiohttp

## a few examples of how people use kafka and aiohttp
- https://abhishekbose550.medium.com/basic-stream-processing-using-kafka-and-faust-7de07ed0ea77

- https://medium.com/geekculture/streaming-model-inference-using-flask-and-kafka-3476d9ff5ca5
  
- https://abhishekbose550.medium.com/basic-stream-processing-using-kafka-and-faust-7de07ed0ea77
  
- https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp 
 
- https://medium.com/@TimvanBaarsen/apache-kafka-cli-commands-cheat-sheet-a6f06eac01b

## some kafka cli
Run from ```$KAFKA_HOME/bin/```. Don't forget to run the kafka container first.

The topic is called ```test```.

- feed kafka
```
./kafka-console-producer.sh --topic test --bootstrap-server localhost:9092
```
    
- read from kafka
```
./kafka-console-consumer.sh --topic test --from-beginning --bootstrap-server localhost:9092
```
