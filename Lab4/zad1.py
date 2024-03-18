import socket, select
import datetime

REF_TIME_1970 = 2208988800

time_host = socket.gethostbyname("ntp1.tp.pl")
time_port = 37

host = '127.0.0.1'
port = 2937

clients = []

srv_socket = socket.socket()

try:
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind((host, port))
    srv_socket.listen(10)
    clients.append(srv_socket)
except:
    print("Nieudane otworzenie socketa")

print(f'Nasłuchiwanie połączeń pod adresem {host}:{port}')


while True:

    read_sockets, write_sockets, error_sockets = select.select(clients, [], [])

    for sock in clients:

        if sock == srv_socket:
            client_socket, client_address = srv_socket.accept()
            clients.append(client_socket)
            print(f'Nowe połączenie spod adresu {client_address}')

        else:
            try:
                data = sock.recv(1024)

                if data:
                    time = None

                    # Pobieranie czasu
                    with socket.socket() as s:
                        try:
                            s.settimeout(5)
                            s.connect((time_host, time_port))

                            data = s.recv(1024)

                            time = int.from_bytes(data, byteorder='big')
                            time -= REF_TIME_1970
                            time = datetime.datetime.fromtimestamp(time)

                        except TimeoutError:
                            print("Połączenie z serwerem czasu nieudane")
                        finally:
                            s.close()

                    # Odesłanie czasu klientowi
                    sock.send(time.strftime("%d.%m.%Y, %H:%M:%S").encode("utf-8"))
            except:
                sock.close()
                clients.remove(sock)
                print("Rozłączon klienta...")
                continue
                
srv_socket.close()