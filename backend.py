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

    def run(self, hostnumber, numberofhosts=1):
        self.numberofhost = numberofhosts
        self.ownIP += str(hostnumber)
        self.hostID = hostnumber
        self.crdt.myvehicleid = hostnumber

        # AF_INET -> ipv4 and SOCK_STREAM -> tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # a thread that broadcast it's own state to all other nodes in a predefined intervall intervall
        # thread = Thread(target=self.broadcaststates)
        # thread.daemon = True
        # thread.start()

        # A thread that looks at changes done by the local machine
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
        print("handling connection from ", connectinfo)
        ip, port = connectinfo
        id = ip[-1]
        data = ""

        while True:
            byte = connection.recv(1)
            byte = byte.decode()
            if byte == ";":
                break
            elif byte:
                data += byte
            else:
                break
        message = json.loads(data)
        print(message)

        ### Add state to TODO stack so worker thread can perform the received action ###
        self.mergeStack.put(message)

        ### merge received state with own state ###
        # self.crdt.merge(message)
        # state = self.crdt.getState()
        # self.broadcast(state)


    # Broadcast nodes current state
    def broadcaststates(self):
        # sleep before starting to broadcast
        time.sleep(5)

        # get state from crdt
        for i in range(120):
            state = self.crdt.query()
            self.broadcaststate(state)
            time.sleep(1)

    # Broadcast a message to all other nodes
    def broadcaststate(self, message):
        print("Broadcasting message to all hosts")
        for host in range(1, (self.numberofhost + 1)):
            host = self.ip + host

            # do not send to ourselves
            if host != self.ownIP:
                self.sendmessage(message, host, self.port)

    # sending message to another host
    def sendmessage(self, message, host, port, connection):

        try:
            serializeddata = json.dumps(message)
        except (TypeError, ValueError) as e:
            raise Exception("Not Json")

        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(host, port)
        # sock.connect((host, port))

        connection.sendall((serializeddata + ";").encode())


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
                self.performaction(state)


            ### Perform actions received from other nodes  and saved in a buffer ###
            if not self.mergeStack.empty():
                state = self.mergeStack.get()
                self.performaction(state)
                self.mergeStack.task_done()

    def performaction(self, state):
        self.crdt.merge(state)




if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[1])
    except KeyboardInterrupt:
        print("Shutting down server")
