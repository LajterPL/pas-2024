import socket

host = "127.0.0.1"
port = 2900

with socket.socket() as s:
    try:
        s.settimeout(5)
        s.connect((host, port))

        msg = input()

        while msg != "exit":
            print(f'Wysłano: {msg}')

            s.send(msg.encode("utf-8"))

            data = s.recv(1024)

            print(f'Odebrano: {data.decode("utf-8")}')

            msg = input()

        s.close()
    except TimeoutError:
        print("Połączenie nieudane")