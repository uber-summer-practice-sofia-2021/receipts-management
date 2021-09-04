import os
import requests
from controllers.controller import Controller
from flask import Flask, request, render_template, url_for, json, Response

server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")

def saveTrip(tripId):
  try:
    file = open("fixtures/trips/" + tripId + ".json", 'x')
    file.write(tripId)
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
myController = Controller(configPath + "/config/HTTPClients.json")#Missing one argument path to config/HTTPClients.json

#Main function
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  tripID = request.json
  tripID = tripID['tripID']
  server.logger.debug(tripID)
  saveTrip(tripID)
  return "Successfully received"
  

if __name__ == "__main__":
   server.run(host='0.0.0.0')