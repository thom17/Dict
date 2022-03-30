import sys
import PyQt5.QtWidgets as qt
#from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(qt.QWidget):
    buttonlist = ("단어 추가", "CSV 읽기", "DB 관리", "시험 보기")
    buttonDict = {buttonlist[0]:"addButton", buttonlist[1] : "readCSV" ,buttonlist[2] :"dbManager", buttonlist[3]:"exam"}
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dict Program')
        self.move(250, 200)
        self.resize(1024, 560)
        self.show()
        self.mainLayOut = qt.QHBoxLayout()
        self.setLayout(self.mainLayOut)
        self.mainLayOut.addWidget(qt.QLabel("0, 0"))
        self.mainLayOut.addWidget(ButtonBox(list(MyApp.buttonlist)))

class ButtonBox(qt.QGroupBox):
    def __init__(self, buttonlist : list):
        qt.QGroupBox.__init__(self)
        layout = qt.QVBoxLayout()
        self.setLayout(layout)
        self.buttonList = []
        self.buttonActList = [self.addWord, self.readCSV, self.dbManager, self.exam]
        for buttonName in buttonlist:
            bt = qt.QPushButton(buttonName)
            layout.addWidget(bt)
            bt.clicked.connect(self.buttonActList[len(self.buttonList)])
            self.buttonList.append(bt)

        #self.show()

    def addWord(self):
        print("add Word")
    def readCSV(self):
        print("read CSV")
    def dbManager(self):
        print("db")
    def exam(self):
        print("exam")





if __name__ == '__main__':
   app = qt.QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())