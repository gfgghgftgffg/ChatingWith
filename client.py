import socket
import sys
import threading
import json
#from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import msgList
import USERWindow

class loginWindow(USERWindow.loginWindow):
    login_succ_signal = Qt.pyqtSignal(str)

    def __init__(self, a_socket):
        super().__init__()
        self.nickname = ""
        self.socket = a_socket
    
    def submit(self):
        if len(self.text_nickname.text()) == 0:
            self.label_hint.setText("昵称不能为空")
            return
        self.login()
        print("return s")

    def login(self):
        #password = input("Plz input ur password:")
        self.socket.send(self.text_nickname.text().encode("utf8"))
        #client_socket.send(password.encode("utf8"))
        data = client_socket.recv(1024)
        data = json.loads(data.decode())
        print("recv",data)
        if data['message'] == msgList.login_succ:
            self.label_hint.setText("ok")
            self.login_succ_signal.emit(self.text_nickname.text())
        elif data['message'] == msgList.err_service_full:
            self.label_hint.setText("服务器满")
        elif data['message'] == msgList.err_existedNickName:
            self.label_hint.setText("昵称已存在")

    def logout(self):
        self.socket.close()


#Program starts here!
SERVER_ADDR = ("127.0.0.1", 7798)
NICKNAME = ""

    


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)

    app = QtWidgets.QApplication(sys.argv)
    LOGIN_WINDOW = loginWindow(client_socket)
    CHAT_WINDOW = QtWidgets.QMainWindow()
    LOGIN_WINDOW.login_succ_signal.connect(LOGIN_WINDOW.close)
    LOGIN_WINDOW.login_succ_signal.connect(CHAT_WINDOW.show)
    LOGIN_WINDOW.show()
    sys.exit(app.exec_())

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

    # thread_recv_msg = threading.Thread(target=recv_chating_msg, args=([client_socket]))
    # thread_send_msg = threading.Thread(target=send_chating_msg, args=([client_socket]))
    # thread_recv_msg.start()
    # thread_send_msg.start()