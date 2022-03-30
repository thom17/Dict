import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("PyQtUi.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self, li : []) :
        super().__init__()
        self.setupUi(self)
        print(type(self.layout()))


        #btBox.bt_addWord.clicked.connect(self.adWord)
#        self.bt

    def addWord(self):
        print("add Word")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass(["test"])
    myWindow.show()
    app.exec_()