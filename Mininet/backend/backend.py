import sys
import time
import socket
from threading import Thread
import json


class Server:
    test = "127.0.0.1"
    port = 1337
    ownIP = "20.1.90."
    numberofhost = 0

    def run(self, hostnumber, numberofhosts=1):
        self.numberofhost = numberofhosts
        self.ownIP += str(hostnumber)

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

    def handleconnection(self, connection, connectinfo):
        print("handling connection")
        host, port = connectinfo
        self.sendmessage(("hejsan", 12, 90), host, port, connection)

    def broadcast(self, message, ):
        print("Broadcasting message")

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

        connection.sendall((serializeddata+";").encode())







if __name__ == '__main__':
    server = Server()
    server.run(sys.argv[1])
