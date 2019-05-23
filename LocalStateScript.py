import sys
import json
import time

### (action, dict(dict, dict, dict))


class Script:
    hosts = 0
    target_counter = 0
    customer_counter = 0
    materials_counter = 0
    waybills_counter = 0
    heaps_counter = 0
    workorder_counter = 0
    loads_counter = 0
    loadswaybills_counter = 0
    startTime = 0



    def run(self, hosts=2):
        time.sleep(5)
        self.startTime = time.time()
        ### Write 5 inserts to all nodes as test starts ###
        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.getCustomers()))
            time.sleep(50/(5*hosts))
            file.write(self.makeLine(self.getMaterial()))
            time.sleep(50 / (5 * hosts))
            file.write(self.makeLine(self.getTargets()))
            time.sleep(50/(5*hosts))
            file.write(self.makeLine(self.getWorkorders()))
            time.sleep(50/(5*hosts))
            file.write(self.makeLine(self.getLoads()))
            time.sleep(50/(5*hosts))
            file.close()



        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.getCustomers()))
            time.sleep(45 / (5 * hosts))
            file.write(self.makeLine(self.getMaterial()))
            file.write(self.makeLine(self.getTargets()))
            time.sleep(45 / (5 * hosts))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            time.sleep(45 / (5 * hosts))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getWaybills()))
            time.sleep(45 / (5 * hosts))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            time.sleep(45 / (5 * hosts))
            file.close()

        for i in range(1, hosts + 1):
            file = open("localstates/local" + str(i), "a")
            file.write(self.makeLine(self.getCustomers()))
            time.sleep(40 / (2 * hosts))
            file.write(self.makeLine(self.getMaterial()))
            time.sleep(40 / (2 * hosts))
            file.write(self.makeLine(self.getTargets()))
            file.close()


        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.updCustomers()))
            time.sleep(35 / (2 * hosts))
            file.write(self.makeLine(self.updMaterial()))
            time.sleep(35 / (2 * hosts))
            file.write(self.makeLine(self.updTargets()))
            file.close()


        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.delLoads()))
            file.close()

        time.sleep(30)

        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.getLoadsWaybills()))
            file.write(self.makeLine(self.getLoads()))
            time.sleep(25 / (5 * hosts))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            time.sleep(25 / (5 * hosts))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getWaybills()))
            time.sleep(25 / (5 * hosts))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getTargets()))
            time.sleep(25 / (5 * hosts))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            time.sleep(25 / (5 * hosts))
            file.close()

        for i in range(1, hosts + 1):
            file = open("localstates/local" + str(i), "a")
            file.write(self.makeLine(self.getLoads()))
            time.sleep(20 / (2 * hosts))
            file.write(self.makeLine(self.getWorkorders()))
            time.sleep(20 / (2 * hosts))
            file.write(self.makeLine(self.getTargets()))
            file.close()

        for i in range(1, hosts + 1):
            file = open("localstates/local" + str(i), "a")
            file.write(self.makeLine(self.delLoads()))
            time.sleep(15 / (5 * hosts))
            file.write(self.makeLine(self.delMaterial()))
            time.sleep(15 / (5 * hosts))
            file.write(self.makeLine(self.delTargets()))
            time.sleep(15 / (5 * hosts))
            file.write(self.makeLine(self.delWaybills()))
            time.sleep(15 / (5 * hosts))
            file.write(self.makeLine(self.delWorkorders()))
            time.sleep(15 / (5 * hosts))
            file.close()




        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.getLoadsWaybills()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            time.sleep(10 / (hosts))
            file.write(self.makeLine(self.getLoadsWaybills()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            file.close()


        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.getLoadsWaybills()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getWaybills()))
            file.write(self.makeLine(self.getTargets()))
            file.write(self.makeLine(self.getWorkorders()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getLoadsWaybills()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getLoads()))
            file.write(self.makeLine(self.getTargets()))
            file.close()

        time.sleep(5)

        for i in range(1, hosts+1):
            file = open("localstates/local"+str(i), "a")
            file.write(self.makeLine(self.updCustomers()))
            file.write(self.makeLine(self.updMaterial()))
            file.write(self.makeLine(self.updTargets()))
            file.write(self.makeLine(self.updLoads()))
            file.write(self.makeLine(self.updLoadsWaybills()))
            file.close()










    def makeLine(self, tuple):
        line = json.dumps(tuple)
        return line+"\n"

    ### Returns a tuple containing the insert action and the dict to be inserted ###
    def getMaterial(self):
        self.materials_counter += 1
        return ('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
         'materials': [(1, 'material'+str(self.materials_counter), time.time(), str(self.materials_counter))], 'table_properties': [],
         'targets': [], 'work_orders': [], 'waybills': []})
    def getTargets(self):
        self.target_counter+=1
        return ('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
               'table_properties': [], 'targets': [(0, self.target_counter-1, "Target"+str(self.target_counter),
                self.target_counter*20, time.time(), "misc"+str(self.target_counter))], 'work_orders': [], 'waybills': []})
    def getCustomers(self):
        self.customer_counter+=1
        return ('i', {'customers': [(0, "Customer"+str(self.customer_counter), self.customer_counter, "Firstname"+
                   str(self.customer_counter), "Number"+str(self.customer_counter),  time.time(),
                            "misc")], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                              'table_properties': [], 'targets': [], 'work_orders': [], 'waybills': []})
    def getWaybills(self):
        self.waybills_counter += 1
        return ('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
              'table_properties': [], 'targets': [], 'waybills': [(0, time.time(), "Supplier"+str(self.waybills_counter)
               , "Customer"+str(self.waybills_counter), "Workorder"+str(self.waybills_counter), "Target" +
               str(self.waybills_counter), "Freetext", "Chepstow", "Operator"+str(self.waybills_counter % 13),
                self.waybills_counter)], 'work_orders': []})
    def getWorkorders(self):
        self.workorder_counter += 1
        return ('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'work_orders': [(0,
            "Name"+str(self.workorder_counter), self.customer_counter-2, self.workorder_counter*100, "misc",
            time.time()+100, time.time(), time.time()+50, self.workorder_counter*97)], 'materials': [],
              'table_properties': [], 'targets': [], 'waybills': []})
    def getHeaps(self):
        self.heaps_counter += 1
        return ('i', {'customers': [], 'heaps': [(0, self.workorder_counter-2, self.target_counter-1, time.time(),
                time.time()+65, self.heaps_counter*200)], 'loads': [], 'loads_waybills': [], 'work_orders': [],
                'materials': [], 'table_properties': [], 'targets': [], 'waybills': []})
    def getLoads(self):
        self.loads_counter += 1
        return ('i', {'customers': [], 'heaps': [], 'loads': [(0, self.loads_counter*300, time.time(), self.loads_counter%20,
                 self.loads_counter*50, self.loads_counter % 4, self.heaps_counter-1, self.materials_counter-3)],
                'loads_waybills': [], 'work_orders': [], 'materials': [], 'table_properties': [], 'targets': [],
                'waybills': []})
    def getLoadsWaybills(self):
        self.loadswaybills_counter += 1
        return ('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [(0, self.loads_counter-2,
               self.waybills_counter-1)], 'work_orders': [], 'materials': [], 'table_properties': [], 'targets': [],
               'waybills': []})

    ### Returns a tuple containing the delete action and the dict to be deleted ###
    def delCustomers(self):
        return ('d', {'customers': [(self.customer_counter-2, "Customer" + str(self.customer_counter),
             self.customer_counter, "Firstname" + str(self.customer_counter), "Number" + str(self.customer_counter),
             time.time(), "misc")], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                      'table_properties': [], 'targets': [], 'work_orders': [], 'waybills': []})
    def delMaterial(self):
        return ('d', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
                      'materials': [
                          (self.materials_counter-2, 'material' + str(self.materials_counter), time.time(), str(self.materials_counter))],
                      'table_properties': [],
                      'targets': [], 'work_orders': [], 'waybills': []})
    def delTargets(self):
        return ('d', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
              'table_properties': [], 'targets': [(self.target_counter-2, self.target_counter - 1, "Target" +
               str(self.target_counter), self.target_counter * 20, time.time(), "misc" + str(self.target_counter))],
              'work_orders': [], 'waybills': []})
    def delWaybills(self):
        return ('d', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [(0, time.time(), "Supplier" +
                str(self.waybills_counter), "Customer" + str(self.waybills_counter), "Workorder" + str(self.waybills_counter),
                 "Target" + str(self.waybills_counter), "Freetext", "Chepstow","Operator" + str(self.waybills_counter % 13),
                 self.waybills_counter)], 'materials': [], 'table_properties': [], 'targets': [], 'waybills': [], 'work_orders': []})
    def delWorkorders(self):
        return ('d', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'work_orders':
            [(self.workorder_counter-2, self.customer_counter - 2, self.workorder_counter * 100, "misc", time.time() + 100, time.time(),
              time.time() + 50, self.workorder_counter * 97)], 'materials': [], 'table_properties': [], 'targets': [],
                  'waybills': []})
    def delHeaps(self):
        return ('d', {'customers': [], 'heaps': [(self.heaps_counter-1, self.workorder_counter - 2, self.target_counter - 1, time.time(),
                  time.time() + 65, self.heaps_counter * 200)], 'loads': [], 'loads_waybills': [], 'work_orders': [],
                      'materials': [], 'table_properties': [], 'targets': [], 'waybills': []})
    def delLoads(self):
        return ('d', {'customers': [], 'heaps': [], 'loads': [(self.loads_counter-1, self.loads_counter * 300,
               time.time(), self.loads_counter % 20, self.loads_counter * 50, self.loads_counter % 4, self.heaps_counter
               - 1, self.materials_counter - 3)],'loads_waybills': [], 'work_orders': [], 'materials': [],
                  'table_properties': [], 'targets': [], 'waybills': []})
    def delLoadsWaybills(self):
        return ('d', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [(self.loadswaybills_counter-1,
            self.loads_counter - 2, self.waybills_counter - 1)],'work_orders': [], 'materials': [], 'table_properties':
            [], 'targets': [], 'waybills': []})

    ### Returns a tuple containing the update action and the dict to be updated ###
    def updCustomers(self):
        self.customer_counter += 1
        return ('u', {'customers': [(self.customer_counter-3, "Customer" + str(self.customer_counter),
             self.customer_counter, "Firstname" + str(self.customer_counter), "Number" + str(self.customer_counter),
             time.time(), "misc")], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                      'table_properties': [], 'targets': [], 'work_orders': [], 'waybills': []})
    def updMaterial(self):
        self.materials_counter += 1
        return ('u', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
                      'materials': [
                          (self.materials_counter-2, 'material' + str(self.materials_counter), time.time(), str(self.materials_counter))],
                      'table_properties': [],
                      'targets': [], 'work_orders': [], 'waybills': []})
    def updTargets(self):
        self.target_counter += 1
        return ('u', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
              'table_properties': [], 'targets': [(self.target_counter-2, self.target_counter - 1, "Target" +
               str(self.target_counter), self.target_counter * 20, time.time(), "misc" + str(self.target_counter))],
              'work_orders': [], 'waybills': []})
    def updWaybills(self):
        self.waybills_counter += 1
        return ('u', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [(0, time.time(), "Supplier" +
                str(self.waybills_counter), "Customer" + str(self.waybills_counter), "Workorder" + str(self.waybills_counter),
                 "Target" + str(self.waybills_counter), "Freetext", "Chepstow","Operator" + str(self.waybills_counter % 13),
                 self.waybills_counter)], 'materials': [], 'table_properties': [], 'targets': [], 'waybills': [], 'work_orders': []})
    def updWorkorders(self):
        self.workorder_counter += 1
        return ('u', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'work_orders':
            [(self.workorder_counter-2, self.customer_counter - 2, self.workorder_counter * 100, "misc", time.time() + 100, time.time(),
              time.time() + 50, self.workorder_counter * 97)], 'materials': [], 'table_properties': [], 'targets': [],
                  'waybills': []})
    def updHeaps(self):
        self.heaps_counter += 1
        return ('u', {'customers': [], 'heaps': [(self.heaps_counter-1, self.workorder_counter - 2, self.target_counter - 1, time.time(),
                  time.time() + 65, self.heaps_counter * 200)], 'loads': [], 'loads_waybills': [], 'work_orders': [],
                      'materials': [], 'table_properties': [], 'targets': [], 'waybills': []})
    def updLoads(self):
        self.loads_counter += 1
        return ('u', {'customers': [], 'heaps': [], 'loads': [(self.loads_counter-1, self.loads_counter * 300,
               time.time(), self.loads_counter % 20, self.loads_counter * 50, self.loads_counter % 4, self.heaps_counter - 1,
                 self.materials_counter - 3)],'loads_waybills': [], 'work_orders': [], 'materials': [], 'table_properties': [], 'targets': [],
                  'waybills': []})
    def updLoadsWaybills(self):
        self.loadswaybills_counter += 1
        return ('u', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [(self.loadswaybills_counter-1,
            self.loads_counter - 2, self.waybills_counter - 1)],'work_orders': [], 'materials': [], 'table_properties':
            [], 'targets': [], 'waybills': []})



if __name__ == '__main__':

    script = Script()
    script.run(sys.argv[1])
