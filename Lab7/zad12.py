import socket
import datetime
import base64

class Mail:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.mail_from = None
        self.mail_to = None
        self.subject = None
        self.text = None
        self.attachments = []
    def set_details(self, sender, reciver, subject):
        self.mail_from = sender
        self.mail_to = reciver
        self.subject = subject
    def set_text(self, text):
        self.text = text
    def add_attachment(self, type, name, path):

        try:
            file = open(path, 'rb')
            data = base64.b64encode(file.read())

            self.attachments.append((type, name, data))
        except IOError:
            print("Nie udało się załączyć pliku")
    def get_size(self):
        size = 0

        if self.text != None:
            size += len(self.text.encode("utf-8"))

        for file in self.attachments:
            size += len(file[2])

        return size


server_domain = "localhost"
host = '127.0.0.1'
port = 110

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(10)

print(f'Nasłuchiwanie połączeń pod adresem {host}:{port}...')

client_socket, client_address = server_socket.accept()

print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')

def reply(str):
    client_socket.send((str + "\r\n").encode())


reply('+OK server ready')

user_name = ""
user_password = ""
mailbox = []

command = ""


mail = Mail()
mail.set_details("test@localhost", "user@localhost", "Wiadomosc testowa")
mail.set_text("Testowa wiadomosc e-mail\no wielu liniach")
mail.add_attachment('image/gif', 'test_img.jpg', r"C:\Users\white\PycharmProjects\pas-2024\Lab7\test_img.jpg")

mailbox.append(mail)

mailbox_size = 0

for msg in mailbox:
    mailbox_size += msg.get_size()

while True:
    try:
        data = client_socket.recv(1024)
        if data:
            char = data.decode()

            if char.endswith("\r\n"):
                if char != "\r\n":
                    command = char[:-2]

                print(f'Otrzymano komendę: {command}')

                tokens = command.split(" ")

                match tokens[0]:
                    case "USER":

                        if user_name != "":
                            reply("-ERR Bad sequence of commands")
                        else:
                            if len(tokens) != 2:
                                reply("-ERR Syntax error in parameters or arguments")
                            else:
                                if tokens[1] == 'user':
                                    user_name = tokens[1]
                                reply('+OK send PASS')
                    case "PASS":

                        if user_name == "" or user_password != "":
                            reply("-ERR Bad sequence of commands")
                        else:
                            if len(tokens) != 2:
                                reply("-ERR Syntax error in parameters or arguments")
                            else:
                                if tokens[1] == 'password':
                                    user_password = tokens[1]
                                reply('+OK Welcome')
                    case "STAT":

                        if user_name == "" and user_password == "":
                            reply("-ERR Need to authenticate")
                        elif len(tokens) != 1:
                            reply("-ERR Wrong number of arguments")
                        else:
                            reply(f'+OK {len(mailbox)} messages ({mailbox_size} bytes)')
                    case "LIST":

                        if user_name == "" and user_password == "":
                            reply("-ERR Need to authenticate")
                        elif len(tokens) != 1:
                            reply("-ERR Wrong number of arguments")
                        else:
                            reply(f'+OK {len(mailbox)} messages ({mailbox_size} bytes)')

                            for idx in range(len(mailbox)):
                                reply(f'{idx + 1} {mailbox[idx].get_size()}')

                            reply(".")
                    case "DELE":

                        if user_name == "" and user_password == "":
                            reply("-ERR Need to authenticate")
                        elif len(tokens) != 2:
                            reply("-ERR Wrong number of arguments")
                        else:

                            if tokens[1].isdigit():

                                msg = mailbox[int(tokens[1]) - 1]
                                mailbox_size -= msg.get_size()
                                mailbox.remove(msg)

                                reply(f'+OK Deleted message {tokens[1]}')
                            else:
                                reply("-ERR Wrong argument")
                    case "RETR":

                        if user_name == "" and user_password == "":
                            reply("-ERR Need to authenticate")
                        elif len(tokens) != 2:
                            reply("-ERR Wrong number of arguments")
                        else:

                            if tokens[1].isdigit():

                                msg = mailbox[int(tokens[1]) - 1]

                                reply(f'+OK Message follows')

                                reply(f'Date: {msg.date.strftime("%d.%m.%Y %H:%M:%S")}')
                                reply(f'Subject: {msg.subject}')
                                reply(f'From: {msg.mail_from}')
                                reply(f'To: {msg.mail_to}')

                                if not msg.text == None:
                                    reply('Content-Type: text/plain')
                                    reply('Content-Transfer-Encoding: quoted-printable')

                                    for line in msg.text.split("\n"):
                                        reply(line)

                                if len(msg.attachments) > 0:
                                    for attachment in msg.attachments:
                                        reply(f'Content-Type: {attachment[0]};\n\r\tname="{attachment[1]}"')
                                        reply('Content-Transfer-Encoding: base64')
                                        reply(f'Content-Disposition: attachment;\n\r\tfilename="{attachment[1]}"')

                                        reply(f'{attachment[2].decode()}')

                                reply(".")
                            else:
                                reply("-ERR Wrong argument")
                    case 'QUIT':
                        if len(tokens) != 1:
                            reply("-ERR Syntax error in parameters or arguments")
                        else:
                            client_socket.close()

                    case other:
                        client_socket.send("-ERR Syntax Error\r\n".encode())

                command = ""
            elif char == '\x08':
                command = command[0:-1]
            else:
                command += char
    except:
        print(f'Klient {client_address[0]}:{client_address[1]} zakończył połączenie')

        client_socket, client_address = server_socket.accept()
        print(f'Nowe połączenie z adresem {client_address[0]}:{client_address[1]}')
        reply('+OK server ready')

        user_name = ""
        user_password = ""
        mailbox = [mail]

        continue

server_socket.close()