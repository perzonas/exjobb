import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1337        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("sending hello world")
    s.send((str(120)+";").encode(), (len(str(120))+1))
    s.sendall((json.dumps("Hello world")+";").encode())
    if True:
        data = []
        byte = s.recv(1)
        message = ""
        while True:
            if byte.decode() == ";":
                s.close()
                print(data)
                break
            elif byte:
                message += byte.decode()
                byte = s.recv(1)
            else:
                break
        print(message)

        message = message[2:]
        converted = json.loads(message)
        print(converted[0])

    """ while True:
        data = s.recv(1)
        data = data.decode()
        if data == ";":
            length = int(data)
            data = ""
            while len(data) >= length:
                data = s.recv(1)
                data = data.decode()
            s.close()
            break
            
            """

