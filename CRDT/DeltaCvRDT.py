from DbConnect import *


class DeltaCvRDT:
    myvehicleid = None
    dbases = ['WorkOrderData6.db', 't']

    def adddb(self, vehicleid):
        self.dbases.append(str(vehicleid))
        addnewdb(vehicleid)

    def query(self, state):
        querydata = {}
        mystate = self.getstate()

        for vid, content in state.items():
            if vid == self.myvehicleid:
                for table, entry in content.items():
                    if entry < mystate[self.myvehicleid][table]:
                        nrtograb = mystate[self.myvehicleid][table] - entry
                        print(dbdeltaquery(self.myvehicleid, table, nrtograb))
                        querydata[self.myvehicleid] = dbdeltaquery(self.myvehicleid, table, nrtograb)
                        print("Result: ", querydata[self.myvehicleid])
            elif not dbexistcheck(vid):
                print("DB DOESN'T EXIST")
            #else:
            #    for table, entry in content.items():
            #        if entry <= mystate[vid][table]:
            #            nrtograb = mystate[vid][table]
            #            querydata[table] = dbdeltaquery(vid, table, nrtograb)

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


    def getstate(self):
        state = {}
        state[self.myvehicleid] = dbgetstate(self.myvehicleid)

        for dbase in self.dbases:
            state[dbase] = dbgetstate(dbase)

        return state


