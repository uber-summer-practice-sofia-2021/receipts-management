import sqlite3
from flask import g

database = "resources/database/receipts.db"

def getDb():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(database)
  db.row_factory = sqlite3.Row
  return db

def closeDbConnection():
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

db.row_factory = make_dicts