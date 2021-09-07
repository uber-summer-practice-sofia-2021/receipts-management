import os
import requests
from controllers.controller import Controller
from flask import Flask, request, render_template, url_for, json, Response, jsonify

server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")

def saveTrip(tripId):
  try:
    file = open("fixtures/trips/" + tripId + ".json", 'x')
    server.logger.debug(file)
  except:
    server.logger.debug("File already exists")


@server.route("/message-queue")
def hello():
  return "Hello World!"

@server.route("/test")
def user():
  return render_template("index.html")


# controller
configPath = os.path.dirname(__file__)
#myController = Controller(configPath + "/config/HTTPClients.json")#Missing one argument path to config/HTTPClients.json
myController = Controller(os.path.join(server.root_path, 'config', 'HTTPClients.json'))

#Main function
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  tripID = request.json
  server.logger.debug(tripID)
  #tripID = tripID['tripID']
  #saveTrip(tripID)

  response = myController.PostRequestToCourierService(tripID)

  server.logger.debug(response.text)

  #requests.post("http://couriers:8000/get_trip_info", json = tripID)
  return "Successfully received"
  
@server.route("/get_trip_info", methods = ['POST'])
def receiveWholeTrip():
  wholeTrip = request.json
  server.logger.debug(wholeTrip)
  return "Successfully Received"


if __name__ == "__main__":
  server.run(host='0.0.0.0')