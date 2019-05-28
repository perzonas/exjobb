from DbConnect import *
import time
import json
import sqlite3


class StateCvRDT:
    myid = None
    dbases = []
    messagecounter = 1
    nrofhosts = 0
    ### Y-axis is nodes in ascending order (node 1 top of matrix, node 8 bottom) ###
    ### and X-axis is messagenumber 1-infitiny ###
    divergematrix = []

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(self.myid, str(vehicleid))



    def update(self, table, entry):
        if not dbexistcheck(self.myvehicleid, self.myvehicleid):
            self.adddb(self.myvehicleid)
        self.delete([self.myvehicleid, table, entry[0]])
        dbaddentry(self.myvehicleid, self.myvehicleid, table, entry)

    def query(self):
        querydata = {}
        if not dbexistcheck(self.myvehicleid, self.myvehicleid):
            self.adddb(self.myvehicleid)
        querydata[self.myvehicleid] = dbquery(self.myvehicleid, self.myvehicleid)

        for dbase in self.dbases:
            try:
                if not dbexistcheck(self.myvehicleid, dbase):
                    self.adddb(dbase)

                querydata[dbase] = dbquery(self.myvehicleid, dbase)
            except sqlite3.OperationalError as e:
                print("####################################")
                print("ERROR WHEN QUERYING DB %s" % dbase)
                print("####################################")

        return querydata


    def merge(self, data):
        for dbid, content in data.items():
            if not dbexistcheck(self.myid, dbid):
                self.adddb(dbid)
            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if table == "graveyard":
                            self.delete(entry[1:])
                        elif not dbentryexist(self.myid, dbid, table, entry[0]):
                            dbaddentry(self.myid, dbid, table, entry)


    def delete(self, entry):
        if not dbexistcheck(self.myvehicleid, self.myvehicleid):
            self.adddb(self.myvehicleid)
        dbdeleteentry(self.myvehicleid, entry[0], entry[1], entry[2])

    def creatematrix(self, nrofhosts):
        for i in range(0, nrofhosts):
            self.divergematrix.append([0])


    def matrixupdate(self, sender, messagenumber, prnt):
        while len(self.divergematrix[0]) < messagenumber:
            for i in range(0, len(self.divergematrix)):
                self.divergematrix[i].append(0)
        self.divergematrix[int(sender)-1][messagenumber-1] = 1
        if prnt == True:
            for li in self.divergematrix:
                toprint = "|"
                for x in li:
                    toprint += " " + str(x)
                toprint += " |"
                print(toprint)

        print("\n")
        self.writeDivergeMatrix()


    def writeDivergeMatrix(self):
        file = open("testdata/divergematrix" + str(self.myid), "w")
        os.chmod("testdata/divergematrix" + str(self.myid), 0o777)
        file.write(json.dumps(self.divergematrix) + "\n")
        file.write(json.dumps(self.messagecounter))
        file.close()