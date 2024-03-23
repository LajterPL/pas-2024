import socket

host = socket.gethostbyname("127.0.0.1")
port = 2909


class TcpData:
    def __init__(self, string):
        string = string.strip().replace(" ", "")

        self.source = int(string[0:4], 16)
        self.destination = int(string[4:8], 16)

        data_string = string[64:]
        self.data = ''.join([chr(int(data_string[i:i + 2], 16)) for i in range(0, len(data_string), 2)])

tcp_data = TcpData( "0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 " +
                    "00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee " +
                    "00 1a 4c ee 68 65 6c 6c 6f 20 3a 29")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        s.settimeout(5)
        s.connect((host, port))
        s.send(f'zad13odp;src;{tcp_data.source};dst;{tcp_data.destination};data;{tcp_data.data}'.encode());
        msg = s.recv(1024)
        print(f'Odpowiedź serwera: {msg.decode("utf-8")}')
        s.close()
    except TimeoutError:
        print("Połączenie nieudane")