import sqlite3
from flask import Flask, request, render_template
import os


server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")
server.config['CONFIG_PATH'] = os.path.join(server.root_path, "config")

#import controllers
from controllers.Init_Controllers import get_controller
from controllers.Init_Controllers import get_db_controller
from controllers.Receipt import Receipt
from controllers.ValidationException import ValidationException


@server.route("/<string:trip_id>")
def load_template(trip_id):
    try:
      newReceipt = get_db_controller().get_from_db(trip_id, server.logger, Receipt) #valid receipt
      return render_template("index.html", data=newReceipt.data,receiptId=newReceipt.receiptId)
    except ValidationException:
      return "No such receipt in database."
    except sqlite3.Error:
      return "Please try again."
  

def get_all_info(tripId):
  try:
    #Request to Courier
    courierResponse = get_controller().PostRequestToCourierService(tripId)
    courierResponse = courierResponse.json()
    server.logger.info("Got courier response.")

    #Request to Order
    orderResponse = get_controller().PostReuqestToOrderService(courierResponse['orderId'])
    orderResponse = orderResponse.json()
    server.logger.info("Got order response.")

    #Creating a Receipt
    currentReceipt = Receipt(courierResponse, orderResponse, server.logger, trip_id=tripId)

    #Insert into Database
    get_db_controller().insert_into_db(currentReceipt, server.logger)

    #Sent Email
    get_controller().send_email(currentReceipt, server.logger)
    server.logger.info("Sent email.")
    return "Successfully Received"
  except (ValidationException, sqlite3.IntegrityError)  as e:
    return "Invalid or already existing receipt", 400
  except sqlite3.Error as e:
    return "The receipt couldn't be inserted into the database. Please try again.", 503
  except Exception as e:
    server.logger.info(e)
    return "Something went wrong...", 400


#Main function  
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  trip = request.json
  trip = trip['tripId'] 
  return get_all_info(trip)

@server.route("/")
def healthCheck():
  return "Healthy"


if __name__ == "__main__":
  server.run(host='0.0.0.0')
