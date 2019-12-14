import socket

#Program starts here!
SERVER_ADDR = ("127.0.0.1", 60000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)
server_socket.listen(128)

while True:
    client_socket, client_addr = server_socket.accept()

    while True:
        recv_data = client_socket.recv(1024)

        if recv_data:
            #Do something
            print(recv_data)

        else:
            break
    client_socket.close()