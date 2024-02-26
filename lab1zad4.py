import sys
import socket
def is_ip_valid(ip):

    ip = ip.split(".")
    if len(ip) != 4:
        return False

    for x in ip:
        try:
            if int(x) < 0 or int(x) > 255:
                return False
        except:
            return False

    return True

ip = sys.argv[1]

if is_ip_valid(ip):
    try:
        hostname = socket.gethostbyaddr(ip)
        print(f'{ip} - {hostname[0]}')
    except:
        print("Nie udało się pobrać hostname dla podanego adresu")