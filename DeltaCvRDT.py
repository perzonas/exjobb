from DbConnect import *


class DeltaCvRDT:
    myvehicleid = None
    dbases = []

    def adddb(self, dbid):
        if dbid != self.myvehicleid:
            self.dbases.append(str(dbid))
        addnewdb(self.myvehicleid, dbid)

    def update(self, table, entry):
        self.delete(self.myvehicleid, table, entry[0])
        dbaddentry(self.myvehicleid, self.myvehicleid, table, entry)

    def query(self, snapshot):
        queryresult = {}
        mystate = self.getsnapshot()

        print("SNAPSHOT: ", snapshot)
        print(" ")
        print("MYSTATE: ", mystate)
        print(" ")

        for dbid, content in snapshot.items():
            if not dbexistcheck(self.myvehicleid, dbid):
                self.adddb(dbid)
                mystate = self.getsnapshot()
            else:
                querydata = {}
                for table, entry in content.items():
                    if entry < mystate[dbid][table]:
                        nrtograb = mystate[dbid][table] - entry
                        querydata[table] = dbdeltaquery(self.myvehicleid, dbid, table, nrtograb)
                        queryresult[dbid] = querydata

        return queryresult


    def merge(self, data):
        for dbid, content in data.items():
            if not dbexistcheck(self.myvehicleid, dbid):
                self.adddb(dbid)
            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if (table == "graveyard" and not dbgraveyardcheck(self.myvehicleid, dbid, entry[2], entry[3])):
                            self.delete(dbid, entry[2], entry[3])
                        elif not dbentryexist(self.myvehicleid, dbid, table, entry[0]):
                            dbaddentry(self.myvehicleid, dbid, table, entry)


    def getsnapshot(self):
        if not dbexistcheck(self.myvehicleid, self.myvehicleid):
            self.adddb(self.myvehicleid)
        state = {}
        state[self.myvehicleid] = dbgetsnapshot(self.myvehicleid, self.myvehicleid)
        for dbase in self.dbases:
            state[dbase] = dbgetsnapshot(self.myvehicleid, dbase)

        return state


    def delete(self, dbid, table, key):
        if not dbgraveyardcheck(self.myvehicleid, dbid, table, key):
            dbdeleteentry(self.myvehicleid, dbid, table, key)