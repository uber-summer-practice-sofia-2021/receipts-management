import pickle
import os
from mysql.connector.connection import MySQLConnection
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from controllers.ValidationException import ValidationException


class Database_Controller:
  def __init__(self):
    url = os.environ['DATABASE_URL']
    self.engine = sqlalchemy.create_engine(url)

  def __serialize_data(self, data):
    serialized = pickle.dumps(data)
    return serialized

  def __deserialize_data(self, data):
    deserialized = pickle.loads(data)
    return deserialized

  def insert_into_db(self, receiptObj, logger):
    logger.info("Inserting into the database")
    try:
      with self.engine.begin() as connection:
        data_tuple = (receiptObj.receiptId, self.__serialize_data(receiptObj.data))
        command= """ INSERT INTO receipts (receiptId, information) VALUES (%s, %s)"""
        logger.info("EXECUTING COMMAND")
        connection.execute(command, data_tuple)
        logger.info("Commited to database")
    except Exception  as e:
      logger.info(e)
      raise ValidationException("Already in the database") from e

  def get_from_db(self, u_id, logger, Receipt):
    try:
        with self.engine.begin() as connection:
          command = """SELECT *
                  FROM receipts 
                  WHERE receiptId LIKE %s """
          data = connection.execute(command, (u_id,))
          data = data.fetchone()
          if(data is None):
            raise IndexError
          newReceipt = Receipt(data[0], self.__deserialize_data(data[1]),logger, alt=True)
          return newReceipt
    except IndexError as e:
      raise ValidationException("No such receipt in database.") from e
    except Exception as e:
      raise SQLAlchemyError("Something went wrong with the database.") from e
    finally:
      logger.info("CLOSING DATABASE CONNECTION")
      connection.close()
