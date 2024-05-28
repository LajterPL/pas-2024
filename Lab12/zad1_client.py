import socket

host = "127.0.0.1"
port = 1350

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)

    try:
        s.connect((host, port))

        while True:
            s.send(input().encode())
            data = s.recv(2048)

            if data:
                print(data.decode())

    except TimeoutError:
        print("Przekroczono czas oczekiwania...")
