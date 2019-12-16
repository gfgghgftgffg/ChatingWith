# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets

        

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
        button_1.clicked.connect(self.close)
        button_2 = QtWidgets.QPushButton(self)
        button_2.setText("登录")
        button_2.move(size.width() * 1 / 5, size.height() * 4 / 5)
        button_2.clicked.connect(self.submit)
    
    def submit(self):
        pass
    
    
    
        

