import sys
import socket

try:
    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket() as s:
        try:
            s.settimeout(5)
            s.connect((host, port))
            print(f'Port {port}: {socket.getservbyport(port, "tcp")}, otwarty')
            s.close()
        except Exception as e:
            print(e)
except:
    print("Należy podać adres i port serwera")