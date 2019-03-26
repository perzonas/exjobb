import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1337        # The port used by the server

toSend = {'test3': {'customers': [(2, 'test2', '55', 'herp', 'derp', 1337, 'durr')]}, 'WorkOrderData6.db':
    {'materials': [(4, 'Rocks', 1544443198241, ''), (5, 'Sand', 1544443203563, ''), (6, 'Thune', 1544610204575, ''),
                   (7, 'Grus', 1544689044056, '')]}}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("sending hello world")
    s.sendall((json.dumps(toSend)+";").encode())


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

