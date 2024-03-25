import socket
import itertools

host = '127.0.0.1'
hidden_port = 2913

with socket.socket() as tcp_sock:
    tcp_sock.settimeout(5)

    seq_ports = []

### Szukanie portów należących do sekwencji
    for test_port in range(65):

        test_port = test_port * 1000 + 666

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:

            try:
                udp_sock.connect((host, test_port))

                udp_sock.send("PING".encode())
                msg = udp_sock.recv(1024)

                if msg and msg.decode() == "PONG":

                    seq_ports.append(test_port)

                udp_sock.close()
            except TimeoutError:
                pass

### Testowanie sekwencji
    for seq in list(itertools.permutations(seq_ports)):

        for port in seq:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
                udp_sock.connect((host, port))
                udp_sock.send("PING".encode())
                data = udp_sock.recv(1024)

        try:
            tcp_sock.connect((host, hidden_port))
            data = tcp_sock.recv(1024)

            if data:
                print(data)
                tcp_sock.close()
                exit()
        except TimeoutError:
            pass

    print("Nie udało się znaleźć kombinacji")
    tcp_sock.close()
