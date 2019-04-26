from DbConnect import *
import time


class StateCvRDT:
    myvehicleid = None
    dbases = []

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(self.myvehicleid, str(vehicleid))


    def update(self, table, entry):
        print("Entry in UPDATE IS: ", entry)
        self.delete([0, self.myvehicleid, table, entry[0]])
        dbaddentry(self.myvehicleid, self.myvehicleid, table, entry)

    def query(self):
        querydata = {}
        querydata[self.myvehicleid] = dbquery(self.myvehicleid, self.myvehicleid)

        for dbase in self.dbases:
            querydata[dbase] = dbquery(self.myvehicleid, dbase)

        return querydata


    def merge(self, data):
        for dbid, content in data.items():
            if not dbexistcheck(self.myvehicleid, dbid):
                self.adddb(dbid)
            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if table == "graveyard":
                            self.delete(entry)
                        elif not dbentryexist(self.myvehicleid, dbid, table, entry[0]):
                            dbaddentry(self.myvehicleid, dbid, table, entry)


    def delete(self, entry):

        #### Input is __ID, DATABASE_ID, table and rowID  ####
        if not dbgraveyardcheck(self.myvehicleid, entry[1], entry[2], entry[3]):
            dbdeleteentry(self.myvehicleid, entry[1], entry[2], entry[3])
