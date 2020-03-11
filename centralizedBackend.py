import sys
import signal
import time
import socket
from threading import Thread
import json
from queue import Queue
from StateCvRDT import *
from DbConnect import *
import os.path
import sqlite3
import math


class Server:
    mergeStack = Queue()
    ip = "20.1.90."
    port = 1337
    ownIP = "20.1.90."
    hostID = 0
    numberofhost = 0
    logicalclock = 0
    centralclockholder = {}
    bytessent = 0
    bytessentadress = ""
    mergetime = []
    messagetime = []
    dropped_messages = 0
    expectedBytes = 0
    messageSizes = []
    domatrix = 0
    msgcounter = 1
    msglist = []



    def run(self, hostnumber, numberofhosts=1, domatrix = 0):

        self.numberofhost = numberofhosts
        self.ownIP += str(hostnumber)
        self.hostID = hostnumber
        for i in range(1, int(numberofhosts)+1):
            self.centralclockholder[i] = 0
        self.bytessentadress = "testdata/bytes" + str(self.hostID)
        self.domatrix = int(domatrix)




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


        print("IP IS: ", self.ownIP)
        time.sleep(5)
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
        start_time = time.time()
        ip, port = connectinfo
        id = ip.split('.')[-1]
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

        if receivedMessage:
            end_time = time.time()
            total_time = end_time-start_time
            self.messagetime.append(total_time*1000)
            message = json.loads(data)
            if int(self.hostID) == 1:
                msg = "a".encode()
                self.expectedBytes += len(msg)
                succeded = connection.send(msg)
                self.bytessent += succeded
                #self.expectedBytes += succeded
            ### Add state to TODO stack so worker thread can perform the received action ###
            if int(self.hostID) == 1:
                self.mergeStack.put((id, message))

            ### slave received state from master and should update its own database based on received state
            else:
                self.updatestate(message)
        else:
            self.dropped_messages += 1

        self.writeMessage()

        connection.close()

    ### Master node have received an updates from slave nodes and perform the action received to update its state
    def performaction(self, id, clock, received):
        (action, content) = received
        if int(clock) > self.centralclockholder[int(id)]:
            self.centralclockholder[int(id)] = clock
            if not dbexistcheck(self.hostID, self.hostID):
                addnewdb(self.hostID, self.hostID)
            ### If the action is insert perform the insert ***
            start_time = time.time()
            if action == "i":
                for table, entry in content.items():
                    if entry:
                        dbaddentry(self.hostID, self.hostID, table, entry[0])
            ### If the action is update then update the DB ###
            elif action == "u":
                for table, entry in content.items():
                    if entry:
                        dbdeleteentry(self.hostID, self.hostID, table, entry[0][0])
                        dbaddentry(self.hostID, self.hostID, table, entry[0])


            ### If the action is delete, then delete a row ###
            else:
                for table, entry in content.items():
                    if entry:
                        dbdeleteentry(self.hostID, self.hostID, table, entry[0][0])
            end_time = time.time()
            total_time = end_time-start_time
            self.mergetime.append((total_time*1000))

            self.writeMerge()



        else:
            print("***  Already added to  DB  ***")


    ###  Slave node have received the state from the master node and will update its own state to this state
    def updatestate(self, state):
        if not dbexistcheck(self.hostID, 1):
            addnewdb(self.hostID, 1)
        start_time = time.time()
        for table, tlist in state[0].items():
            if tlist:
                for entry in tlist:
                    try:
                        if not dbentryexist(self.hostID, 1, table, entry[0]):
                            dbaddentry(self.hostID, 1, table, entry)
                    except sqlite3.OperationalError:
                        self.updatestate(state[0])
        end_time = time.time()
        total_time = end_time-start_time
        self.mergetime.append((total_time*1000))
        self.writeMerge()

        if self.domatrix == 1 and self.hostID != 1:

            while len(self.msglist) < state[1]-1:
                self.msglist.append(0)

            self.msglist.append(1)

            file = open("testdata/divergelist" + str(self.hostID), "w")
            os.chmod("testdata/divergelist" + str(self.hostID), 0o777)
            file.write(json.dumps(self.msglist) + "\n")
            file.close()

    # Broadcast a message to all other nodes
    def broadcaststate(self):


        while True:
            time.sleep(25)

            if not dbexistcheck(self.hostID, self.hostID):
                addnewdb(self.hostID, self.hostID)
            try:
                state = dbquery(self.hostID, self.hostID)
                message = (state, self.msgcounter)
                self.msgcounter += 1


                for host in range(1, (int(self.numberofhost) + 1)):
                    host = self.ip + str(host)

                    # do not send to ourselves
                    if host != self.ownIP:
                        thread = Thread(target=self.sendmessage, args=[message, host, self.port])
                        thread.daemon = True
                        thread.start()
                        #self.sendmessage(message, host, self.port)
            except sqlite3.OperationalError:
                print("*"*20)
                print(" ")
                print(" ")
                print("*"*20)
                pass

    # sending message to another host
    def sendmessage(self, message, host, port):
        finished = False
        received = False

        try:
            serializeddata = json.dumps(message)
        except (TypeError, ValueError) as e:
            raise Exception("Not Json")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            data = (serializeddata + ";").encode()
            datasize = len(data)
            self.messageSizes.append(datasize)
            self.expectedBytes += datasize
            totalsent = 0
            while totalsent < datasize:
                sent = sock.send(data[totalsent:])
                if sent == 0:
                    print("Connection broken closing socket")
                    break
                totalsent += sent
                if totalsent == datasize:
                    finished = True
            if finished and self.hostID != 1:
                byte = sock.recv(1)
                byte = byte.decode()
                if byte == "a":
                    received = True
            sock.close()
            self.bytessent += totalsent
            ### Write bytes sent to testdatafile ###
            self.writeBytes()
            return received

        except Exception as e:
            return received

        ### antingen räkna hur lång tid det tar att ett meddelande kommer fram till den andra noden och då även räkna
        # hur många meddelanden som tappas p.g.a. i CRDT så kommer inte samma meddelande skickas flera gånger utan en
        # ny state kommer skickas nästa gång som inte säkert är samma. ska man då tolka detta som sama eller ett nytt?
        # Räkna på tiden det tar för en merge, local update, copy state etc. och jämföra dessa? vilken latency är bäst?



    def localthread(self):
        filename = "localstates/local"+self.hostID
        sendQueue = Queue()
        currentMessage = None
        position = 0

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
            if text:
                for i in range(position, len(text)):
                    action = text[i]
                    try:
                        action = json.loads(action)


                ### Send the update from the local machine to the centralized machine ###
                ### if you are a slave node you send the update to master, if you are master you perform update

                        if int(self.hostID) != 1:
                            if action:
                                self.logicalclock += 1
                                sendQueue.put((self.logicalclock, action))

                        ### Master node perform actions received from other nodes that are saved in a buffer ###
                        else:
                            if action:
                                self.logicalclock += 1
                                self.mergeStack.put((self.hostID, (self.logicalclock, action)))
                    except:
                        pass
                position = len(text)

                if int(self.hostID) != 1:
                    if currentMessage is None and not sendQueue.empty():
                        currentMessage = sendQueue.get()
                    if currentMessage is not None:
                        if self.sendmessage(currentMessage, self.ip + "1", 1337):
                            currentMessage = None
                            sendQueue.task_done()
                else:
                    if not self.mergeStack.empty():
                        (id, (clock, operation)) = self.mergeStack.get()
                        self.performaction(id, clock, operation)
                        self.mergeStack.task_done()




    def writeMerge(self):
        ### Write results to testfile ###
        file = open("testdata/mergelatency" + str(self.hostID), "w")
        os.chmod("testdata/mergelatency" + str(self.hostID), 0o777)
        file.write(json.dumps(self.mergetime))
        file.close()

    def writeBytes(self):
        ### Create testdata file if it doesn't exist ###
        file = open("testdata/bytes"+str(self.hostID), "w")
        os.chmod("testdata/bytes"+str(self.hostID), 0o777)
        file.write(json.dumps((self.bytessent, self.expectedBytes)))
        file.close()

        file = open("testdata/messagesize" + str(self.hostID), "w")
        os.chmod("testdata/messagesize" + str(self.hostID), 0o777)
        file.write(json.dumps(self.messageSizes))
        file.close()



    def writeMessage(self):
        file = open("testdata/messagelatency" + str(self.hostID), "w")
        os.chmod("testdata/messagelatency" + str(self.hostID), 0o777)
        file.write(json.dumps(self.messagetime))
        file.close()

        file = open("testdata/droppedmessages" + str(self.hostID), "w")
        os.chmod("testdata/droppedmessages" + str(self.hostID), 0o777)
        file.write(str(self.dropped_messages))
        file.close()






if __name__ == '__main__':
    server = Server()
    try:
        server.run(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        print("Too few arguments")

