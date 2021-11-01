import sqlite3

#initialize database
conn = sqlite3.connect("site.db")

# create cursor
c = conn.cursor()

# execute command
c.execute("""
	CREATE TABLE robot(
	id INTEGER PRIMARY KEY,
	name TEXT,
	command TEXT
	)
	""")

conn.commit()

print("Database created!")

conn.close()