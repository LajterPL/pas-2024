import socket

host = "www.httpbin.org"
port = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)

    try:
        s.connect((host, port))

        content_size = 64

        print("Podaj imię: ")
        name = input()
        content_size += len(name)

        print("Podaj numer telefonu: ")
        tel = input()
        content_size += len(tel)

        print("Podaj adres e-mail: ")
        mail = input()
        content_size += len(mail)

        print("Podaj rozmiar pizzy: ")
        size = input()
        content_size += len(size)

        print("Podaj dodatki: ")
        topping = input()
        content_size += len(topping)

        print("Podaj godzinę dostawy: ")
        delivery = input()
        content_size += len(delivery)

        print("Podaj szczegóły dostawy: ")
        comments = input()
        content_size += len(comments)


        s.send(("POST /post HTTP/1.1\r\n" +
                "Host: httpbin.org\r\n" +
                "Content-Type: application/x-www-form-urlencoded\r\n" +
                f'Content-Length: {content_size}\r\n' +
                "\r\n" +
                f'comments={comments}&custemail={mail}&custname={name}&custtel={tel}&' +
                f'delivery={delivery}&size={size}&topping={topping}').encode())

        data = s.recv(4096)

        print(data.decode())

    except TimeoutError:
        print("Nieudane połączenie z serwerem")