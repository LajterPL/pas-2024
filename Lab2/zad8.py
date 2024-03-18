import sys
import socket

if len(sys.argv) != 2:
    print("Niewłaściwa liczba argumentów")
else:
    try:
        host = socket.gethostbyname(sys.argv[1])

        print("Skanowanie portów...")
        print("Otwarte porty:")
        for port in range(1, 65535):
            with socket.socket() as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))

                if result == 0:
                    print(f'Port {port}: {socket.getservbyport(port, "tcp")}, otwarty')
    except:
        print("Nieprawidłowy adres serwera")