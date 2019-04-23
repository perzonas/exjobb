import sys
import time
import socket
from threading import Thread
import json
from queue import Queue
from StateCvRDT import *
from DbConnect import *
import os.path
import sqlite3


class Server:
    mergeStack = Queue()
    test = "127.0.0.1"
    ip = "20.1.90."
    port = 1337
    ownIP = "20.1.90."
    hostID = 0
    numberofhost = 0
    logicalclock = 0
    centralclockholder = {}
    historyQueue = Queue()

    def run(self, hostnumber, numberofhosts=1):
        self.numberofhost = numberofhosts
        self.ownIP += str(hostnumber)
        self.hostID = hostnumber
        for i in range(1, int(numberofhosts)+1):
            self.centralclockholder[i] = 0

        # AF_INET -> ipv4 and SOCK_STREAM -> tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # a thread that ask master for update and then receives the update and updates it's own state in a
        # predefined interval
        if int(self.hostID) == 1:
            print("*** starting broadcast thread ***")
            thread = Thread(target=self.broadcaststate)
            thread.daemon = True
            thread.start()
            print("*** Broadcast thread is running ***")

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
        ip, port = connectinfo
        id = ip[-1]
        data = ""
        receivedMessage = False

        while True:
            byte = connection.recv(1)
            byte = byte.decode()
            if byte == ";":
                receivedMessage = True
                break
            elif byte:
                data += byte
            else:
                break
        message = json.loads(data)

        ### Received entire message, return ack ###
        if receivedMessage:
            connection.send("a".encode())



        connection.close()

    ### Master node have received an updates from slave nodes and perform the action received to update its state
    def performaction(self, id, clock, received):
        (action, content) = json.loads(received)
        if int(clock) > self.centralclockholder[int(id)]:
            self.centralclockholder[int(id)] = clock
            if not dbexistcheck(self.hostID, self.hostID):
                addnewdb(self.hostID, self.hostID)
            ### If the action is insert perform the insert ***
            if action == "i":
                for table, entry in content.items():
                    if entry:
                        dbaddentry(self.hostID, self.hostID, table, entry[0])

        else:
            print("***  Already added to  DB  ***")


    ###  Slave node have received the state from the master node and will update its own state to this state
    def updatestate(self, state):
        print("***  Updating slave state based on master state  ***\n")
        if not dbexistcheck(self.hostID, self.hostID):
            addnewdb(self.hostID, self.hostID)
        for table, tlist in state.items():
            if tlist:
                for entry in tlist:
                    if not slavedbentryexist(self.hostID, self.hostID, table, entry):
                        dbaddentry(self.hostID, self.hostID, table, entry)
        pass

    # Broadcast a message to all other nodes
    def broadcaststate(self):


        while True:

            time.sleep(15)
            message = dbquery(self.hostID, self.hostID)
            print("***  Broadcasting master state: %s  ***\n")
            for host in range(1, (int(self.numberofhost) + 1)):
                host = self.ip + str(host)

                # do not send to ourselves
                if host != self.ownIP:
                    self.sendmessage(message, host, self.port)

    # sending message to another host
    def sendmessage(self, message, host, port):
        received = False

        try:
            serializeddata = json.dumps(message)
        except (TypeError, ValueError) as e:
            raise Exception("Not Json")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.sendall((serializeddata + ";").encode())

            byte = sock.recv(1)
            byte = byte.decode()
            if byte == "a":
                print("*** Received ACK ***")
                received = True

            sock.close()
            return received
        except Exception as e:
            return received


    def localthread(self):
        filename = "localstates/local"+self.hostID
        sendQueue = Queue()
        currentMessage = None

        ### Create local update file if it doesn't exist
        if not os.path.isfile(filename):
            file = open(filename, "w+")
            os.chmod(filename, 0o777)
            file.close()

        while True:
            reproduce = None
            action = None



            ### Read file that holds local updates ###
            file = open(filename, "r")
            text = file.readlines()
            file.close()
            if text:
                action = text[0]
                if len(text) > 1:
                    reproduce = text[1:]


            ### Update the file and remove the line that will be performed if there was an update in the file ###

                file = open(filename, "w")
                if reproduce:
                    for line in reproduce:
                        file.write(line)
                else:
                    file.write("")
                file.close()

            ### Send the update from the local machine to the centralized machine ###
            ### if you are a slave node you send the update to master, if you are master you perform update

            if int(self.hostID) != 1:
                if action:
                    self.logicalclock += 1
                    sendQueue.put((self.logicalclock, action))

                if currentMessage is None and not sendQueue.empty():
                    currentMessage = sendQueue.get()
                if currentMessage is not None:
                    if self.sendmessage(currentMessage, self.ip + "1", 1337):
                        currentMessage = None
                        sendQueue.task_done()


            ### Master node perform actions received from other nodes that are saved in a buffer ###
            else:
                if action:
                    self.logicalclock += 1
                    self.mergeStack.put((self.hostID, (self.logicalclock, action)))
                if not self.mergeStack.empty():
                    (id, (clock, operation)) = self.mergeStack.get()
                    self.performaction(id, clock, operation)
                    self.mergeStack.task_done()






if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[2])
    except (KeyboardInterrupt, IndexError) as e:
        if e == KeyboardInterrupt:
            print("Shutting down server")
        else:
            print("Too few arguments")