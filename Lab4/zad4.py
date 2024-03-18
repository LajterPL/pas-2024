import socket

host = '127.0.0.1'
port = 2902

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    srv_socket.bind((host, port))
except:
    print("Nieudane otworzenie socketa")
    exit()

print(f'Nasłuchiwanie połączeń pod adresem {host}:{port}')

try:
    while True:
        x, adress = srv_socket.recvfrom(1024)
        op, adress = srv_socket.recvfrom(1024)
        y, adress = srv_socket.recvfrom(1024)

        print(f'Otrzymano dane od {adress[0]}:{adress[1]}')

        if x and op and y:

            try:

                result = None

                match(op.decode()):
                    case '+':
                        result = float(x) + float(y)
                    case '-':
                        result = float(x) - float(y)
                    case '/':
                        result = float(x) / float(y)
                    case '*':
                        result = float(x) * float(y)
                    case _:
                        result = "Niewłaściwa operacja"


                srv_socket.sendto(str(result).encode(), adress)
                print(f'Odesłano dane do {adress[0]}:{adress[1]}')

            except ValueError as e:
                srv_socket.sendto(str(e).encode(), adress)
            except:
                print("Nie udało się odesłać danych")
finally:
    srv_socket.close()