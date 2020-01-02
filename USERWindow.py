from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class loginWindow(QtWidgets.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
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

        self.text_nickname = QtWidgets.QLineEdit(self)
        self.text_nickname.move(size.width() * 2 / 10 + 50, size.height() * 1 / 10 - 5)
        self.text_nickname.returnPressed.connect(self.submit)
        button_2 = QtWidgets.QPushButton(self)
        button_2.setText("登录")
        button_2.move(size.width() * 1 / 5, size.height() * 4 / 5)
        #button_2.setEnabled(False)

        self.label_hint = QtWidgets.QLabel(self)
        self.label_hint.setText("12333")
        self.label_hint.move(size.width() * 9 / 20, size.height() * 9 / 10)

        button_1.clicked.connect(self.close)
        button_2.clicked.connect(self.submit)

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



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1319, 868)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 590, 811, 161))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 560, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 560, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(860, 20, 201, 771))
        self.listView.setObjectName("listView")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 811, 531))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(740, 760, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(630, 760, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(260, 560, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.listView_2 = QtWidgets.QListView(self.centralwidget)
        self.listView_2.setGeometry(QtCore.QRect(1080, 20, 221, 771))
        self.listView_2.setObjectName("listView_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1319, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "聊天室"))
        self.pushButton.setText(_translate("MainWindow", "发送图片"))
        self.pushButton_2.setText(_translate("MainWindow", "上传文件"))
        self.pushButton_3.setText(_translate("MainWindow", "发送"))
        self.pushButton_4.setText(_translate("MainWindow", "关闭"))
        self.pushButton_5.setText(_translate("MainWindow", "下载文件"))

