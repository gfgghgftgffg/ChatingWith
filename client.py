import socket
import sys
import threading
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
import window
import msgList

def login():
    username = input("Plz input ur username:")
    #password = input("Plz input ur password:")
    client_socket.send(username.encode("utf8"))
    #client_socket.send(password.encode("utf8"))
    data = client_socket.recv(1024).decode("utf8")
    if data == "1":
        return 1
    else:
        return 0

def logout():
    client_socket.close()

def recv_chating_msg(client_socket):
    while True:
        recv_data= client_socket.recv(1024)
        if recv_data:
            data = recv_data.decode("utf8")
            print(data)
        else:
            break

def send_chating_msg(client_socket):
    while True:
        msg_send = input("Input your msg:")
        client_socket.send(msg_send.encode("utf8"))


#Program starts here!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    LOGIN_WINDOW = window.loginWindow()
    LOGIN_WINDOW.show()
    sys.exit(app.exec_())

    SERVER_ADDR = ("127.0.0.1", 7798)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)
    if login():
        thread_recv_msg = threading.Thread(target=recv_chating_msg, args=([client_socket]))
        thread_send_msg = threading.Thread(target=send_chating_msg, args=([client_socket]))
        thread_recv_msg.start()
        thread_send_msg.start()

    logout()