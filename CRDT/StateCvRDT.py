from DbConnect import *
import time


class StateCvRDT:
    vehicleid = None

    def adddb(self, vehicleid):
        add(vehicleid)

    def query(self):
        return dbquery()

    def queryid(self, id):
        dbqueryid(id)

    def compare(self, state):
        pass

    def merge(self, statelist):
        for state in statelist:
            if self.compare(state):
                print(1)


class Entry:
    id = 0
    timestamp = 0
    data = None

# print(int(time.time()))
