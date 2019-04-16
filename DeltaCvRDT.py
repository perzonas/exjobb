from DbConnect import *


class DeltaCvRDT:
    myvehicleid = None
    dbases = []

    def adddb(self, dbid):
        self.dbases.append(str(dbid))
        addnewdb(self.myvehicleid, dbid)

    def update(self, myvid, table, row):
        dbaddentry(myvid, table, row)

    def query(self, snapshot):
        queryresult = {}
        mystate = self.getstate()

        for dbid, content in snapshot.items():
            if not dbexistcheck(self.myvehicleid, dbid):
                self.adddb(dbid)
            else:
                querydata = {}
                for table, entry in content.items():
                    if entry < mystate[dbid][table]:
                        nrtograb = mystate[dbid][table] - entry
                        querydata[table] = dbdeltaquery(self.myvehicleid, dbid, table, nrtograb)
                        queryresult[dbid] = querydata

        return queryresult


    def compare(self, dbid, table, entry):
        dbcheck = dbentryexist(self.myvehicleid, dbid, table, entry)
        gravecheck = dbgraveyardcheck(self.myvehicleid, self.myvehicleid, table, entry)
        return dbcheck or gravecheck


    def merge(self, data):
        for dbid, content in data.items():
            if not dbexistcheck(self.myvehicleid, dbid):
                self.adddb(dbid)

            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if table == "graveyard":
                            print("MENTRY: ", entry)
                        if table == "graveyard" and not dbgraveyardcheck(self.myvehicleid, dbid, table, entry):
                            self.delete(entry)
                        elif not self.compare(dbid, table, entry[0]):
                            dbaddentry(self.myvehicleid, dbid, table, entry)
                        else:
                            print("SKIPPING: ", dbid, " | ", table, " | ", entry)


    def getstate(self):
        state = {}
        state[self.myvehicleid] = dbgetstate(self.myvehicleid, self.myvehicleid)

        for dbase in self.dbases:
            state[dbase] = dbgetstate(self.myvehicleid, dbase)

        return state


    def delete(self, entry):
        if not dbgraveyardcheck(self.myvehicleid, entry[0], entry[1], entry[2]):
            dbdeleteentry(self.myvehicleid, entry[0], entry[1], entry[2])