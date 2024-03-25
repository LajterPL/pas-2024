import socket

host = '127.0.0.1'
port = 2915

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

        if data:
            srv_socket.sendto("PONG".encode(), adress)

finally:
    srv_socket.close()