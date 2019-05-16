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
        print("ID:", name, "| Databases: ", content)

    iscorrect = []


    for i in range(1, nrofnodes+1):
        for j in range(1, nrofnodes+1):
            iscorrect.append(resultdict[i] == resultdict[j])


    print("\nAll datbases are identical: ", all(iscorrect))



consistensycheck(8)