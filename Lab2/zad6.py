import socket

host = "127.0.0.1"
port = 2902

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        s.settimeout(5)
        s.connect((host, port))

        data1 = input()
        op = input()
        data2 = input()

        s.send(data1.encode("utf-8"))
        s.send(op.encode("utf-8"))
        s.send(data2.encode("utf-8"))

        data = s.recv(1024)

        print(f'Odebrano: {data.decode("utf-8")}')

        s.close()
    except TimeoutError:
        print("Połączenie nieudane")