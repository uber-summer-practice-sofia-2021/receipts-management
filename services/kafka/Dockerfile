FROM python:3.8-slim

RUN apt-get update && apt-get install -y vim curl

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 2181
EXPOSE 5000 
EXPOSE 9092 
EXPOSE 6066


ENV TOPIC0000 = trips
ENV TOPIC0002 = trips2
ENV TOPIC_DLQ = trips-dlq

ENV APP_ID    = freya_kafka_consumer
ENV BROKERS   = b-2.uber-delivery.dcv4e6.c6.kafka.eu-west-1.amazonaws.com:9092,b-1.uber-delivery.dcv4e6.c6.kafka.eu-west-1.amazonaws.com:9092

ENV FREYA_URL = http://recei-Publi-MGBJQGR3KCF-121656833.eu-west-1.elb.amazonaws.com



# CMD ["python", "consumer.py", "worker", "-l", "info", "--without-web"]

 CMD ["tail", "-f", "/dev/null"] 

# CMD ["./start.sh"]
