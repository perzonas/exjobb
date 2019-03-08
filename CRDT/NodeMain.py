from StateCvRDT import *


def main():
    crdt = StateCvRDT()
    crdt.merge()
    result = crdt.query()

    print(result)


def receive():
    pass


def send():
    pass

main()

