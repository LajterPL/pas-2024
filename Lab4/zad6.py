import socket

host = '127.0.0.1'
port = 2903

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
                    data = socket.gethostbyname(data.decode())
                except:
                    data = "Nieprawidłowa nazwa hostname"

                srv_socket.sendto(data.encode(), adress)
                print(f'Odesłano dane do {adress[0]}:{adress[1]}')

            except:
                print("Nie udało się odesłać danych")
finally:
    srv_socket.close()