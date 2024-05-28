import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)

        self.client = client

    def run(self):

        while True:
            try:
                data = self.client.recv(2048)

                if data:
                    self.client.send(data)
            except:
                client_address = self.client.getnameinfo()

                print(f'Klient {client_address[0]}:{client_address[1]} zakończył połączenie')


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

            while True:
                client_socket, client_address = s.accept()

                print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')

                c = ClientThread(client_socket)
                c.start()

server = Server("127.0.0.1", 1350)
server.run()
