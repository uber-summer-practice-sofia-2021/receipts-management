import os
import requests
from controllers.controller import Controller
from flask import Flask, config, request, render_template, url_for, json, Response, jsonify
#Import the g object, sqlite3 and all functions for the database
from db_class import *
from pathlib import Path
import sys


server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")
server.config['CONFIG_PATH'] = os.path.join(server.root_path, "config")

myController = Controller(server.config['CONFIG_PATH'] + "/HTTPClients.json")#Missing one argument path to config/HTTPClients.json

#db
#database = DB(open(configPath + "/db_config.json"))

def saveTrip(tripId):
  try:
    with open ("/fixtures/trips/" + tripId + "json", 'x') as file : 
      server.logger.debug(file)
  except:
    server.logger.debug("File already exists")


@server.route("/message-queue")
def hello():
  return "cool?"


@server.route("/test")
def user():
  return render_template("index.html")

@server.route("/testdb", methods = ["GET"])
def testdb():
  #database.make_dicts()
  #server.logger.debug("LOOOOOOOOOOOOOOOOOOOOK")
  #server.logger.debug(server.config['CONFIG_PATH'])
  with open (os.path.join((server.root_path), "config", 'HTTPClients.json')) as file:
    data = json.load(file)
    server.logger.debug(data)
  #open('HTTPClients.json')
  return "cool"

def getAllInfo(tripID):
  courierResponse = requests.post("http://couriers:8000/get_trip_info", json = tripID)
  courierResponse = courierResponse.json()
  orderResponse = requests.post("http://orders:9000/get_order_info", json = courierResponse['orderId'])
  orderResponse = orderResponse.json()
  server.logger.debug(orderResponse)
  server.logger.debug(courierResponse)

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


if __name__ == "__main__":
  server.run(host='0.0.0.0')