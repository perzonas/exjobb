import os
import sys
import glob
from LocalStateScript import Script
import shutil


class Test:


    def run(self, hosts=8):
        hosts = int(hosts)
        ###  Clean up from last test ###

        ###  Clean up local states  ###
        files = glob.glob("localstates/*")
        for file in files:
            os.remove(file)
            print("File removed: ", file)



        files = glob.glob("testdata/*")
        for file in files:
            if file != "testdata/information.txt":
                os.remove(file)
                print("File removed: ", file)


        ###  Clean up databases  ###
        directories = os.listdir("databases/")
        for id in directories:
            shutil.rmtree("databases/" + id)
            print("File removed: ", id)
            #files = glob.glob("databases/"+str(id)+"/*")
            #for file in files:
            #    os.remove(file)


        script = Script()
        script.run(hosts)


if __name__ == '__main__':

    test = Test()
    try:
        test.run(sys.argv[1])
    except IndexError as e:
        print("Too few arguments")
