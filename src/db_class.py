import sqlite3
from sqlite3.dbapi2 import DatabaseError
from flask import g


class DB:
  def __init__(self, path):
    self.__database = path

  def __getDb(self):
    db = getattr(g, '_database', None)
    if db is None:
      db = g._database = sqlite3.connect(self.__database)
    return db

  def __closeDbConnection(self):
    db = getattr(g, '_database', None)
    if db is not None:
      db.close()

  def make_dicts(cursor, row):
      return dict((cursor.description[idx][0], value)
                  for idx, value in enumerate(row))
                  
  def query_db(self, query, args=(), one=False):
    cur = self.__getDb().execute(query, args)
    rv = cur.fetchall()
    self.__closeDbConnection()
    return (rv[0] if rv else None) if one else rv

  
