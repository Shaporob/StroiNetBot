import sqlite3 as sq

db = sq.connect("database/database.db", detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES)
cur = db.cursor()
