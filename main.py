import socket
import sys
import threading
import json
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import client
from time import sleep

def recv_chating_msg(client_socket):
    while True:
        recv_data= client_socket.recv(1024)
        if recv_data:
            data = json.loads(recv_data.decode())
            if data['type'] == 'onlineList':
                onlineList = data['userList']
                print(onlineList)
            elif data['type'] == 'message':
                name = data['username']
                message = data['message']
                print(name, message, end='\n')

def send_chating_msg(client_socket):
    while True:
        msg_send = input("Input your msg:")#现在发送的消息不需要序列化
        client_socket.send(json.dumps(msg_send.encode()))


#Program starts here!
SERVER_ADDR = ("127.0.0.1", 7798)
NICKNAME = ""

def show_ChatWindow(a):
    sleep(1)
    CHAT_WINDOW.show()

    

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDR)

app = QtWidgets.QApplication(sys.argv)
LOGIN_WINDOW = client.loginWindow(client_socket)
LOGIN_WINDOW.show()

CHAT_WINDOW = client.loginWindow(client_socket)

LOGIN_WINDOW.login_succ_signal.connect(LOGIN_WINDOW.close)
LOGIN_WINDOW.login_succ_signal.connect(lambda a: show_ChatWindow(a))


sys.exit(app.exec_())