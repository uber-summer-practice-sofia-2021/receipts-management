FROM python:3.8-slim

RUN apt-get update && apt-get install -y vim curl

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 8000
ENV FLASK_ENV=development
ENV FLASK_APP=courier-test.py

CMD ["flask", "run", "--port=8000", "--host=0.0.0.0"]