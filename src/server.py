import os
import requests
from controllers.controller import Controller
from flask import Flask, request, render_template, url_for, json, Response

server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")

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
  server.logger.debug(tripID)
  return tripID
  

if __name__ == "__main__":
   server.run(host='0.0.0.0')