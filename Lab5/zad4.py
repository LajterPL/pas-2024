import socket
from datetime import datetime

host = '127.0.0.1'

tcp_port = 2914
udp_port = 2915

with socket.socket() as s:
    s.settimeout(5)
    s.connect((host, tcp_port))

    t1 = datetime.now()
    s.send("PING".encode())
    data = s.recv(1024)

    if data:
        t2 = datetime.now()

        print(f'Czas odpowiedzi serwera TCP: {t2 - t1}')

    s.close()


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(5)
    s.connect((host, udp_port))

    t1 = datetime.now()
    s.send("PING".encode())
    data = s.recv(1024)

    if data:
        t2 = datetime.now()

        print(f'Czas odpowiedzi serwera UDP: {t2 - t1}')


    s.close()
