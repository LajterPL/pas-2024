import socket

host = socket.gethostbyname("127.0.0.1")
port = 2909

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class TcpData:
    def __init__(self, string):
        string = string.strip().replace(" ", "")

        self.source = int(string[0:4], 16)
        self.destination = int(string[4:8], 16)

        data_string = string[64:]
        self.data = ''.join([chr(int(data_string[i:i + 2], 16)) for i in range(0, len(data_string), 2)])

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

                    tcp_data = TcpData("0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 " +
                                       "00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee " +
                                       "00 1a 4c ee 68 65 6c 6c 6f 20 3a 29")

                    if data[0] == "zad13odp":
                        if (data_src == str(tcp_data.source) and data_dst == str(tcp_data.destination) and data_content == tcp_data.data):
                            srv_socket.sendto("TAK".encode(), adress)
                        else:
                            srv_socket.sendto("NIE".encode(), adress)
                    else:
                        srv_socket.sendto("BAD_SYNTAX".encode(), adress)

                except Exception as e:
                    print(e)


            except Exception as e:
                print(e)
finally:
    srv_socket.close()