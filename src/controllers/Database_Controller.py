import sqlite3
import json
import os
import pickle
import sqlalchemy


class Database_Controller:
  def __init__(self, path):
    with open(path) as file:  
      self.db_directory = json.load(file)
      self.db_directory = os.path.dirname(os.path.dirname(__file__)) + self.db_directory['path']
      self.my_pool = sqlalchemy.pool.QueuePool(self.get_connection, max_overflow=10, pool_size=6)

  def get_connection(self):
    connection = sqlite3.connect(self.db_directory)
    return connection

  def __serialize_data(self, data):
    serialized = pickle.dumps(data)
    return serialized

  def __deserialize_data(self, data):
    deserialized = pickle.loads(data)
    return deserialized

  def insert_into_db(self, receiptObj, logger):
    logger.debug("Inserting")
    try:
      connection = self.my_pool.connect()
      db_cursor = connection.cursor() 
      data_tuple = (receiptObj.receiptId, self.__serialize_data(receiptObj.data))
      command= """ INSERT INTO receipts (receiptId, information) VALUES (?, ?)"""
      db_cursor.execute(command, data_tuple)
      connection.commit()
      connection.close()
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as db_error:
      logger.debug(db_error.detail)
    except (sqlite3.Error) as db_error:
      logger.debug(db_error)
    finally:
      connection.close()

  def get_from_db(self, u_id, logger, Receipt):
    logger.debug("Selecting")
    try:
      connection = self.my_pool.connect()
      db_cursor = connection.cursor()
      logger.debug("Just before command")
      command = """SELECT * 
              FROM receipts 
              WHERE receiptId = ? """
      db_cursor.execute(command, (u_id,))
      data = db_cursor.fetchall()
      newReceipt = Receipt(data[0][0], self.__deserialize_data(data[0][1]))
      connection.close()
      return newReceipt
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as db_error:
      logger.debug(db_error.detail)
    except (sqlite3.Error) as db_error:
      logger.debug(db_error)
    finally:
      connection.close()

  
