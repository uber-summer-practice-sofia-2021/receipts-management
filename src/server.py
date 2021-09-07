import os
import requests
from controllers.controller import Controller
from flask import Flask, config, request, render_template, url_for, json, Response, jsonify
#Import the g object, sqlite3 and all functions for the database
from db_class import *

server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")
server.config.from_json('config.json')

# controller
configPath = server.config['CONFIG_PATH']
myController = Controller(configPath + "/HTTPClients.json")#Missing one argument path to config/HTTPClients.json

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


<<<<<<< HEAD
# controller
configPath = os.path.dirname(__file__)
#myController = Controller(configPath + "/config/HTTPClients.json")#Missing one argument path to config/HTTPClients.json
myController = Controller(os.path.join(server.root_path, 'config', 'HTTPClients.json'))
=======
@server.route("/testdb", methods = ["GET"])
def testdb():
  server.logger.debug(server.config['CONFIG_PATH'])
  server.logger.debug(configPath)
  server.logger.debug(myController.get_courier_info)
  return "cool"


def getAllInfo(tripID):
  courierResponse = requests.post("http://couriers:8000/get_trip_info", json = tripID)
  courierResponse = courierResponse.json()
  orderResponse = requests.post("http://orders:9000/get_order_info", json = courierResponse['orderId'])
  orderResponse = orderResponse.json()
  server.logger.debug(orderResponse)
  server.logger.debug(courierResponse)

>>>>>>> 22d6e5cd48adc89b4a6ee20074958bd98c1fc1a6

#Main function
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  tripID = request.json
<<<<<<< HEAD
  server.logger.debug(tripID)
  #tripID = tripID['tripID']
  #saveTrip(tripID)

  response = myController.PostRequestToCourierService(tripID)

  server.logger.debug(response.text)

  #requests.post("http://couriers:8000/get_trip_info", json = tripID)
=======
  tripID = tripID['tripID']
  server.logger.debug(tripID)
  getAllInfo(tripID)
>>>>>>> 22d6e5cd48adc89b4a6ee20074958bd98c1fc1a6
  return "Successfully received"


if __name__ == "__main__":
  server.run(host='0.0.0.0')