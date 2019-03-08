import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1337        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    while True:
        data = []
        byte = s.recv(1)
        byte = byte.decode()
        print(byte)
        if byte == ";":
            s.close()
            print(data)
            break
        elif byte:
            print("ih")
            data.append(byte)
        else:
            break

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

