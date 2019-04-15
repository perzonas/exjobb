from DbConnect import *
import time


class StateCvRDT:
    myvehicleid = None
    dbases = []

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(self.myvehicleid, str(vehicleid))

    def updaterow(self, myvid, table, oldrow, newrow):
        self.delete(myvid, table, oldrow)
        dbaddentry(self.myvehicleid, myvid, table, newrow)

    def query(self):
        querydata = {}
        querydata[self.myvehicleid] = dbquery(self.myvehicleid, self.myvehicleid)

        for dbase in self.dbases:
            querydata[dbase] = dbquery(self.myvehicleid, dbase)

        return querydata

    def compare(self, dbid, table, key):
        dbcheck = dbentryexist(self.myvehicleid, dbid, table, key)
        gravecheck = dbgraveyardcheck(self.myvehicleid, dbid, table, key)
        return dbcheck or gravecheck

    def merge(self, data):
        for dbid, content in data.items():
            if not dbexistcheck(self.myvehicleid, dbid):
                self.adddb(dbid)

            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if not self.compare(dbid, table, entry[0]):
                            dbaddentry(self.myvehicleid, dbid, table, entry)


    def delete(self, entry):
        dbdeleteentry(self.myvehicleid, entry)