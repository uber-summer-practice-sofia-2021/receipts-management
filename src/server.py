from sre_constants import SUCCESS
from flask import Flask, request, render_template
import os
import json
from werkzeug.exceptions import BadRequest


server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")
server.config['CONFIG_PATH'] = os.path.join(server.root_path, "config")

#import controllers
from controllers.Init_Controllers import get_controller
from controllers.Init_Controllers import get_db_controller
from controllers.Receipt import Receipt
from controllers.Validation_Exception import Validation_Exception


def save_trip(tripId):
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
 json_url = os.path.join(server.root_path, "fixtures" ,"receiptsContent.json")
 json_data = json.load(open(json_url))
 return render_template('index.html', data = json_data)



@server.route("/testdb", methods = ["GET"])
def testdb():
  with open (os.path.join(server.config['CONFIG_PATH'], 'HTTPClients.json')) as file:
    data = json.load(file)
    server.logger.debug(data)
  return "cool"



def get_all_info(tripId):
  try:
    get_db_controller().check_existing_id(tripId)
    server.logger.debug("Checked for already existing Receipt Id")
    #Request to Courier
    courierResponse = get_controller().PostRequestToCourierService(tripId)
    courierResponse = courierResponse.json()
    server.logger.debug("Got courier response.")

    #Request to Order
    orderResponse = get_controller().PostReuqestToOrderService(courierResponse['orderId'])
    orderResponse = orderResponse.json()
    server.logger.debug("Got order response.")

    #Creating a Receipt
    currentReceipt = Receipt(courierResponse, orderResponse, server.logger, trip_id=tripId)
    server.logger.debug("Generated receipt.")
    server.logger.debug("Receipt id - " + currentReceipt.receiptId + ":")
    server.logger.debug(currentReceipt.data)

    #get_db_controller().insert_into_db(currentReceipt, server.logger)
    #server.logger.debug("Inserted into database.")

    #get_controller().send_email(currentReceipt)
    server.logger.debug("Sent email.")

    #test loading obj from database
    #newReceipt = get_db_controller().get_from_db("b364522a-b588-41dc-8a9d-6984878f14", server.logger, Receipt) #invalid receipt
    newReceipt = get_db_controller().get_from_db("97df8470-1a84-49fa-9164-92dcf4135b99", server.logger, Receipt) #valid receipt
    server.logger.debug("Got a new receipt")
  except Validation_Exception as e:
    server.logger.debug(e)
  except BadRequest as e:
    server.logger.debug(e)
  except Exception as e:
    server.logger.debug(e)
  finally:
    return "Successfully Received"



#Main function  
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  trip = request.json
  trip = trip['tripId'] 
  return get_all_info(trip)


if __name__ == "__main__":
  server.run(host='0.0.0.0')
