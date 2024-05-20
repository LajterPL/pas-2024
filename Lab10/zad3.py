import socket
import ssl

host = "echo.websocket.org"
port = 443


class WebSocketPacket:
    def __init__(self, opcode, length, payload):
        self.opcode = opcode
        self.length = length
        self.payload = payload

    def get_bytes(self) -> bytearray:
        frame = ''

        frame += '1' # FIN
        frame += '000' # RSV
        frame += bin(self.opcode)[2:].zfill(4) # OPCODE
        frame += '1' # MASK

        if self.length <= 125:
            frame += bin(self.length)[2:].zfill(7)
            frame = int(frame, 2).to_bytes(2, 'big')
        elif self.length <= 131071:
            frame += bin(126)[2:].zfill(7)
            frame += bin(self.length)[2:].zfill(16)
            frame = int(frame, 2).to_bytes(4, 'big')
        else:
            frame += bin(127)[2:].zfill(7)
            frame += bin(self.length)[2:].zfill(64)
            frame = int(frame, 2).to_bytes(10, 'big')

        frame += int(0).to_bytes(4, 'big')
        frame += self.payload

        return frame


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)

    s = ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23).wrap_socket(s, server_hostname=host)

    msg = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi elementum ligula eros, quis egestas est maximus vel. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In tristique purus quis eleifend non. "
    msg = msg.encode()


    websocket_frame = WebSocketPacket(1, len(msg), msg)

    print(websocket_frame.get_bytes())

    try:
        s.connect((host, port))
        s.send(
            f'GET / HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())

        data = s.recv(2048)
        print(data.decode())

        data = s.recv(2048)
        print(data)

        s.send(websocket_frame.get_bytes())

        data = s.recv(2048)
        print(data)

        print("Wiadomość wysłana")


    except TimeoutError:
        print("Przekroczono czas żądania...")