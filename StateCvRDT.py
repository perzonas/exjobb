from DbConnect import *
import time


class StateCvRDT:
    myvehicleid = None
    dbases = []

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(vehicleid)

    def update(self, myvid, table, row):
        dbaddentry(myvid, table, row)

    def query(self):
        querydata = {}
        querydata[self.myvehicleid] = dbquery(self.myvehicleid)

        for dbase in self.dbases:
            querydata[dbase] = dbquery(dbase)

        return querydata

    def compare(self, dbid, table, entry):
        dbentryexist(dbid, table, entry)

    def merge(self, data):
        for vid, content in data.items():
            if not vid == self.myvehicleid:
                if not dbexistcheck(vid):
                    self.adddb(vid)

                for table, entry in content.items():
                    if content:
                        if not self.compare(vid, table, content[0]):
                            dbaddentry(vid, table, content)

        # CALL FOR BROADCAST

    def garbagecheck(self):
        dbgarbagecheck()