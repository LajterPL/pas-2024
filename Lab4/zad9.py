import socket

host = socket.gethostbyname("127.0.0.1")
port = 2910

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

                try:
                    print(data)
                    data = data.decode().split(";")

                    data_src = data[2]
                    data_dst = data[4]
                    data_content = data[6]

                    udp = UdpData()
                    udp.fromString("ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f 6e 20 69 73 20 66 75 6e")

                    if (data_src == str(udp.source) and data_dst == str(udp.destination) and data_content == udp.data):
                        srv_socket.sendto("TAK".encode(), adress)
                    else:
                        srv_socket.sendto("NIE".encode(), adress)

                except:
                    srv_socket.sendto("BAD_SYNTAX".encode(), adress)

            except Exception as e:
                print(e)
finally:
    srv_socket.close()