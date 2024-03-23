import socket

host = "127.0.0.1"
port = 2911

class UdpData:
    def __init__(self, string):
        string = string.strip().replace(" ", "")

        self.source = int(string[0:4], 16)
        self.destination = int(string[4: 8], 16)

        data_string = string[16:]
        self.data = ''.join([chr(int(data_string[i:i + 2], 16)) for i in range(0, len(data_string), 2)])

class TcpData:
    def __init__(self, string):
        string = string.strip().replace(" ", "")

        self.source = int(string[0:4], 16)
        self.destination = int(string[4:8], 16)

        data_string = string[64:]
        self.data = ''.join([chr(int(data_string[i:i + 2], 16)) for i in range(0, len(data_string), 2)])

class IpData:
    def __init__(self, string):
        string = string.strip().replace(" ", "")

        self.version = int(string[0:1], 16)

        source_hex = string[24:32]
        self.source = (f'{int(source_hex[0:2], 16)}.{int(source_hex[2:4], 16)}.' +
                       f'{int(source_hex[4:6], 16)}.{int(source_hex[6:8], 16)}')

        destination_hex = string[32:40]
        self.destination = (f'{int(destination_hex[0:2], 16)}.{int(destination_hex[2:4], 16)}.' +
                            f'{int(destination_hex[4:6], 16)}.{int(destination_hex[6:8], 16)}')

        self.protocol = string[18:20]
        data_string = string[40:]

        if self.protocol == "06":
            self.protocol_data = TcpData(data_string)
        elif self.protocol == "11":
            self.protocol_data = UdpData(data_string)


ip_data = IpData(   "45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b" +
                    "c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1" +
                    "80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01" +
                    "00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67" +
                    "72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        s.settimeout(5)
        s.connect((host, port))

        s.send(f'zad15odpA;ver;{ip_data.version};srcip;{ip_data.source};dstip;{ip_data.destination};type;{ip_data.protocol}'.encode());

        msg = s.recv(1024)
        msg = msg.decode()
        print(f'Odpowiedź serwera: {msg}')


        if msg == "TAK":
            s.send((f'zad15odpB;srcport;{ip_data.protocol_data.source};' +
                   f'dstport;{ip_data.protocol_data.destination};' +
                   f'data;{ip_data.protocol_data.data}').encode())

            msg = s.recv(1024)
            msg = msg.decode()
            print(f'Odpowiedź serwera: {msg}')


        s.close()
    except TimeoutError:
        print("Połączenie nieudane")

