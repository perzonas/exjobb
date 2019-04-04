import sys
import json

### (action, dict(dict, dict, dict))


class Script:
    hosts = 0



    def run(self, hosts):
        self.hosts = int(hosts)
        self.addmaterials()
        self.addcustomers()


    ### Add a number of materials for all machines
    def addmaterials(self):
        line1 = json.dumps(("insert", {"materials": {"name": "gravel", "date": "17-02-2019", "nameid": 345}}))
        line2 = json.dumps(("insert", {"materials": {"name": "dirt", "date": "28-06-2018", "nameid": 28}}))
        line3 = json.dumps(("insert", {"materials": {"name": "rocks", "date": "17-08-2017", "nameid": 98}}))
        line4 = json.dumps(("insert", {"materials": {"name": "pavement", "date": "19-02-2019", "nameid": 35}}))

        for i in range(1, self.hosts):
            file = open(("localstates/local"+str(i)), "a")
            file.write(line1+"\n")
            file.write(line2+"\n")
            file.write(line3+"\n")
            file.write(line4+"\n")
            file.close()


    ### Add a number of customers to all machines
    def addcustomers(self):
        line1 = json.dumps(("insert", {"customers": {"name": "ericsson", "nameid": 22, "contact": "Fredrik Johansson",
                                                    "phone": "+46727898767",  "date": "12-02-2012", "misc": "hate ericsson"}}))
        line2 = json.dumps(("insert", {"customers": {"name": "cpac", "nameid": 25, "contact": "Andre perzon",
                                                    "phone": "+46776898767", "date": "20-01-2012",
                                                    "misc": "good stuff"}}))
        line3 = json.dumps(("insert", {"customers": {"name": "apotekarnes", "nameid": 2, "contact": "Linus Johansson",
                                                    "phone": "+46727898111", "date": "12-02-2015",
                                                    "misc": "bananas"}}))
        line4 = json.dumps(("insert", {"customers": {"name": "dtek", "nameid": 12, "contact": "Elias Forsberg",
                                                    "phone": "+46727823456", "date": "12-10-2007",
                                                    "misc": "hate ericsson"}}))
        line5 = json.dumps(("insert", {"customers": {"name": "", "nameid": 22, "contact": "Fredrik Johansson",
                                                    "phone": "+46727898767", "date": "12-02-2012",
                                                    "misc": "hate ericsson"}}))
        for i in range(1, self.hosts):
            file = open(("localstates/local"+str(i)), "a")
            file.write(line1+"\n")
            file.write(line2+"\n")
            file.write(line3+"\n")
            file.write(line4+"\n")
            file.write(line5+"\n")
            file.close()






if __name__ == '__main__':

    script = Script()
    script.run(sys.argv[1])
