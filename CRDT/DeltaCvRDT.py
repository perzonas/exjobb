from DbConnect import *


class DeltaCvRDT:
    timestamp = 0
    dict = {}

    def join(self):
        print("join")

    def query(self):
        dbquery("heaps", "11")

    def merge(self):
        print("merge")

    def compare(self, received, local):
        if received < local:
            print(1)


class Entry:
    id = 0
    timestamp = 0
    data = None


dbquery("heaps", "11")
