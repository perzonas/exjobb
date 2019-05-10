import sqlite3
from DbConnect import *

def consistensycheck(nrofnodes):
    resultdict = {}

    for i in range(1, nrofnodes+1):
        insidedict = {}
        for j in range(1, nrofnodes+1):
            insidedict[j] = dbquery(i, j)
        resultdict[i] = insidedict

    for name, content in resultdict.items():
        print(name, content)

    iscorrect = []

    for i in range(1, nrofnodes+1):
        for j in range(1, nrofnodes+1):
            for k in range(1, nrofnodes+1):
                

consistensycheck(2)