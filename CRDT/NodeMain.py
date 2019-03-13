from StateCvRDT import *
from DeltaCvRDT import *


def main():
    crdt = StateCvRDT()
    crdt.myvehicleid = 'test3'
    print("Vanlig: ", crdt.query())
    dcrdt = DeltaCvRDT()
    dcrdt.myvehicleid = 'test3'
    result = dcrdt.getstate()
    print(result)
    result['test3']['materials'] -= 2
    result['test3']['customers'] -= 2

    print(result)
    print(dcrdt.query(result))





def receive():
    pass


def send():
    pass

main()

