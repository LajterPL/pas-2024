import socket

host = '127.0.0.1'
port = 2912

with socket.socket() as s:
    try:
        s.settimeout(5)
        s.connect((host, port))

        while True:
            number = input()

            s.send(number.encode())

            msg = s.recv(1024)

            print(f'Odpowiedź serwera: {msg.decode()}')



    except TimeoutError:
        print("Połączenie nieudane")
    finally:
        s.close()