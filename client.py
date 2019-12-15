import socket
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
import loginWindow
import msgList

def login():
    username = input("Plz input ur username:")
    #password = input("Plz input ur password:")
    client_socket.send(username.encode("utf8"))
    #client_socket.send(password.encode("utf8"))

    data = client_socket.recv(1024).decode("utf8")
    print(data)

def logout():
    client_socket.close()


#Program starts here!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    LOGIN_WINDOW = QMainWindow()
    loginWindow.Ui_MainWindow().setupUi(LOGIN_WINDOW)
    LOGIN_WINDOW.show()

    sys.exit(app.exec_())

    SERVER_ADDR = ("127.0.0.1", 7798)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)
    login()
    logout()