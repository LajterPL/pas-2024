import sys
import socket

try:
    hostname = sys.argv[1]
    try:
        ip = socket.gethostbyname(hostname)
        print(f'{hostname} - {ip}')
    except:
        print("Nie udało się znaleźć adresu o podanej nazwie")
except:
    print("Nie podano nazwy hostname")
