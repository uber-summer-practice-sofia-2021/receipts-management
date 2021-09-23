FROM python:3.8-slim

RUN apt-get update && apt-get install -y vim curl

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 2181
EXPOSE 5000 
EXPOSE 9092 




CMD ["python", "consumer.py", "worker", "-l", "info", "--without-web"]

# CMD ["tail", "-f", "/dev/null"] 

# CMD ["./start.sh"]
