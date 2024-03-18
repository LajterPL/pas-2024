import socket

host = "127.0.0.1"
port = 2906

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        s.settimeout(5)
        s.connect((host, port))

        msg = input()
        s.send(msg.encode("utf-8"))

        data = s.recv(1024)

        print(f'Odebrano: {data.decode("utf-8")}')

        s.close()
    except TimeoutError:
        print("Połączenie nieudane")