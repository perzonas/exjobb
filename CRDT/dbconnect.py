import sqlite3


databases = {}
# conn = sqlite3.connect('WorkOrderData6.db')
# conn = sqlite3.connect('example.db')

# c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE stocks
#            (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
# conn.commit()


def add(dbid, timestamp):
    databases[dbid ]


def dbquery():
    conn = sqlite3.connect('WorkOrderData6.db')
    # conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute('SELECT * FROM targets')
    print(c.fetchall())

    conn.close()


def dbqueryid(id):
    conn = sqlite3.connect('WorkOrderData6.db')
    # conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute('SELECT * FROM states WHERE h_target=?', id)  # table names cannot be parametrized
    print(c.fetchone())

    conn.close()


# def dbadd(id, )

# conn.close()

