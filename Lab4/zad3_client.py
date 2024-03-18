import socket

host = '127.0.0.1'
port = 2901

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        s.settimeout(5)
        s.connect((host, port))
        s.send("Test".encode())
        data = s.recv(1024).decode()
        print(data)
        s.close()
    except TimeoutError:
        print("Połączenie nieudane")