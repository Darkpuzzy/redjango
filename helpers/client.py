import json
import socket

HOST = 'localhost'    # The remote host
PORT = 50007          # The same port as used by the server


def connect_to():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'get')
            data = s.recv(1024)
            print(data.decode())
            if data == b'':
                return {'Stopped'}
            else:
                system_load = json.loads(data.decode())
                return system_load
    except Exception as e:
        return {'Error': str(e)}
