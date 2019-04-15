from StateCvRDT import *
from DeltaCvRDT import *


def main():
    crdt = DeltaCvRDT()
    crdt.myvehicleid = 'test3'
    print("Vanlig: ", dbquery(crdt.myvehicleid, crdt.myvehicleid))
    d = {'test3': {'graveyard': [], 'customers': [(1, 'six', '66', 'sectiosex', 'sixtys', 60, 'saxtio'), (2, 'i', '8765', 'x', 's', 41, 'o'), (3, 'a', '8768', 'a', 'a', 11, 'a')], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [(1, '', 555, 'test'), (2, 'test', 555, '')], 'table_properties': [], 'targets': [], 'waybills': []}}
    crdt.merge(d)
    crdt.delete(("test3", "customers", 2))
    print("Vanlig updated: ", dbquery(crdt.myvehicleid, crdt.myvehicleid))
    result = crdt.getstate()
    result['test3']['customers'] -= 2
    crdt.merge(crdt.query(result))
    print("End: ", crdt.query(result))





def receive():
    pass


def send():
    pass

main()

