import socket

host = socket.gethostbyname("127.0.0.1")
port = 2910

class UdpData:
    def __init__(self):
        self.source = None
        self.destination = None
        self.data = None

    def fromString(self, string):
        string = string.replace(" ", "")

        self.source = int(string[0:4], 16)
        self.destination = int(string[4: 8], 16)

        data_string = string[16:]
        self.data = ''.join([chr(int(data_string[i:i+2], 16)) for i in range(0, len(data_string), 2)])


udp = UdpData()
udp.fromString("ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f 6e 20 69 73 20 66 75 6e")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        s.settimeout(5)
        s.connect((host, port))
        s.send(f'zad14odp;src;{udp.source};dst;{udp.destination};data;{udp.data}'.encode("utf-8"));
        msg = s.recv(1024)
        print(f'Odpowiedź serwera: {msg.decode("utf-8")}')
        s.close()
    except TimeoutError:
        print("Połączenie nieudane")