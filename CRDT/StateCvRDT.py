from DbConnect import *
import time


class StateCvRDT:
    myvehicleid = None
    dbases = ['WorkOrderData6.db']

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(vehicleid)

    def query(self):
        querydata = {}
        querydata[self.myvehicleid] = dbquery(self.myvehicleid)

        for dbase in self.dbases:
            querydata[dbase] = dbquery(dbase)

        return querydata

    def compare(self, dbid, table, entry):
        entryexist(dbid, table, entry)

    def merge(self, data):
        for vid, content in data.items():
            if not vid == self.myvehicleid:
                if not dbexistcheck(vid):
                    self.adddb(vid)

                for table, entry in content.items():
                    if content:
                        if not self.compare(vid, table, content[0]):
                            addentry(table, content)

    def garbagecheck(self):
        dbgarbagecheck()