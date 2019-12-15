import socket
from threading import Thread
import msgList

def try_login(client_socket):
    while True:
        recv_data = client_socket.recv(1024)

        if recv_data:
            if len(LOGIN_POOL) >= 128:
                client_socket.send(msgList.err_service_full.encode("utf8"))
            data = recv_data.decode("utf8")
            if data in LOGIN_NAME_LIST:
                client_socket.send(msgList.err_existedNickName.encode("utf8"))
            else:
                LOGIN_NAME_LIST.append(data)
                client_socket.send(msgList.login_succ.encode("utf8"))
                print(LOGIN_NAME_LIST)

        else:
            break
    print("Disconnect")
    client_socket.close()


#Program starts here!
SERVER_ADDR = ("127.0.0.1", 7798)
LOGIN_NAME_LIST = []
LOGIN_POOL = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)
server_socket.listen(128)

while True:
    client_socket, client_addr = server_socket.accept()
    LOGIN_POOL.append(client_socket)
    thread = Thread(target=try_login, args=(client_socket))
    print(LOGIN_NAME_LIST)
