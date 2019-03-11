import sys
import time
import socket
from threading import Thread
import json


class Server:
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

        # AF_INET -> ipv4 and SOCK_STREAM -> tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Starting server")
        sock.bind((self.test, self.port))
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
                print("Exception when accepting connection or creating thread.")
                print(exception)

    # handling incoming connection
    def handleconnection(self, connection, connectinfo):
        print("handling connection from ", connectinfo)
        ip, port = connectinfo
        id = ip.split(".")[-1]
        message, type = self.retrievemessage(connection)
        print(message)
        print(type)

        #host, port = connectinfo
        #self.sendmessage(("hejsan", 12, 90), host, port, connection)

    def retrievemessage(self, connection):
        id = 0
        data = ""
        type = 0


        while True:
            byte = connection.recv(1)
            byte = byte.decode()
            if byte == ";":
                break
            elif byte:
                data += byte
            else:
                break
        type = int(data)
        data = ""
        while True:
            byte = connection.recv(1)
            byte = byte.decode()
            if byte == ";":
                connection.close()
                break
            elif byte:
                data += byte
            else:
                break
        message = json.loads(data)
        return message, type

    def broadcast(self, message, ):
        print("Broadcasting message to all hosts")
        for host in range(1, (self.numberofhost+1)):
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
        print(host, port)
        # sock.connect((host, port))
        print(serializeddata)
        connection.send((str(len(serializeddata))+";").encode(), (len(serializeddata)+1))
        print(len(serializeddata))

        connection.sendall((serializeddata+";").encode())







if __name__ == '__main__':
    server = Server()
    server.run(sys.argv[1])
