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


        # a thread that ask master for update and then receives the update and updates it's own state in a
        # predefined interval
        if int(self.hostID) != 1:
            print("*** starting update thread ***")
            thread = Thread(target=self.updatestate)
            thread.daemon = True
            thread.start()
            print("*** Update thread is running ***")

        # A thread that looks at changes done by the local machine
        print("*** Starting worker thread ***")
        thread = Thread(target=self.localthread)
        thread.daemon = True
        thread.start()
        print("*** Worker thread is running ***")

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
        print("message received: ", message)

        ### Add state to TODO stack so worker thread can perform the received action ###
        if int(self.hostID) != 1:
            self.mergeStack.put(message)
        else:
            ### slave received state from master and should update its own database based on received state
            self.performaction(message)

    def performaction(self, message):
        pass

    def updatestate(self):
        while True:
            time.sleep(10+int(self.hostID))
            message = ("upgrade", {})
            print("*** Asking master for update ***")
            self.sendmessage(message, (self.ip+"1"), 1337)


    # Broadcast a message to all other nodes
    def broadcaststate(self, message):
        print("Broadcasting message to all hosts")
        for host in range(1, (self.numberofhost + 1)):
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
            sock.sendall((serializeddata + ";").encode())
        except Exception as e:
            return False


    def localthread(self):
        filename = "localstates/local"+self.hostID

        ### Create local update file if it doesn't exist
        if not os.path.isfile(filename):
            file = open(filename, "w+")
            os.chmod(filename, 0o777)
            file.close()

        while True:
            reproduce = None
            action = ""

            ### Read file that holds local updates ###
            file = open(filename, "r")
            text = file.readlines()
            file.close()
            if text:
                action = text[0]
                if len(text) > 1:
                    reproduce = text[1:]

                ### Send the update from the local machine to the centralized machine ###
                ### if you are a slave node you send the update to master, if you are master you perform update

                if int(self.hostID) != 1:
                    if self.sendmessage(action, (self.ip+"1"), 1337):
                        self.performaction(action)

            ### Update the file and remove the line that will be performed if there was an update in the file ###

                        file = open(filename, "w")
                        if reproduce:
                            for line in reproduce:
                                file.write(line)
                        else:
                            file.write("")
                        file.close()










            ### Maybe not needed in this topology
            ### Perform actions received from other nodes and saved in a buffer ###
            if int(self.hostID) == 1:
                if not self.mergeStack.empty():
                    state = self.mergeStack.get()
                    self.performaction(state)
                    self.mergeStack.task_done()
            time.sleep(5)






if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[2])
    except (KeyboardInterrupt, IndexError) as e:
        if e == KeyboardInterrupt:
            print("Shutting down server")
        else:
            print("Too few arguments")
