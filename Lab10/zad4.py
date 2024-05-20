import socket

class WebSocketPacket:
    def __init__(self, opcode, length, payload):
        self.opcode = opcode
        self.length = length
        self.payload = payload

    def get_bytes(self) -> bytes:
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

        frame += int(0).to_bytes(4, 'big') #MASK
        frame += self.payload

        return frame

def packet_from_bytes(b: bytes):
    opcode = int(bin(b[0])[6:], 2)

    mask = int(bin(b[1])[2:3], 2)

    packet_length = int(bin(b[1])[3:], 2)

    payload_index = 0

    if packet_length <= 125:
        payload_index += 2
    elif packet_length == 126:
        payload_index += 4
    else:
        payload_index += 10

    if mask == 1:
        payload_index += 4

    payload = b[payload_index:]

    return WebSocketPacket(opcode, len(payload), payload)

server_domain = "localhost"
host = '127.0.0.1'
port = 1300

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(10)

print(f'Nasłuchiwanie połączeń pod adresem {host}:{port}...')

client_socket, client_address = server_socket.accept()

print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')

while True:
    try:
        data = client_socket.recv(2048)
        if data:
            packet = packet_from_bytes(data)
            client_socket.send(packet.payload)

    except:
        print(f'Klient {client_address[0]}:{client_address[1]} zakończył połączenie')

        client_socket, client_address = server_socket.accept()
        print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')

        continue

server_socket.close()