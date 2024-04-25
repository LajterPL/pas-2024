import socket
import base64

with socket.socket() as s:
    s.settimeout(30)

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

        readFlag = True

        while readFlag:
            res = s.recv(1024).decode()

            for line in res.split("\r\n"):
                if line == ".":
                    readFlag = False
                else:
                    print(line)

        print("Podaj numer wiadomości do odczytu: ")
        msg_idx = input()

        s.send(f'RETR {msg_idx}\r\n'.encode())

        data = s.recv(1024)

        msg_content = ""

        readFlag = True

        while readFlag:
            res = s.recv(4096).decode()

            msg_content += res

            for line in res.split("\r\n"):
                if line == ".":
                    readFlag = False

        print("Odczyt wiadomości zakończony...")

        header, content = msg_content[:msg_content.index("Content-Type:")], msg_content[msg_content.index("Content-Type:"):]

        content = content.split("Content-Type:")

        print(header)

        for chunk in content:
            chunk = chunk.split("\r\n")

            if chunk[0].strip().startswith("text/plain"):
                for i in range(2, len(chunk)):
                    print(chunk[i])
            elif chunk[0].strip().startswith("image/gif"):

                file_name = chunk[0].split("name=\"")[1][:-1]

                img_data = chunk[3]
                img_data = base64.b64decode(img_data)

                with open(f'./Saved/{file_name}', 'wb') as file:
                    file.write(img_data)

                print(f'Zapisano plik {file_name}')

        s.close()
    except TimeoutError:
        print("Połączenie z serwerem nie powiodło się")
    finally:
        s.close()
