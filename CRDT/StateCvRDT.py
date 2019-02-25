from dbconnect import *
import time


class Database:
    timestamp = time.time()
    name = None  # should look something like 'WorkOrderData6.db'


class StateCvRDT:
    databases = {}
    myvehicleid = None
    mydb = Database()
    mydb.name = myvehicleid

    def add(self, vehicleid):

            db = Database()
            db.name = vehicleid
            databases[vehicleid] = db

    def query(self):
        dbquery()

    def queryid(self, id):
        dbqueryid(id)

    def compare(self, state):
        if state.vehicleid not in databases:
            self.add(state.vehicleid)
        else:
            localdb = self.dquery(state.vehicleid)
            if localdb.timestamp < state.timestamp:
                return True

    def merge(self, statelist):
        for s in statelist:
            if self.compare(s):
                print(1)


class Entry:
    id = 0
    timestamp = 0
    data = None


# dbquery()

print(int(time.time()))