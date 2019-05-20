from DbConnect import *


class DeltaCvRDT:
    myid = None
    dbases = []
    messagecounter = 1
    divergematrix = [[1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0]]

    def adddb(self, dbid):
        if dbid != self.myid:
            self.dbases.append(str(dbid))
        addnewdb(self.myid, dbid)

    def update(self, table, entry):
        self.delete(self.myid, table, entry[0])
        dbaddentry(self.myid, self.myid, table, entry)

    def query(self, tuperu):
        #print("\nTUPERU: ", tuperu, "\n")
        snapshot = tuperu[0]
        queryresult = {}
        mystate = self.getsnapshot()

        if tuperu[1][0] != 0:
            self.matrixupdate(tuperu[1][0], tuperu[1][1])


        for dbid, content in snapshot.items():
            if not dbexistcheck(self.myid, dbid):
                self.adddb(dbid)
                mystate = self.getsnapshot()
            else:
                querydata = {}
                for table, entry in content.items():
                    if entry < mystate[dbid][table]:
                        nrtograb = mystate[dbid][table] - entry
                        querydata[table] = dbdeltaquery(self.myid, dbid, table, nrtograb)
                        queryresult[dbid] = querydata

        return queryresult


    def merge(self, data):
        for dbid, content in data.items():
            if not dbexistcheck(self.myid, dbid):
                self.adddb(dbid)
            for table, tlist in content.items():
                if tlist:
                    for entry in tlist:
                        if (table == "graveyard" and not dbgraveyardcheck(self.myid, dbid, entry[2], entry[3])):
                            self.delete(dbid, entry[2], entry[3])
                        elif not dbentryexist(self.myid, dbid, table, entry[0]):
                            dbaddentry(self.myid, dbid, table, entry)


    def getsnapshot(self):
        if not dbexistcheck(self.myid, self.myid):
            self.adddb(self.myid)
        state = {}
        state[self.myid] = dbgetsnapshot(self.myid, self.myid)
        for dbase in self.dbases:
            state[dbase] = dbgetsnapshot(self.myid, dbase)

        return state


    def delete(self, dbid, table, key):
        if not dbgraveyardcheck(self.myid, dbid, table, key):
            dbdeleteentry(self.myid, dbid, table, key)


    #def updatematrix(self, sender, messagenumber):
    #    if self.divergematrix.shape < (8, messagenumber):
    #        self.divergematrix = np.pad(self.divergematrix, (0,messagenumber), 'constant', constant_values=0)
    #        self.divergematrix.resize(8, messagenumber+3)

        #self.divergematrix[sender][messagenumber] = messagenumber

    #    print(self.divergematrix)


    def matrixupdate(self, sender, messagenumber):
        while len(self.divergematrix[0])-1 < messagenumber:
            for i in range(0,8):
                self.divergematrix[i].append(0)

        self.divergematrix[int(sender)-1][messagenumber] = "X"

        for li in self.divergematrix:
            toprint = "|"
            for x in li:
                toprint += " " + str(x)
            toprint += " |"
            print(toprint)