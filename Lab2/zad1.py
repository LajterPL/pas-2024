import socket
import time
import datetime

host = socket.gethostbyname("ntp1.tp.pl")
port = 37

with socket.socket() as s:
    try:
        s.settimeout(5)
        s.connect((host, port))

        data = s.recv(1024)

        REF_TIME_1970 = 2208988800
        t = int.from_bytes(data, byteorder='big')
        t -= REF_TIME_1970

        t = datetime.datetime.fromtimestamp(t)

        print(t)
        s.close()
    except TimeoutError:
        print("Połączenie nieudane")
