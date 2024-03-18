import socket, select

host = '127.0.0.1'
port = 2901

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
                    # Odesłanie danych klientowi
                    sock.send(data)
            except:
                sock.close()
                clients.remove(sock)
                print("Rozłączon klienta...")
                continue

srv_socket.close()