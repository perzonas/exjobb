from StateCvRDT import *
from DeltaCvRDT import *


def main():
    crdt = StateCvRDT()
    crdt.myvehicleid = 'test5'
    print("Vanlig: ", crdt.query())
    #crdt.update('test3', 'customers', (1, 'asd', '222', 'dsft', 'sSDSDre', 2, 'beEFSrra'))

    #dcrdt = DeltaCvRDT()
    #dcrdt.myvehicleid = 'test3'
    #result = dcrdt.getstate()
    #print("State: ", result)
    #result['test3']['customers'] -= 2
    #result['WorkOrderData6.db']['materials'] -= 4
    #print("Result: ", result)
    #print(dcrdt.query(result))





def receive():
    pass


def send():
    pass

main()

