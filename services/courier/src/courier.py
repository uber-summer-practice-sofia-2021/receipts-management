import os
import json
from flask import Flask, request, Response,  jsonify
from flask.json import JSONDecoder
import requests

server = Flask(__name__)

@server.route("/")
def hello():
  return "Hello World!"

#Simulates courier API interacting with us
@server.route("/send", methods=["POST"])
def sendTripInfo():
  file = {"tripID":"trip"}
  server.logger.debug(file)
  requests.post("http://receipts:5000/receive_trip_id", json = file)
  return "Successfully Sent"

@server.route("/get_trip_info", methods = ["POST"])
def sendAllInfo():
  tripID = request.json
<<<<<<< HEAD
  server.logger.debug(tripID)

  trip_info = json.load(open(os.path.join(server.root_path, "fixtures", "courier.json")))

  server.logger.debug(trip_info)

  #file = json.load(open("fixtures/" + tripID+ ".json"))

  server.logger.debug(trip_info)

  #requests.post("http://receipts:5000/get_trip_info", json = file)

  return trip_info
=======
  file = json.load(open("fixtures/" + tripID+ ".json"))
  return file
>>>>>>> 22d6e5cd48adc89b4a6ee20074958bd98c1fc1a6

if __name__ == "__main__":
   server.run(host='0.0.0.0')