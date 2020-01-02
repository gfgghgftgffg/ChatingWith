import socket
import sys
import threading
import json
#from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import msgList
import USERWindow
import queue
import time

class loginWindow(USERWindow.loginWindow):
    login_succ_signal = Qt.pyqtSignal(str)

    def __init__(self, a_socket):
        super().__init__()
        self.nickname = ""
        self.socket = a_socket
    
    def submit(self):
        if len(self.text_nickname.text()) == 0:
            self.label_hint.setText("        昵称不能为空")
            return
        self.login()

    def login(self):
        #password = input("Plz input ur password:")
        self.socket.send(self.text_nickname.text().encode("utf8"))
        #client_socket.send(password.encode("utf8"))
        data = client_socket.recv(1024)
        data = json.loads(data.decode())
        if data['message'] == msgList.login_succ:
            self.label_hint.setText("ok")
            self.login_succ_signal.emit(self.text_nickname.text())
        elif data['message'] == msgList.err_service_full:
            self.label_hint.setText("        服务器满")
        elif data['message'] == msgList.err_existedNickName:
            self.label_hint.setText("         昵称已存在")

    def logout(self):
        self.socket.close()


class chatWindow(USERWindow.Ui_MainWindow):

    def __init__(self,mainWindow, a_socket):
        global NICKNAME
        super().setupUi(mainWindow)
        #mainWindow.setWindowFlags(Qt.Qt.FramelessWindowHint)
        mainWindow.setFixedSize(mainWindow.width(), mainWindow.height())
        self.socket = a_socket
        self.msgque = queue.Queue()
        self.lock = threading.Lock()
        self.onlineList = []
        self.listModel = QtCore.QStringListModel()
        self.listModel_2 = QtCore.QStringListModel()
        self.sender = NICKNAME
        

        self.pushButton_4.clicked.connect(mainWindow.close)
        self.pushButton_4.clicked.connect(self.socket.close)
        self.pushButton_3.clicked.connect(self.send_chating_msg)
        self.pushButton_2.clicked.connect(self.uploadFiles)
        self.pushButton_5.clicked.connect(self.flushDownloadFiles)
        self.pushButton.clicked.connect(self.send_chating_pic)

        self.listView_2.doubleClicked.connect(self.downloadFiles)
        
    
    def run(self,nickname):
        self.sender = nickname
        self.thread_recv_msg = threading.Thread(target=self.recv_chating_msg)
        self.thread_recv_msg.start()
        self.listView.setModel(self.listModel)
        self.listView_2.setModel(self.listModel_2)

        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.listView_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    
    def send_chating_msg(self):
        tolist = []
        for i in self.listView.selectedIndexes():
            tolist.append(i.data())
        if len(tolist) == 0:
            totype = 'USER_MSG_ALL'
        else:
            totype = 'USER_MSG_PRI'

        data = {}
        send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        data = {'type':totype,'message':self.textEdit.toPlainText(),'sender':self.sender,'send_time':send_time,'tolist':tolist}
        self.socket.send(json.dumps(data).encode())
        self.textEdit.clear()


    def send_chating_pic(self):

        tolist = []
        for i in self.listView.selectedIndexes():
            tolist.append(i.data())
        if len(tolist) == 0:
            totype = 'USER_PIC_ALL'
        else:
            totype = 'USER_PIC_PRI'

        data = {}
        send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        imgName, imgType = QtWidgets.QFileDialog.getOpenFileName(None, "选择图片", "", "*.jpg;;*.png;;All Files(*)")

        with open(imgName, 'rb') as f:
            bytes = f.read()
        data = {'type':totype,'sender':self.sender,'send_time':send_time,'tolist':tolist}
        self.socket.send(json.dumps(data).encode())

        self.socket.sendall(bytes)
        


    def recv_chating_msg(self):
        while True:
            recv_data= self.socket.recv(1024)
            if recv_data:
                self.lock.acquire()
                try:
                    data = json.loads(recv_data.decode())
                    if data['type'] == 'onlineList':
                        self.onlineList = data['message']
                        self.listModel.setStringList(self.onlineList)
                        #self.listView.setModel(self.listModel)
                    elif data['type'] == 'fileList':
                        self.fileList = data['message']
                        self.listModel_2.setStringList(self.fileList)
                        
                    elif data['type'] == 'USER_MSG':
                        self.textBrowser.append(data['sender'] + ' (' + data['send_time'] + ')')
                        self.textBrowser.append(data['message'] + '\n')

                    elif data['type'] == 'USER_PIC':
                        self.textBrowser.append(data['sender'] + ' (' + data['send_time'] + ')')
                        self.textBrowser.append('<img src=%s>' % data['message'])
                        self.textBrowser.append('\n')
                finally:
                    self.lock.release()


    
    def uploadFiles(self):

        file_port = 22333
        file_tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_tmp_socket.connect(("127.0.0.1", file_port))
        
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        file_dialog.setFilter(QtCore.QDir.Files)

        if file_dialog.exec_():
            filename = file_dialog.selectedFiles()
            name = filename[0].split('/')[-1]

            data = {'type':'UPLOAD','message':name}
            file_tmp_socket.send(json.dumps(data).encode())
            with open(filename[0], 'rb') as f:
                while True:
                    a = f.read(1024)
                    if not a:
                        break
                    file_tmp_socket.send(a)
                time.sleep(0.1)
                file_tmp_socket.send('EOF'.encode())
        file_tmp_socket.close()


    def downloadFiles(self,index):

        file_port = 22333
        file_tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_tmp_socket.connect(("127.0.0.1", file_port))

        
        download_file_name = self.fileList[index.row()]
        download_path = QtWidgets.QFileDialog.getExistingDirectory(None,"Download To","C:/")
        download_full_path = download_path + "\\" + download_file_name
        if(download_file_name):
            data = {'type':'DOWNLOAD','message':download_file_name}
            file_tmp_socket.send(json.dumps(data).encode())
            with open(download_full_path, 'wb') as f:
                while True:
                    data = file_tmp_socket.recv(1024)
                    if data == 'EOF'.encode():
                        break
                    f.write(data)
        file_tmp_socket.close()
    
    def flushDownloadFiles(self):
        data = {'type':'NEW_FILE_LIST','message':''}
        self.socket.send(json.dumps(data).encode())

    



if __name__ == '__main__':
    SERVER_ADDR = ("127.0.0.1", 7799)
    NICKNAME = ""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)
    

    app = QtWidgets.QApplication(sys.argv)
    LOGIN_WINDOW = loginWindow(client_socket)
    
    CHAT_WINDOW = QtWidgets.QMainWindow()
    ui = chatWindow(CHAT_WINDOW, client_socket)

    LOGIN_WINDOW.login_succ_signal.connect(LOGIN_WINDOW.close)
    LOGIN_WINDOW.login_succ_signal.connect(CHAT_WINDOW.show)
    LOGIN_WINDOW.login_succ_signal.connect(lambda nickname:ui.run(nickname))
    LOGIN_WINDOW.show()
    sys.exit(app.exec_())
