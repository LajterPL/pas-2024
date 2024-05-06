import socket

host = "httpbin.org"
port = 80

with socket.socket() as s:
    s.settimeout(10)

    try:
        s.connect((host, port))

        s.send(f'GET /image/png \r\nHOST: {host} \r\n'.encode())

        with open("saved-img.png", 'bw') as file:

            data = s.recv(2048)

            while data != b'':
                file.write(data)
                data = s.recv(2048)


    except TimeoutError:
        print("Nieudane połączenie z serwerem")