from DbConnect import *
import time


class StateCvRDT:
    vehicleid = None
    timestamp = 0
    data = {}

    def adddb(self, vehicleid):
        addnewdb(vehicleid)

    def query(self):
        return dbquery()

    def queryid(self, id):
        pass

    def compare(self, table, entry):
        entryexist(table, entry)

    def merge(self):
        self.data['customers'] = (9, 'test2', '55', 'herp', 'derp', 1337, 'durr')
        vehicleid = 'test3'

        if not dbexistcheck(vehicleid):
            self.adddb(vehicleid)
            pass

        for table, content in self.data.items():
            if content:
                if not self.compare(table, content[0]):
                    addentry(table, content)

    def garbagecheck(self):
        dbgarbagecheck()