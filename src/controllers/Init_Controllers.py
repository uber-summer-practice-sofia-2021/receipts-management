from controllers.Receipt import Receipt
from controllers.Controller import Controller
from controllers.Database_Controller import Database_Controller
from server import server
from flask import g

def get_controller():
  controller = getattr(g, '_my_controller', None)
  if controller is None:
    g._my_controller = Controller(server.config['CONFIG_PATH'] + "/HTTPClients.json")
  return g._my_controller


def get_db_controller():
    db_controller = getattr(g, '_database', None)
    if db_controller is None:
        g._database = Database_Controller()
    return g._database

