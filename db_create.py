import sqlite3
import os


database = sqlite3.connect(os.path.dirname(__file__) + "/src/database/receipts.db")

cs = database.cursor()

cs.execute("""CREATE TABLE receipts (
        receiptId TEXT NOT NULL PRIMARY KEY UNIQUE,
        information BLOB NOT NULL
    )""")

cs.close()