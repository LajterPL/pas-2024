import socket
import threading

def write_log(s):
    with open("server.log", "a") as log:
        log.write(s)
        log.close()

class ClientThread(threading.Thread):
    def __init__(self, client, address, lock):
        threading.Thread.__init__(self)

        self.client = client
        self.address = address
        self.lock = lock

    def run(self):
        while True:
            data = self.client.recv(2048)

            if data:
                self.client.send(data)

                self.lock.acquire()

                write_log(f'[{self.address[0]}:{self.address[1]}] {data.decode()}\n')

                self.lock.release()


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

            with open("server.log", "w") as log:
                log.write(f'[Server {self.host}:{self.port}]\n')
                log.close()

            log_lock = threading.Lock()

            while True:
                client_socket, client_address = s.accept()

                print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')

                log_lock.acquire()

                write_log(f'[{client_address[0]}:{client_address[1]}] connected\n')

                log_lock.release()

                c = ClientThread(client_socket, client_address, log_lock)
                c.start()

server = Server("127.0.0.1", 1350)
server.run()
