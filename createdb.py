import sqlite3
"""
conn = sqlite3.connect('users.db')

print("Opened users Database successfully")

cursorObj = conn.cursor()

cursorObj.execute('CREATE TABLE users \
                  (Name TEXT NOT NULL,\
                   Age INT NOT NULL, \
                   Gender VARCHAR(20) NOT NULL, \
                   email TEXT);')

conn.commit()

print("Table created successfully")

conn.close()
"""

conn = sqlite3.connect('users.sqlite3')

cursorObj = conn.cursor()

cursorObj.execute('DELETE FROM Users;')
conn.commit()
print("values inserted successfully")
conn.close()