import sys
import time
import socket
from threading import Thread
import json
from queue import Queue
from StateCvRDT import *
import os.path


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
    bytessentadress = ""

    def run(self, hostnumber, numberofhosts=1):
        self.numberofhost = int(numberofhosts)
        self.ownIP += str(hostnumber)
        self.hostID = hostnumber
        self.crdt.myvehicleid = hostnumber
        self.bytessentadress = "testdata/bytes" + self.hostID

        ### Create testdata file if it doesn't exist
        if not os.path.isfile(self.bytessentadress):
            file = open(self.bytessentadress, "w+")
            os.chmod(self.bytessentadress, 0o777)
            file.close()

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
                print("Connection established with", connectioninfo)

                # Creates a thread for each connection
                thread = Thread(target=self.handleconnection, args=[connection, connectioninfo])
                thread.daemon = True
                thread.start()
            except Exception as exception:
                print("Exception when creating thread.")
                print(exception)


    # handling incoming connection
    def handleconnection(self, connection, connectinfo):
        ip, port = connectinfo
        id = ip[-1]
        data = ""
        recievedmessage = False

        while True:
            byte = connection.recv(1)
            byte = byte.decode()
            if byte == ";":
                recievedmessage = True
                break
            elif byte:
                data += byte
            else:
                break

        if recievedmessage:
            message = json.loads(data)
            print("### RECEIVED MESSAGE FROM NODE %s ###" % id)

            ### Add state to TODO stack so worker thread can perform the received action ###
            self.mergeStack.put(message)

        ### merge received state with own state ###
        # self.crdt.merge(message)
        # state = self.crdt.getState()
        # self.broadcast(state)


    # Broadcast nodes current state
    def broadcaststates(self):
        # sleep before starting to broadcast
        time.sleep(2)

        # get state from crdt
        for i in range(3):
            state = self.crdt.query()
            self.broadcaststate(state)
            time.sleep(2)

    # Broadcast a message to all other nodes
    def broadcaststate(self, message):
        print("Broadcasting message to all hosts")
        for host in range(1, (self.numberofhost + 1)):
            host = str(host)
            host = self.ip + host

            # do not send to ourselves
            if host != self.ownIP:
                self.sendmessage(message, host, self.port)

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
            ### Write bytes sent to testdatafile ###
            file = open(self.bytessentadress, "w")
            file.write(str(self.bytessent))
            file.close()


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
            reproduce = []
            action = ""



            ### Read file that holds local updates ###
            file = open(filename, "r")
            text = file.readlines()
            file.close()
            if text:
                action = text[0]
                if len(text) > 1:
                    reproduce = text[1:]
                else:
                    reproduce = ""

                ### Update the file and remove the line that will be performed if there was an update in the file ###

                file = open(filename, "w")
                if reproduce:
                    for line in reproduce:
                        file.write(line)
                else:
                    file.write("")
                file.close()

                ### Perform the action from local machine ###
                state = json.loads(action)
                data = {str(self.hostID): state[1]}
                print("#### PERFORMING AN UPDATE ####")
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



            ### Perform actions received from other nodes  and saved in a buffer ###
            if not self.mergeStack.empty():
                print("#### PERFORMING A MERGE ####")
                state = self.mergeStack.get()
                self.crdt.merge(state)
                self.mergeStack.task_done()








if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[2])
    except KeyboardInterrupt:
        print("\n###  Shutting down server  ###")
        time.sleep(2)
