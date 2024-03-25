import random
import socket, select

HOST = '127.0.0.1'
PORT = 2912

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

random_number = random.randint(1, 1000)

print(f'Losowa liczba: {random_number}')

while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:

            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)

            print(f'Client {client_address[0]} connected...')

        else:
            try:
                data = sock.recv(1024)
                if data:

                    data = int(data)

                    if data > random_number:
                        sock.send("Za duża".encode())
                    elif data < random_number:
                        sock.send("Za mała".encode())
                    else:
                        sock.send("Zgadłeś!".encode())
                        server_socket.close()
                        exit()


            except:
                print(f'Client {client_address[0]} is offline...')
                sock.close()
                connected_clients_sockets.remove(sock)
                continue
server_socket.close()