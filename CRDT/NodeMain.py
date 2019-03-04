from StateCvRDT import *


def main():
    crdt = StateCvRDT()
    result = crdt.query()

    print(result)

    crdt.vehicleid = 1
    print(crdt.vehicleid)


main()

