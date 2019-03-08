import sqlite3

db = sqlite3.connect('fre', isolation_level=None)
c = db.cursor()

# c.execute('''CREATE TABLE person(id integer primary key autoincrement, name text, age integer)''')

c.execute(''' INSERT INTO person(name,age)
              VALUES(?,?) ''', ('c', 5))

c.execute(''' INSERT INTO person(name,age)
              VALUES(?,?) ''', ('d', 5))

c.execute('SELECT * FROM person')

print(c.fetchall())


c.close()
