import sqlite3

# Connect to the database
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

# Create a table to store tasks if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed INTEGER)''')

# Commit changes and close connection
conn.commit()
conn.close()
