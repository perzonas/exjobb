from DbConnect import *
import time
import sqlite3


class StateCvRDT:
    myvehicleid = None
    dbases = []

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(self.myvehicleid, str(vehicleid))



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
            if not dbexistcheck(self.myvehicleid, dbid):
                self.adddb(dbid)
            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if table == "graveyard":
                            self.delete(entry[1:])
                        elif not dbentryexist(self.myvehicleid, dbid, table, entry[0]):
                            dbaddentry(self.myvehicleid, dbid, table, entry)


    def delete(self, entry):
        if not dbexistcheck(self.myvehicleid, self.myvehicleid):
            self.adddb(self.myvehicleid)
        dbdeleteentry(self.myvehicleid, entry[0], entry[1], entry[2])

