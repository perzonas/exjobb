from StateCvRDT import *
from DeltaCvRDT import *


def main():
    crdt = StateCvRDT()
    crdt.myvehicleid = 'test3'
    print("Vanlig: ", crdt.query())
    d = {'test3': {'customers': [(6, 'six', '66', 'sectiosex', 'sixtys', 60, 'saxtio'),(7, 'i', '8765', 'x', 's', 41, 'o')], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [(1, '', 555, 'test'), (2, 'test', 555, '')], 'table_properties': [], 'targets': [], 'waybills': []}}
    crdt.merge(d)
    print("Vanlig updated: ", crdt.query())
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

