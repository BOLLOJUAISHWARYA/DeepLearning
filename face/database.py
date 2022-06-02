import sqlite3

conn = sqlite3.connect('database.db')
print('opened')
conn.execute(""" CREATE TABLE details(id integer primary key autoincrement ,name VARCHAR(255) NOT NULL UNIQUE ,password varchar(255))""")
print('Table created')
conn.close()
