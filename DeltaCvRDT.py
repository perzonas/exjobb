from DbConnect import *
import numpy as np
import json

class DeltaCvRDT:
    myid = None
    dbases = []
    messagecounter = 1
    nrofhosts = 0

    ### Y-axis is nodes in ascending order (node 1 top of matrix, node 8 bottom) ###
    ### and X-axis is messagenumber 1-infitiny ###
    divergematrix = []

    def adddb(self, dbid):
        if dbid != self.myid:
            self.dbases.append(str(dbid))
        addnewdb(self.myid, dbid)

    def update(self, table, entry):
        self.delete(self.myid, table, entry[0])
        dbaddentry(self.myid, self.myid, table, entry)

    def query(self, snapshot):
        queryresult = {}
        mystate = self.getsnapshot()

        for dbid, content in snapshot.items():
            if not dbexistcheck(self.myid, dbid):
                self.adddb(dbid)
                mystate = self.getsnapshot()
            else:
                querydata = {}
                for table, entry in content.items():
                    if int(entry) < mystate[dbid][table]:
                        nrtograb = mystate[dbid][table] - entry
                        querydata[table] = dbdeltaquery(self.myid, dbid, table, nrtograb)
                        queryresult[dbid] = querydata

        return queryresult


    def merge(self, data):
        for dbid, content in data.items():
            if not dbexistcheck(self.myid, dbid):
                self.adddb(dbid)
            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if table == "graveyard" and not dbgraveyardcheck(self.myid, dbid, entry[2], entry[3]):
                            self.delete(dbid, entry[2], entry[3])
                        elif not dbentryexist(self.myid, dbid, table, entry[0]):
                            dbaddentry(self.myid, dbid, table, entry)


    def getsnapshot(self):
        if not dbexistcheck(self.myid, self.myid):
            self.adddb(self.myid)
        state = {}
        state[self.myid] = dbgetsnapshot(self.myid, self.myid)
        for dbase in self.dbases:
            state[dbase] = dbgetsnapshot(self.myid, dbase)

        return state


    def delete(self, dbid, table, key):
        if not dbgraveyardcheck(self.myid, dbid, table, key):
            dbdeleteentry(self.myid, dbid, table, key)


    def creatematrix(self, nrofhosts):
        for i in range(0, nrofhosts):
            self.divergematrix.append([0])


    def matrixupdate(self, sender, messagenumber, prnt):
        while len(self.divergematrix[0]) < messagenumber:
            for i in range(0, len(self.divergematrix)):
                self.divergematrix[i].append(0)
        print("\nSENDER: ", sender, "MESSAGENUMBER: ", messagenumber, "\n" )
        self.divergematrix[int(sender)-1][messagenumber-1] = 1

        if prnt == True:
            for li in self.divergematrix:
                toprint = "|"
                for x in li:
                    toprint += " " + str(x)
                toprint += " |"
                print(toprint)

        self.writeDivergeMatrix()


    def writeDivergeMatrix(self):
        file = open("testdata/divergematrix" + str(self.myid), "w")
        os.chmod("testdata/divergematrix" + str(self.myid), 0o777)
        file.write(json.dumps(self.divergematrix) + "\n")
        file.write(json.dumps(self.messagecounter))
        file.close()