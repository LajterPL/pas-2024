import socket
import ssl

host = "echo.websocket.org"
port = 443


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)

    s = ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23).wrap_socket(s, server_hostname=host)

    try:
        s.connect((host, port))
        s.send(f'GET / HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())


        data = s.recv(2048)
        print(data.decode())


    except TimeoutError:
        print("Przekroczono czas żądania...")