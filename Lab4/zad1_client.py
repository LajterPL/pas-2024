import socket
import datetime

host = '127.0.0.1'
port = 2937

with socket.socket() as s:
    try:
        s.settimeout(5)
        s.connect((host, port))
        s.send("Test".encode())
        data = s.recv(1024).decode()
        print(data)
        s.close()
    except TimeoutError:
        print("Połączenie nieudane")