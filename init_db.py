
import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS properties(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
address TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS units(
id INTEGER PRIMARY KEY AUTOINCREMENT,
property_id INTEGER,
name TEXT,
rent REAL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
property_id INTEGER,
unit_id INTEGER,
date TEXT,
type TEXT,
category TEXT,
amount REAL,
notes TEXT
)
''')

conn.commit()
conn.close()
