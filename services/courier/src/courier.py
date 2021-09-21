import os
import json
from flask import Flask, request, Response,  jsonify
from flask.json import JSONDecoder
import requests
from werkzeug.exceptions import BadRequest

server = Flask(__name__)

@server.route("/")
def hello():
  return "Hello World!"

#Simulates courier API interacting with us
@server.route("/send", methods=["POST"])
def sendTripInfo():
  file = {"tripId":"b364522a-b588-41dc-8a9d-6984878f1454"} #this is already in db for testing
  response = requests.post("http://receipts:5000/receive_trip_id", json = file)
  server.logger.info(response.status_code)
  return str(response.status_code)

@server.route("/get_trip_info", methods = ["POST"])
def sendAllInfo():
  tripId = request.json
  with open(os.path.join(server.root_path, "fixtures", "{0}.json").format(tripId)) as file:
    trip_info = json.load(file)
  server.logger.info(trip_info)
  return trip_info

if __name__ == "__main__":
   server.run(host='0.0.0.0')
