import sys
import json
import time

### (action, dict(dict, dict, dict))


class Script:
    hosts = 0



    def run(self, hosts=2):
        '''
        self.hosts = int(hosts)
        self.addmaterials()
        self.addcustomers()
        time.sleep(1)
        if self.hosts > 2:
            self.addtargets(3)
        else:
            self.addtargets(2)
        '''
        self.addcustomers()
        self.addworkorders()
        self.updateCustomers()
        return 1



    ### Add a number of materials to machine 1
    def addmaterials(self):
        line1 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
                                      'materials': [(1, 'gravel', 1554371143, '345')], 'table_properties': [],
                                      'targets': [], 'waybills': []}))
        line2 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
                                      'materials': [(3, 'dirt', 1522921530, '98')], 'table_properties': [],
                                      'targets': [], 'waybills': []}))
        line3 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
                                      'materials': [(4, 'rocks', 1543980836, '66')], 'table_properties': [],
                                      'targets': [], 'waybills': []}))
        line4 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
                                      'materials': [(5, 'pavement', 1414985403, '35')], 'table_properties': [],
                                      'targets': [], 'waybills': []}))


        file = open("localstates/local1", "a")
        file.write(line1+"\n")
        file.write(line2+"\n")
        file.write(line3+"\n")
        file.write(line4+"\n")
        file.close()


    ### Add a number of customers to machine 2
    def addcustomers(self):
        line1 = json.dumps(('i', {'customers': [(0, "ericsson", 22, "Fredrik Johansson", "+46727898767",  15432121836,
                            "hate ericsson")], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [], 'waybills': []}))

        line2 = json.dumps(('i', {'customers': [(0, "cpac", 25, "Andre Perzon", "+46776898767", 1540836, "good stuff")],
                                  'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [], 'table_properties': [],
                                  'targets': [], 'waybills': []}))

        line3 = json.dumps(('i', {'customers': [(0, "apotekarnes", 2, "Linus Johansson", "+46727898111", 154532236,
                                    "bananas")], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [], 'waybills': []}))

        line4 = json.dumps(('i', {'customers': [(0, "dtek", 12, "Elias Forsberg", "+46727823456", 1543980836,
                                 "hate ericsson")], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [], 'waybills': []}))

        line5 = json.dumps(('i', {'customers': [(0, "chalmers", 22, "Fredrik Johansson", "+46727898767", 1543790836,
                                 "hate ericsson")], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [], 'waybills': []}))

        file = open("localstates/local2", "a")
        file.write(line1+"\n")
        file.write(line2+"\n")
        file.write(line3+"\n")
        file.write(line4+"\n")
        file.write(line5+"\n")
        file.close()

    def addtargets(self, number):
        line1 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [(0, 0, "Pappa noden", 30000, 1543984526,
                                   "hate ericsson")], 'waybills': []}))

        line2 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [(0, 1, "elaka styvdottern", 3000, 15439123836,
                                                                       "hate ericsson")], 'waybills': []}))

        line3 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [(0, 0, "favorit sonen", 130000, 1586980836,
                                                                       "hate ericsson")], 'waybills': []}))

        file = open(("localstates/local" + str(number)), "a")
        file.write(line1 + "\n")
        file.write(line2 + "\n")
        file.write(line3 + "\n")

    def addworkorders(self):
        line1 = json.dumps(('i', {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [], 'targets': [], 'waybills': [], 'work_orders': [(0, "krashar",
                                  2222222, 30000, "misc", "duetime", 1543984526, 1543999526, 20)]}))

        file = open(("localstates/local" + str(2)), "a")
        file.write(line1 + "\n")

    def updateCustomers(self):
        line1 = json.dumps(('u', {'customers': [(1, "ericssonsuger", 22, "Fredrik Johansson", "+46727898767", 15432121836,
                                                 "hate ericsson")], 'heaps': [], 'loads': [], 'loads_waybills': [],
                                  'materials': [],
                                  'table_properties': [], 'targets': [], 'waybills': []}))
        line2 = json.dumps(('u', {'customers': [(2, "cpacisgut", 25, "Andre Perzon", "+46776898767", 1540836, "good stuff")],
                                  'heaps': [], 'loads': [], 'loads_waybills': [], 'materials': [],
                                  'table_properties': [],
                                  'targets': [], 'waybills': []}))

        file = open("localstates/local2", "a")
        file.write(line1 + "\n")
        file.write(line2 + "\n")


if __name__ == '__main__':

    script = Script()
    script.run(sys.argv[1])
