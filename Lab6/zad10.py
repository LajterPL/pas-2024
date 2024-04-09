import socket

server_domain = "localhost"
host = '127.0.0.1'
port = 587

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(10)

print(f'Nasłuchiwanie połączeń pod adresem {host}:{port}...')

client_socket, client_address = server_socket.accept()

print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')

def reply(str):
    client_socket.send((str + "\r\n").encode())


reply(f'220 {server_domain} Service Ready')

client_domain = ""
mail_from = ""
mail_to = ""
mail_data = ""
command = ""

while True:
    try:
        data = client_socket.recv(1024)
        if data:
            char = data.decode()

            if char == "\r\n":
                print(f'Otrzymano komendę: {command}')

                tokens = command.split(" ")

                match tokens[0]:
                    case "HELO":

                        if client_domain != "":
                            reply("503 Bad sequence of commands")
                        else:
                            if len(tokens) != 2:
                                reply("501 Syntax error in parameters or arguments")
                            else:
                                client_domain = tokens[1]
                                reply(f'250 {server_domain} OK')

                    case "HELP":
                        if len(tokens) == 1:
                            reply(f'250 {server_domain} OK')

                            client_socket.send(("DOSTEPNE KOMENDY:\r\nHELO\r\nHELP\r\nRSET" +
                                           "\r\nQUIT\r\nNOOP\r\nMAIL FORM\r\nRCPT TO\r\nDATA\r\n").encode())
                        else:
                            reply("504 Command parameter is not implemented")
                    case "RSET":
                        if len(tokens) == 1:
                            reply(f'250 {server_domain} OK')

                            client_domain = ""
                            mail_from = ""
                            mail_to = ""
                            mail_data = ""
                        else:
                            reply("504 Command parameter is not implemented")
                    case "QUIT":
                        if len(tokens) == 1:
                            reply(f'221 {server_domain} Service closing transmission channel')

                            client_socket.close()
                        else:
                            reply("504 Command parameter is not implemented")
                    case "NOOP":
                        if len(tokens) == 1:
                            reply(f'250 {server_domain} OK')
                        else:
                            reply("504 Command parameter is not implemented")
                    case "MAIL":
                        if mail_from != "":
                            reply("503 Bad sequence of commands")
                        else:
                            if len(tokens) == 3 and tokens[1] == "FROM":
                                mail_from = tokens[2]
                                reply(f'250 {server_domain} OK')
                            else:
                                reply("501 Syntax error in parameters or arguments")
                    case "RCPT":
                        if mail_from == "" or mail_to != "":
                            reply("503 Bad sequence of commands")
                        else:
                            if len(tokens) == 3 and tokens[1] == "TO":
                                mail_to = tokens[2]
                                reply(f'250 {server_domain} OK')
                            else:
                                reply("501 Syntax error in parameters or arguments")
                    case "DATA":
                        if mail_from == "" or mail_to == "":
                            reply("503 Bad sequence of commands")
                        else:
                            if len(tokens) == 1:
                                reply("354 Start mail input. End with <CRLF><CRLF>")

                                end_flag = False

                                while True:
                                    data = client_socket.recv(1024)

                                    if data:
                                        char = data.decode()

                                        if char == "\r\n":
                                            if end_flag:
                                                break
                                            else:
                                                end_flag = True
                                        else:
                                            end_flag = False

                                        mail_data += char

                                reply(f'250 {server_domain} OK')

                                print(f'FROM: {mail_from}\nTO: {mail_to}\n\n{mail_data}')

                                mail_to = ""
                                mail_from = ""
                                mail_data = ""

                            else:
                                reply("501 Syntax error in parameters or arguments")
                    case other:
                        client_socket.send("500 Syntax Error\r\n".encode())

                command = ""
            elif char == '\x08':
                command = command[0:-1]
            else:
                command += char
    except:
        print(f'Klient {client_address[0]}:{client_address[1]} zakończył połączenie')

        client_socket, client_address = server_socket.accept()
        print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')
        reply(f'220 {server_domain} Service Ready')

        client_domain = ""
        mail_from = ""
        mail_to = ""
        mail_data = ""
        command = ""

        continue

server_socket.close()