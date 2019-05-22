import sqlite3
from DbConnect import *
import json
import numpy as np


def consistensycheck(nrofnodes, type):
    resultdict = {}
    iscorrect = []

    for i in range(1, nrofnodes+1):
        insidedict = {}
        if type == 1:
            insidedict[1] = dbquery(i, 1)
        else:
            for j in range(1, nrofnodes+1):
                insidedict[j] = dbquery(i, j)
        resultdict[i] = insidedict

    #for name, content in resultdict.items():
    #    print("ID:", name, "| Databases: ", content)

    for i in range(1, nrofnodes+1):
            for j in range(1, nrofnodes+1):
                iscorrect.append(resultdict[i] == resultdict[j])

    print("\nAll datbases are identical: ", all(iscorrect))
    return all(iscorrect)


def divergematrixcheck(nrofnodes):
    percentresult = 0
    matrices = {}
    npmatrices = {}
    rdict = {}
    mdict = {}
    largestmatrix = 0

    ### Reads matrices, makes them the same size if necessary and checks ###
    ### how similar they are.                                            ###
    for i in range(1, nrofnodes+1):
        file = open("testdata/divergematrix" + str(i), "r")
        text = file.readlines()
        #print(text)
        mtrx = json.loads(text[0])
        nrofmessages = json.loads(text[1])

        file.close()

        matrices[i] = mtrx
        mdict[i] = nrofmessages

        if largestmatrix < len(mtrx[0]):
            largestmatrix = len(mtrx[0])

    ### Pad matrices to be the same size ###
    for i in range(1, nrofnodes+1):
        tmpsize = largestmatrix - len(matrices[i][0])


        while tmpsize < largestmatrix and tmpsize != 0:
            for j in range(0, nrofnodes):
                matrices[i][j].append(0)

            tmpsize += 1

    ### Turn normal matrices into numpy arrays ###
    for i in range(1, nrofnodes+1):
        npmatrices[i] = np.array(matrices[i])

    ###
    for i in range(1, nrofnodes+1):
        rlist = []

        for j in range(1, nrofnodes+1):
            if i != j:
                rlist.append(np.sum(np.equal(npmatrices[i], npmatrices[j])))

        rdict[i] = rlist

    tsize = npmatrices[1].size
    for i in range(1, nrofnodes-1):
        for j in range(0, nrofnodes-1):
            rdict[i][j] = round(100-rdict[i][j]/tsize*100, 2)

    print("Divergence in procent:", rdict, "\n")
    print("Size: ", npmatrices[1].size)



#consistensycheck(4, 1)
#divergematrixcheck(8)

#consistensycheck(1)
#consistensycheck(2)


