import sqlite3
from DbConnect import *

def consistensycheck(nrofnodes):
    dbaste = {}
    for i in range(1, nrofnodes):
        for j in range(1, nrofnodes):
            dbaste[j] = dbquery(i, j)

    print(dbaste)


consistensycheck(2)