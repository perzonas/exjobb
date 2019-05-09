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
    dropped_msgs = 0

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
            self.dropped_msgs += 1

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
        for i in range(3):
            snapshot = self.crdt.getsnapshot()
            self.broadcastsnapshot(snapshot)
            time.sleep(2)

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
        state = self.crdt.query(task[1])
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

            print("### BYTES SENT: ", self.bytessent)



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
                for action in text:

                    ### Perform the action from local machine ###
                    state = json.loads(action)
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
                                self.crdt.delete(self.hostID, [0, self.hostID, table, entry[0]])
                    end_time = time.time()
                    total_time = end_time - start_time
                    self.mergetime.append((total_time * 1000))



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








if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Too few arguments")

    finally:
        print("\n", server.mergetime)
        inputs = len(server.mergetime)
        sum = sum(server.mergetime)
        if inputs != 0:
            medel = sum / inputs
            print("\n### MEDEL ÄR: %06.4f ###" % medel)
            server.mergetime.sort()

            if inputs % 2 == 0:
                print("\n### MEAN VALUE IS: %06.4f & %06.4f ###" % (
                server.mergetime[int(inputs / 2) - 1], server.mergetime[int(inputs / 2)]))
            else:
                print("\n### MEAN VALUE IS: %06.4f ###" % server.mergetime[math.floor(inputs / 2)])
        print("\n### SAVING RESULTS ###")
        ### Write converge latency to testdatafile ###
        file = open("testdata/mergelatency" + str(server.hostID), "w")
        os.chmod("testdata/mergelatency" + str(server.hostID), 0o777)
        file.write(json.dumps(server.mergetime))
        file.close()

        ### Create testdata file if it doesn't exist
        file = open(server.bytessentadress, "w")
        os.chmod(server.bytessentadress, 0o777)
        file.write(json.dumps((server.bytessent, server.expectedbytes)))
        file.close()

        print("\n### Shutting down server ###")
        time.sleep(2)