from StateCvRDT import *
from DeltaCvRDT import *


def main():
    crdt = DeltaCvRDT()
    crdt.myvehicleid = 'test3'
    crdt.dbases.append("test5")
    print("Vanlig: ", dbquery(crdt.myvehicleid, crdt.myvehicleid))
    print("Vanlig: ", dbquery(crdt.myvehicleid, "test5"))
    d = {'test3': {'graveyard': [], 'customers': [(1, 'six', '66', 'sectiosex', 'sixtys', 60, 'saxtio'),
                                                  (2, 'i', '8765', 'x', 's', 41, 'o'),
                                                  (3, 'a', '8768', 'a', 'a', 11, 'a'),
                                                  (4, 'g', '768', 'g', 'g', 31, 'g')], 'heaps': [], 'loads': [],
                   'loads_waybills': [], 'materials': [(1, '', 555, 'test'), (2, 'test', 555, '')],
                   'table_properties': [], 'targets': [], 'waybills': []}}
    a = {'test5': {'graveyard': [], 'customers': [(1, 'fff', '46', 'secasdtix', 'sisd', 30, 'sahuio'),
                                                  (2, 'e', '865', 'e', 'e', 51, 'e'),
                                                  (3, 'h', '88', 'd', 'd', 121, 'd')], 'heaps': [], 'loads': [],
                   'loads_waybills': [], 'materials': [(1, '', 555, 'test'), (2, 'test', 555, '')],
                   'table_properties': [], 'targets': [], 'waybills': []}}
    #crdt.merge(d)
    print("------------------------------------------------------------------")
    crdt.merge(a)
    crdt.delete(("test3", "customers", 1))
    crdt.delete(("test3", "customers", 2))
    #crdt.delete(("test3", "customers", 3))
    #crdt.delete(("test3", "customers", 4))
    print("Vanlig updated test3: ", dbquery(crdt.myvehicleid, crdt.myvehicleid))
    print("Vanlig updated test5: ", dbquery(crdt.myvehicleid, "test5"))
    result = crdt.getstate()
    #print("RESULT: ", result)
    result['test3']['customers'] = 0
    result['test5']['customers'] = 0
    print("End: ", crdt.query(result))





def receive():
    pass


def send():
    pass

main()

