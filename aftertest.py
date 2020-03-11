import sqlite3
from DbConnect import *
import json
import numpy as np
import sys


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


def divergematrixcheck(nrofnodes):
    matrices = {}
    msgdict = {}

    for i in range(1, nrofnodes+1):
        file = open("testdata/divergematrices/divergematrix" + str(i), "r")
        text = file.readlines()
        mtrx = json.loads(text[0])
        nrofmessages = json.loads(text[1])

        file.close()

        matrices[i] = mtrx
        msgdict[i] = nrofmessages

    ### Count zeroes in matrix ###
    totalzeroes = 0
    worstnode = (0, 0)
    totalmessages = 0
    rowzeroes = (0,0)
    tmpz = 0

    for i in range(1, nrofnodes+1):
        tmpworstnode = 0
        for j in range(0, nrofnodes):
            for k in range(0, len(matrices[i][j])):
                if matrices[i][j][k] == 0:
                    totalzeroes += 1
                    tmpworstnode += 1
                    tmpz += 1
                else:
                    if tmpz > rowzeroes[1]:
                        rowzeroes = (i,tmpz)
                    else:
                        tmpz = 0
                    totalmessages +=1

        if tmpworstnode > worstnode[1]:
            worstnode = (i, tmpworstnode)

    print(totalzeroes)
    print(worstnode)
    print(rowzeroes)
    printmatrices(matrices)

    file = open("testdata/divergematrix" + str(1), "a")
    file.write(json.dumps(totalzeroes) + "\n")
    file.write(json.dumps(worstnode) + "\n")
    file.write(json.dumps(rowzeroes))
    file.close()

    '''
    ### Pad matrices to be the same size ###
    for i in range(1, nrofnodes+1):
        while len(matrices[i][0]) < largestmatrix:
            for j in range(0, nrofnodes):
                matrices[i][j].append(0)
    
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
            rdict[i][j] = round(100-rdict[i][j]/float(tsize)*100, 2)
    #printmatrices(matrices)

    groundmatrix = np.ones(npmatrices[1].shape)
    npm = 0

    gtrdict = {}
    for i in range(1, nrofnodes+1):
        gtrdict[i] = np.sum(np.equal(npmatrices[i], groundmatrix))

        if i == 1 or npm > gtrdict[1]:
            npm = gtrdict[i]

    print("NPM: ", npm, "GT: ", groundmatrix.size, "r: ", round(100-npm/float(groundmatrix.size)*100, 2))
    npm = round(100-npm/float(groundmatrix.size)*100, 2)
    
    print("Number of messages sent: ", msgdict)
    print("Divergence in procent:", rdict, "\n")
    print("Number of messages sent divergence:", largestmatrix-smallestmatrix)
    #print("Ground truth: ", gtrdict)
    #print(npm)

    file = open("testdata/divergematrix" + str(1), "a")
    file.write(json.dumps(rdict) + "\n")
    file.write(json.dumps(npm))
    file.close()
    '''


def listcheck(nrofnodes):
    matrix = []
    for i in range(2, nrofnodes+1):
        file = open("testdata/divergelist" + str(i), "r")
        text = file.readlines()
        list = json.loads(text[0])

        matrix.append(list)

    #print(matrix)

    totalzeroes = 0
    worstnode = (0, 0)
    totalmessages = 0
    rowzeroes = (0, 0)
    tmpz = 0

    for j in range(0, nrofnodes-1):
        tmpworstnode = 0
        print(str(matrix[j]).replace(",", ""))
        for k in range(0, len(matrix[j])):
            if matrix[j][k] == 0:
                totalzeroes += 1
                tmpworstnode += 1
                tmpz += 1
            else:
                if tmpz > rowzeroes[1]:
                    rowzeroes = (j+2, tmpz)
                else:
                    tmpz = 0
                totalmessages += 1

            if tmpworstnode > worstnode[1]:
                worstnode = (j+2, tmpworstnode)

    print(totalzeroes)
    print(worstnode)
    print(rowzeroes)

    file = open("testdata/divergelist" + str(2), "a")
    file.write(json.dumps(totalzeroes) + "\n")
    file.write(json.dumps(worstnode) + "\n")
    file.write(json.dumps(rowzeroes))
    file.close()

def printmatrices(matrices):
    for id, matrix in matrices.items():
        for li in matrix:
            toprint = "|"
            for x in li:
                toprint += " " + str(x)
            toprint += " |"
            print(toprint)
        print("\n")


### Checks how different ways the nodes took to converge ###
def divergeways(nrofnodes):
    percentresult = 0
    matrices = {}
    npmatrices = {}
    rdict = {}
    msgdict = {}
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
        msgdict[i] = nrofmessages

        if largestmatrix < len(mtrx[0]):
            largestmatrix = len(mtrx[0])
        elif smallestmatrix == 0 or smallestmatrix > len(mtrx[0]):
            smallestmatrix = len(mtrx[0])

    ### Pad matrices to be the same size ###
    for i in range(1, nrofnodes+1):
        while len(matrices[i][0]) < largestmatrix:
            for j in range(0, nrofnodes):
                matrices[i][j].append(0)

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
            rdict[i][j] = round(100-rdict[i][j]/float(tsize)*100, 2)

    for id, matrix in matrices.items():
        for li in matrix:
            toprint = "|"
            for x in li:
                toprint += " " + str(x)
            toprint += " |"
            print(toprint)
        print("\n")

    groundmatrix = np.ones(npmatrices[1].shape)
    npm = 0

    gtrdict = {}
    for i in range(1, nrofnodes+1):
        gtrdict[i] = np.sum(np.equal(npmatrices[i], groundmatrix))

        if i == 1 or npm > gtrdict[1]:
            npm = gtrdict[i]

    print("NPM: ", npm, "GT: ", groundmatrix.size, "r: ", round(100-npm/float(groundmatrix.size)*100, 2))
    npm = round(100-npm/float(groundmatrix.size)*100, 2)

    print("Number of messages sent: ", msgdict)
    print("Divergence in procent:", rdict, "\n")
    print("Number of messages sent divergence:", largestmatrix-smallestmatrix)
    print("Ground truth: ", gtrdict)
    print(npm)

    file = open("testdata/divergematrix" + str(1), "a")
    file.write(json.dumps(rdict) + "\n")
    file.write(json.dumps(npm))
    file.close()



if __name__ == '__main__':
    divergematrixcheck(16)
    #listcheck(16)
    pass