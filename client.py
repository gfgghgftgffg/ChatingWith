import socket
import sys
import threading
import json
#from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import msgList

onlineList = []  # 在线用户列表

SERVER_ADDR = ("127.0.0.1", 7798)

class loginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatingWith")
        self.setWindowIcon(QtGui.QIcon('./Image/Icon.png'))
        #set the window size and put it on screen center
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size_width = screen.width() / 3
        window_size_height = screen.height() / 2
        self.resize(window_size_width,window_size_height)
        newLeft = (screen.width() - window_size_width) / 2
        newTop = (screen.height() - window_size_height) / 2
        self.move(newLeft,newTop)
        self.setMinimumSize(600,500)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)

        self.setupUI()
        self.setSocket()
        self.nickname = ""
    
    def setupUI(self):
        size = self.geometry()
        
        label_1 = QtWidgets.QLabel(self)
        label_1.setText("昵称")
        label_1.move(size.width() * 2 / 10, size.height() * 1 / 10)
        label_2 = QtWidgets.QLabel(self)
        label_2.setText("性别")
        label_2.move(size.width() * 2 / 10, size.height() * 2 / 10)
        label_3 = QtWidgets.QLabel(self)
        pic_size = min(size.width(),size.height()) * 2 / 5
        label_3.setPixmap(QtGui.QPixmap("./Image/Icon.png").scaled(pic_size, pic_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio))
        label_3.move(size.width() * 3 / 10, size.height() * 4 / 10)
        
        button_1 = QtWidgets.QPushButton(self)
        button_1.setText("退出")
        button_1.move(size.width() * 2 / 3, size.height() * 4 / 5)
        button_1.clicked.connect(self.close)

        self.text_nickname = QtWidgets.QLineEdit(self)
        self.text_nickname.move(size.width() * 2 / 10 + 50, size.height() * 1 / 10 - 5)
        self.text_nickname.returnPressed.connect(self.submit)
        button_2 = QtWidgets.QPushButton(self)
        button_2.setText("登录")
        button_2.move(size.width() * 1 / 5, size.height() * 4 / 5)
        #button_2.setEnabled(False)
        button_2.clicked.connect(self.submit)

        self.label_hint = QtWidgets.QLabel(self)
        self.label_hint.setText("12333")
        self.label_hint.move(size.width() * 9 / 20, size.height() * 9 / 10)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == Qt.Qt.LeftButton:
            self.move_window = True
            self.cursor_pos_1 = Qt.QCursor.pos()
            self.pos = self.geometry()
            #print(self.cursor_pos_1.x(),self.cursor_pos_1.y())
    def mouseMoveEvent(self, QMouseEvent):
        if self.move_window:   
            self.cursor_pos_2 = Qt.QCursor.pos()
            #print(self.cursor_pos_2.x(),self.cursor_pos_2.y())
            new_left = self.cursor_pos_2.x() - self.cursor_pos_1.x() + self.pos.left()
            new_top = self.cursor_pos_2.y() - self.cursor_pos_1.y() + self.pos.top()
            self.move(new_left,new_top)
    def mouseReleaseEvent(self, QMouseEvent):
        if self.move_window:
            self.move_window = False

    
    def setSocket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(SERVER_ADDR)
    
    def submit(self):
        if self.text_nickname.text() == "":
            self.label_hint.setText("Nickname can' be empty")
            return
        self.nickname = self.text_nickname.text()
        self.login()
        
    def login(self):
        if self.nickname != "":
            print("~" +self.nickname + "~")
        #password = input("Plz input ur password:")
        self.client_socket.send(self.nickname.encode("utf8"))
        #client_socket.send(password.encode("utf8"))
        data = self.client_socket.recv(1024).decode("utf8")
        if data == "1":
            print("ok")
        else:
            print("fail")

    def logout(self):
        self.client_socket.close()


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
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    LOGIN_WINDOW = loginWindow()
    LOGIN_WINDOW.show()
    sys.exit(app.exec_())
