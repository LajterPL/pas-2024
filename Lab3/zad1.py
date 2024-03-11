import socket

host = socket.gethostbyname("ntp1.tp.pl")
port = 37

with socket.socket() as s:
    try:
        s.settimeout(5)
        s.connect((host, port))
        data = s.recv(1024)
        print(int.from_bytes(data, byteorder='big'))
        s.close()
    except:
        print("Połączenie nieudane")
