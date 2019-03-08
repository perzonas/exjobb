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
        data = {}
        data['customers'] = (9, 'test2', '55', 'herp', 'derp', 1337, 'durr')

        for table, content in data.items():
            if content:
                if not self.compare(table, content[0]):
                    addentrytotable(table, content)



# print(int(time.time()))
