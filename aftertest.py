import sqlite3
from DbConnect import *
import json
import numpy as np


def consistensycheck(nrofnodes, type):

    resultdict = {}
    iscorrect = []
    wrong = []
    try:
        # centralized solution testing
        if type == 1:
            first = dbquery(1, 1)
            for i in range(2, nrofnodes + 1):
                other = dbquery(i, 1)
                if first == other:
                    iscorrect.append(True)
                else:
                    bool = True
                    for table in first:
                        if not len(first[table]) == len(other[table]):
                            bool = False
                    if bool:
                        print("LENGTH")
                        iscorrect.append(True)
                    else:
                        iscorrect.append(False)
                        wrong.append("Node%d db %d differs from Node%d db %d\n" % (1, 1, i, 1))

        # CRDT solutions
        else:
            first = {}

            for i in range(1, nrofnodes + 1):
                for j in range(1, nrofnodes + 1):
                    if j == 1:
                        first = dbquery(j, i)
                    else:
                        other = dbquery(j, i)
                        if first == other:
                            iscorrect.append(True)
                        else:
                            bool = True
                            for table in first:
                                if not len(first[table]) == len(other[table]):
                                    bool = False
                            if bool:
                                print("LENGTH")
                                iscorrect.append(True)
                            else:
                                iscorrect.append(False)
                                wrong.append("Node%d db %d differs from Node%d db %d\n" % (1, i, j, i))



        if all(iscorrect):
            print("ALL NODES HAVE CONVERGED!!")
            return True
        else:
            for line in wrong:
                print(line)
            return False

    except sqlite3.OperationalError as e:
        print("ERROR", e)
        return False
'''

    resultdict = {}
    iscorrect = []
    try:

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

        print(iscorrect)
        return all(iscorrect)
    except sqlite3.OperationalError:
        return False
'''

def divergematrixcheck(nrofnodes):
    percentresult = 0
    matrices = {}
    npmatrices = {}
    rdict = {}
    mdict = {}
    largestmatrix = 0
    smallestmatrix = 0

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
        elif smallestmatrix == 0 or smallestmatrix > len(mtrx[0]):
            smallestmatrix = len(mtrx[0])

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
    for i in range(1, nrofnodes+1):
        for j in range(0, nrofnodes-1):
            rdict[i][j] = round(100-rdict[i][j]/tsize*100, 2)

    for id, matrix in matrices.items():
        for li in matrix:
            toprint = "|"
            for x in li:
                toprint += " " + str(x)
            toprint += " |"
            print(toprint)
        print("\n")

    npm = npmatrices[1].shape
    groundmatrix = np.ones(npm)
    print(npm, "\n")
    print(groundmatrix)

    gtrdict = {}
    for i in range(1, nrofnodes+1):
        gtrdict[i] = np.sum(np.equal(npmatrices[i], groundmatrix))

    print("Number of messages sent: ", mdict)
    print("Divergence in procent:", rdict, "\n")
    print("Number of messages sent divergence:", largestmatrix-smallestmatrix)
    print("Ground truth: ", gtrdict)



#consistensycheck(16, 3)
divergematrixcheck(8)

#consistensycheck(1)
#consistensycheck(2)


