import sys
import socket

try:
    host = sys.argv[1]
    port = sys.argv[2]

    with socket.socket() as s:
        try:
            s.connect((host, port))
            print("Połączenie udane")
            s.close()
        except:
            print("Połączenie nieudane")
except:
    print("Należy podać adres i port serwera")