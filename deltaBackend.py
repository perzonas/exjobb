import sys
import time
import socket
from threading import Thread
import json
from queue import Queue
from StateCvRDT import *
from DeltaCvRDT import *
import os.path
import math


class Server:
    crdt = DeltaCvRDT()
    taskStack = Queue()
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
    dropped_messages = 0

    def run(self, hostnumber, numberofhosts=1):
        self.numberofhost = int(numberofhosts)
        self.ownIP += str(hostnumber)
        self.hostID = hostnumber
        self.crdt.myvehicleid = hostnumber
        self.bytessentadress = "testdata/bytes" + self.hostID


        # AF_INET -> ipv4 and SOCK_STREAM -> tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # a thread that broadcast it's own snapshot to all other nodes in a predefined intervall
        thread = Thread(target=self.broadcastsnapshots)
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
                print("Connection established with", connectioninfo)

                # Creates a thread for each connection
                thread = Thread(target=self.handleconnection, args=[connection, connectioninfo])
                thread.daemon = True
                thread.start()
            except Exception as exception:
                print("Exception when creating thread.", exception)


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
            print("### RECEIVED MESSAGE FROM NODE %s ###" % id)

            ### Add state to TODO stack so worker thread can perform the received action ###
            self.taskStack.put(message)

        else:
            self.dropped_messages += 1

        self.writeMessage()

        connection.close()
        ### merge received state with own state ###
        # self.crdt.merge(message)
        # state = self.crdt.getState()
        # self.broadcast(state)


    # Broadcast nodes current state
    def broadcastsnapshots(self):
        # sleep before starting to broadcast
        time.sleep(2)

        # get state from crdt
        for i in range(10):
            snapshot = self.crdt.getsnapshot()
            self.broadcastsnapshot(snapshot)
            time.sleep(4)

    # Broadcast a message to all other nodes
    def broadcastsnapshot(self, message):
        print("Broadcasting SNAPSHOT to all hosts")
        for host in range(1, (self.numberofhost + 1)):
            host = str(host)
            host = self.ip + host

            ms = [self.hostID, message]

            # do not send to ourselves
            if host != self.ownIP:
                self.sendmessage(ms, host, self.port)
    
    def snapreply(self, task):
        host = str(task[0])
        host = self.ip + host
        print("Sending a snapreply to : ", host)
        print(" ")
        print("TASK: ", task[1])
        print(" ")
        state = self.crdt.query(task[1])
        print("STATE: ", state)
        print(" ")
        if not len(state) == 0:
            self.sendmessage(state, host, self.port)

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


        while True:
            ### Read file that holds local updates ###
            file = open(filename, "r")
            text = file.readlines()
            file.close()
            file = open(filename, "w")
            file.write("")
            file.close()
            if text:
                #print("TEXT: ", text)
                for action in text:

                    ### Perform the action from local machine ###
                    try:
                        state = json.loads(action)
                    except:
                        print("-----------------------------------------")
                        print("deltaBackend: json.loads(action)  ACTION: ", action, " TEXT: ", text)
                        print(" ")
                        print()
                        print("-----------------------------------------")
                    data = {str(self.hostID): state[1]}
                    print("#### PERFORMING AN UPDATE ####")
                    start_time = time.time()
                    if state[0] == "i":
                        self.crdt.merge(data)
                    elif state[0] == "u":
                        for table, entry in state[1].items():
                            if entry:
                                self.crdt.update(table, entry[0])
                    else:
                        for table, entry in state[1].items():
                            if entry:
                                self.crdt.delete(self.hostID, table, entry[0][0])
                    end_time = time.time()
                    total_time = end_time - start_time
                    self.mergetime.append((total_time * 1000))

                    self.writeMerge()



            ### Perform actions received from other nodes  and saved in a buffer ###
            if not self.taskStack.empty():
                task = self.taskStack.get()

                if len(task) == 2:
                    print("#### PERFORMING A SNAPREPLY ####")
                    self.snapreply(task)
                    self.taskStack.task_done()
                else:
                    print("#### PERFORMING A MERGE ####")
                    start_time = time.time()
                    self.crdt.merge(task)
                    end_time = time.time()
                    total_time = end_time - start_time
                    self.mergetime.append((total_time * 1000))
                    self.taskStack.task_done()

                    self.writeMerge()

    def writeMerge(self):
        ### Write results to testfile ###
        file = open("testdata/mergelatency" + str(self.hostID), "w")
        os.chmod("testdata/mergelatency" + str(self.hostID), 0o777)
        file.write(json.dumps(self.mergetime))
        file.close()

    def writeBytes(self):
        ### Create testdata file if it doesn't exist ###
        file = open("testdata/bytes" + str(self.hostID), "w")
        os.chmod("testdata/bytes" + str(self.hostID), 0o777)
        file.write(json.dumps((self.bytessent, self.expectedBytes)))
        file.close()

    def writeMessage(self):
        file = open("testdata/messagelatency" + str(self.hostID), "w")
        os.chmod("testdata/messagelatency" + str(self.hostID), 0o777)
        file.write(json.dumps((self.dropped_messages, self.messagetime)))
        file.close()







if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Too few arguments")


