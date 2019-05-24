import sys
import time
import socket
from threading import Thread
import json
from queue import Queue
from StateCvRDT import *
import os.path
import math


class Server:
    crdt = StateCvRDT()
    mergeStack = Queue()
    test = "127.0.0.1"
    ip = "20.1.90."
    port = 1337
    ownIP = "20.1.90."
    hostID = 0
    numberofhost = 0
    logicalclock = 0
    bytessent = 0
    expectedbytes = 0
    bytessentadress = ""
    mergetime = []
    messagetime = []
    dropped_msgs = 0
    messagesize = []

    def run(self, hostnumber, numberofhosts=1):
        self.numberofhost = int(numberofhosts)
        self.ownIP += str(hostnumber)
        self.hostID = hostnumber
        self.crdt.myvehicleid = hostnumber
        self.bytessentadress = "testdata/bytes" + self.hostID


        # AF_INET -> ipv4 and SOCK_STREAM -> tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # a thread that broadcast it's own state to all other nodes in a predefined intervall intervall
        thread = Thread(target=self.broadcaststates)
        thread.daemon = True
        thread.start()

        # A thread that looks at changes done by the local machine and performs all the actions on the CRDT
        thread = Thread(target=self.localthread)
        thread.daemon = True
        thread.start()

        print("Starting server")
        sock.bind((self.ownIP, self.port))
        (ip, po) = sock.getsockname()
        print("Started server at %s" % ip)

        print("Listening for connections on port: %d" % self.port)
        sock.listen(5)
        while True:
            # someone connected to the socket
            try:
                connection, connectioninfo = sock.accept()
                print("CONNECTION ESTABLISHED WITH: ", connectioninfo)

                # Creates a thread for each connection
                thread = Thread(target=self.handleconnection, args=[connection, connectioninfo])
                thread.daemon = True
                thread.start()
            except Exception as exception:
                print("Exception when creating thread.")
                print(exception)


    # handling incoming connection
    def handleconnection(self, connection, connectinfo):
        start_time = time.time()
        ip, port = connectinfo
        id = ip.split('.')[-1]
        data = ""
        receivedmessage = False

        while True:
            byte = connection.recv(1)
            byte = byte.decode()
            if byte == ";":
                receivedmessage = True
                break
            elif byte:
                data += byte
            else:
                break

        if receivedmessage:
            end_time = time.time()
            total_time = end_time - start_time
            self.messagetime.append(total_time*1000)
            message = json.loads(data)
            ### Add state to TODO stack so worker thread can perform the received action ###
            self.mergeStack.put(message)
        else:
            self.dropped_msgs += 1
        self.writeMessage()




    # Broadcast nodes current state
    def broadcaststates(self):
        # sleep before starting to broadcast
        time.sleep(2)

        # get state from crdt
        while True:
            state = self.crdt.query()
            self.broadcaststate(state)
            time.sleep(5)

    # Broadcast a message to all other nodes
    def broadcaststate(self, message):
        for host in range(1, (self.numberofhost + 1)):
            host = str(host)
            host = self.ip + host

            # do not send to ourselves
            if host != self.ownIP:
                thread = Thread(target=self.sendmessage, args=[message, host, self.port])
                thread.daemon = True
                thread.start()
                #self.sendmessage(message, host, self.port)

    # sending message to another host
    def sendmessage(self, message, host, port):

        try:
            serializeddata = json.dumps(message)
        except (TypeError, ValueError) as e:
            raise Exception("Not Json")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            data = (serializeddata+";").encode()
            datasize = len(data)
            print("DATASIZE IS: ",datasize)
            self.messagesize.append(datasize)
            self.expectedbytes += datasize
            totalsent = 0
            while totalsent < datasize:
                sent = sock.send(data[totalsent:])
                if sent == 0:
                    print("Connection broken closing socket")
                    break
                totalsent += sent
            sock.close()
            self.bytessent += totalsent
            self.writeBytes()






        except Exception as e:
            "Fail during socket connection"


    def localthread(self):
        filename = "localstates/local"+self.hostID


        ### Create local update file if it doesn't exist
        if not os.path.isfile(filename):
            file = open(filename, "w+")
            os.chmod(filename, 0o777)
            file.close()
        position = 0

        while True:
            reproduce = []
            action = ""

            ### Read file that holds local updates ###
            file = open(filename, "r")
            text = file.readlines()
            file.close()
            if text:
                for i in range(position, len(text)):
                    try:
                        action = text[i]
                        ### Perform the action from local machine ###
                        state = json.loads(action)
                        data = {str(self.hostID): state[1]}

                        start_time = time.time()
                        print("&&&&&UPDATING DATA &&&&&&&")
                        if state[0] == "i":
                            self.crdt.merge(data)
                        elif state[0] == "u":
                            for table, entry in state[1].items():
                                if entry:
                                    self.crdt.update(table, entry[0])
                        else:
                            for table, entry in state[1].items():
                                if entry:
                                    self.crdt.delete((self.hostID, table, entry[0][0]))
                        end_time = time.time()
                        total_time = end_time - start_time
                        self.mergetime.append((total_time * 1000))
                        self.writeMerge()
                    except:
                        pass
            position = len(text)


            ### Perform actions received from other nodes  and saved in a buffer ###
            if not self.mergeStack.empty():
                state = self.mergeStack.get()
                start_time = time.time()
                self.crdt.merge(state)
                end_time = time.time()
                total_time = end_time - start_time
                self.mergetime.append((total_time * 1000))
                self.mergeStack.task_done()
                self.writeMerge()


    def writeMerge(self):
        ### Write results to testfile ###
        file = open("testdata/mergelatency" + str(self.hostID), "w")
        os.chmod("testdata/mergelatency" + str(self.hostID), 0o777)
        file.write(json.dumps(self.mergetime))
        file.close()

    def writeBytes(self):
        ### Create testdata file if it doesn't exist ###
        file = open(self.bytessentadress, "w")
        os.chmod(self.bytessentadress, 0o777)
        file.write(json.dumps((self.bytessent, self.expectedbytes)))
        file.close()

        file = open("testdata/messagesize" + str(self.hostID), "w")
        os.chmod("testdata/messagesize" + str(self.hostID), 0o777)
        file.write(json.dumps(self.messagesize))
        file.close()

    def writeMessage(self):
        file = open("testdata/messagelatency" + str(self.hostID), "w")
        os.chmod("testdata/messagelatency" + str(self.hostID), 0o777)
        file.write(json.dumps(self.messagetime))
        file.close()

        file = open("testdata/droppedmessages" + str(self.hostID), "w")
        os.chmod("testdata/droppedmessages" + str(self.hostID), 0o777)
        file.write(str(self.dropped_msgs))
        file.close()


    def testing(self):
        server.crdt.crdtbasecheck()


if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Too few arguments")


