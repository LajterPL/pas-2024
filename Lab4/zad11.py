import socket

host = socket.gethostbyname("127.0.0.1")
port = 2911

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

try:
    srv_socket.bind((host, port))
except:
    print("Nieudane otworzenie socketa")
    exit()

print(f'Nasłuchiwanie połączeń pod adresem {host}:{port}')

try:
    while True:
        data, adress = srv_socket.recvfrom(1024)

        print(f'Otrzymano dane od {adress[0]}:{adress[1]}')

        if data:

            try:

                data = data.decode().split(";")

                if (data[0] == "zad15odpA" and
                    data[1] == "ver" and
                    data[3] == "srcip" and
                    data[5] == "dstip" and
                    data[7] == "type"):

                    if (data[2] == str(ip_data.version) and
                        data[4] == ip_data.source and
                        data[6] == ip_data.destination and
                        data[8] == ip_data.protocol):

                        srv_socket.sendto("TAK".encode(), adress)

                        data, adress = srv_socket.recvfrom(1024)

                        if data:
                            data = data.decode().split(";")

                            if data[0] == "zad15odpB" and data[1] == "srcport" and data[3] == "dstport" and data[5] == "data":
                                if (data[2] == str(ip_data.protocol_data.source) and
                                    data[4] == str(ip_data.protocol_data.destination) and
                                    data[6] == ip_data.protocol_data.data):

                                    srv_socket.sendto("TAK".encode(), adress)

                                else:
                                    srv_socket.sendto("NIE".encode(), adress)
                            else:
                                srv_socket.sendto("BAD_SYNTAX".encode(), adress)
                    else:
                        srv_socket.sendto("NIE".encode(), adress)
                else:
                    srv_socket.sendto("BAD_SYNTAX".encode(), adress)


            except Exception as e:
                print(e)
finally:
    srv_socket.close()