import socket

host = "httpbin.org"
port = 80



with socket.socket() as s:
    s.settimeout(10)

    try:
        s.connect((host, port))

        s.send(f'GET /html \r\nHOST: {host} \r\nUser-Agent: Safari/7.0.3'.encode())

        html_data = ""

        while not html_data.endswith("</html>"):
            data = s.recv(2048)
            html_data += data.decode()

        with open("saved-site.html", 'w') as file:
            file.write(html_data)

        print(html_data)

    except TimeoutError:
        print("Nieudane połączenie z serwerem")