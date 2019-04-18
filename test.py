import os
import sys
import glob


class Test:


    def run(self, hosts=2):
        hosts = int(hosts)
        ###  Clean up from last test ###

        ###  Clean up local states  ###
        files = glob.glob("localstates/*")
        for file in files:
            os.remove(file)
            print("File removed: ", file)

        ###  Clean up databases  ###
        for i in range(1, (hosts+1)):
            files = glob.glob("databases/"+str(i)+"/*")
            for file in files:
                os.remove(file)
                print("File removed: ", file)



if __name__ == '__main__':

    test = Test()
    try:
        test.run(sys.argv[1])
    except IndexError as e:
        print("Too few arguments")
