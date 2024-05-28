import random
import socket
import threading

rand_int = random.randint(1, 100)

class ClientThread(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)

        self.client = client
        self.address = address

    def run(self):

        while True:
            try:
                data = self.client.recv(2048)

                if data:
                    str = data.decode()

                    if str.isdigit():
                        if int(str) > rand_int:
                            self.client.send("Dana liczba jest większa od wylosowanej".encode())
                        elif int(str) < rand_int:
                            self.client.send("Dana liczba jest mniejsza od wylosowanej".encode())
                        else:
                            self.client.send("Udało się zgadnąć liczbę!".encode())
                            self.client.shutdown(socket.SHUT_RDWR)
                            self.client.close()

                            print(f'Zakończono połączenie z {self.address[0]}:{self.address[1]}')
                            return
                    else:
                        self.client.send("Dana musi być liczbą".encode())
            except TimeoutError:
                print(f'Klient {self.address[0]}:{self.address[1]} zakończył połączenie')


class Server:
    def __init__(self, host, port):

        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(10)

            print(f'Nasłuchiwanie połączeń pod adresem {self.host}:{self.port}...')
            print(f'Losowa liczba: {rand_int}')

            while True:
                client_socket, client_address = s.accept()

                print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')

                c = ClientThread(client_socket, client_address)
                c.start()

server = Server("127.0.0.1", 1350)
server.run()
