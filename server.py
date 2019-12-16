import socket
import threading
import msgList

def try_login(client_socket):
    client_socket.send("111".encode("utf8"))
    while True:
        recv_data = client_socket.recv(1024)

        if recv_data:
            if len(USER_POOL) >= 128:
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
USER_POOL = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)
server_socket.listen(128)

while True:
    client_socket, client_addr = server_socket.accept()
    new_thread = threading.Thread(target=try_login, args=([client_socket]))
    USER_POOL.append(new_thread)
    new_thread.start()
