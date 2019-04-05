from DbConnect import *
import time


class StateCvRDT:
    myvehicleid = None
    dbases = []

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(self.myvehicleid, str(vehicleid))

    def update(self, myvid, table, row):
        dbaddentry(self.myvehicleid, myvid, table, row)

    def query(self):
        querydata = {}
        #querydata[self.myvehicleid] = dbquery(self.myvehicleid)

        for dbase in self.dbases:
            querydata[dbase] = dbquery(dbase)

        return querydata

    def compare(self, dbid, table, entry):
        dbentryexist(self.myvehicleid, dbid, table, entry)

    def merge(self, data):
        for vid, content in data.items():
            if not dbexistcheck(self.myvehicleid, vid):
                self.adddb(vid)

            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if not self.compare(vid, table, entry[0]):
                            dbaddentry(self.myvehicleid, vid, table, entry)


    def garbagecheck(self):
        dbgarbagecheck()