import socket


def login():
    username = input("Plz input ur username:")
    password = input("Plz input ur password:")
    client_socket.send(username.encode("utf8"))
    client_socket.send(password.encode("utf8"))

def logout():
    client_socket.close()


#Program starts here!
SERVER_ADDR = ("127.0.0.1", 60000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDR)
login()
logout()