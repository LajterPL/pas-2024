import socket

with socket.socket() as s:
    s.settimeout(15)

    print("Podaj adres IP: ")
    host = input()
    print("Podaj numer portu: ")
    port = input()

    try:
        s.connect((host, int(port)))
        data = s.recv(1024)

        print(data.decode())

        while True:
            print("Podaj nazwę użytkownika: ")
            user_name = input()
            s.send(f'USER {user_name}\r\n'.encode())

            data = s.recv(1024)

            if data.decode().startswith("+OK"):
                break

        while True:
            print("Podaj hasło: ")
            user_password = input()
            s.send(f'PASS {user_password}\r\n'.encode())

            data = s.recv(1024)

            if data.decode().startswith("+OK"):
                break

        s.send("LIST\r\n".encode())

        data = s.recv(1024)

        print(data.decode())

        data = s.recv(1024)

        while data.decode().startswith("."):
            res = data.decode()
            print(res)

            data = s.recv(1024)

        print("Podaj numer wiadomości do odczytu: ")
        msg_idx = input()

        s.send(f'RETR {msg_idx}\r\n'.encode())

        data = s.recv(1024)

        img_name = ""
        img = ""

        shown_lines = ["Date", "Subject", "From", "To"]

        while data.decode() != ".\r\n":

            res = data.decode()

            for start in shown_lines:
                if res.startswith(start):
                    print(res)
                    print("Stop")

            data = s.recv(1024)

    except TimeoutError:
        print("Połączenie z serwerem nie powiodło się")
    finally:
        s.close()