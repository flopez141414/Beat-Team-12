import sys

import r2pipe
import pymongo
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLabel, QFileDialog, QSplitter, \
    QHBoxLayout, QFrame, QGridLayout, QTabWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QListWidget, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore
from PyQt5.uic.properties import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets

from CommentView import Ui_Dialog as comment_window
from AnalysisResultView import Ui_Dialog as analysis_window
from OutputFieldView import Ui_Dialog as output_Field_Window


class AnalysisTab(QWidget):
    
    def __init__(self):
        super().__init__()
        stringsPOI=[]
        functionsPOI=[]
        variablesPOI=[]
        dllsPOI=[]
        structuresPOI=[]
        
        mainlayout = QGridLayout()
        leftLayout = QGridLayout()
        rightLayout = QGridLayout()
        topLayout = QGridLayout()
        mainlayout.addLayout(topLayout, 0, 0, 1, 6)
        mainlayout.addLayout(leftLayout, 1, 0, 6, 1)
        mainlayout.addLayout(rightLayout, 1, 1, 6, 5)

        # Top layout elements
        pluginDropdown = QComboBox()
        runStatic = QPushButton('Run')
        self.poiDropdown = QComboBox()
        runDynamic = QPushButton('Run')
        self.stopDynamic = QPushButton('Stop')

        self.stopDynamic.setEnabled(False)

        topLayout.addWidget(QLabel('Plugin'), 0, 0)
        topLayout.addWidget(pluginDropdown, 0, 1, 1, 2)
        topLayout.addWidget(QLabel('Static Analysis'), 1, 0)
        topLayout.addWidget(runStatic, 1, 1, 1, 1)
        topLayout.addWidget(QLabel('Point of Interest Type'), 2, 0)
        topLayout.addWidget(self.poiDropdown, 2, 1, 1, 2)
        topLayout.addWidget(QLabel('Dynamic Analysis'), 1, 5, 1, 1)
        topLayout.addWidget(runDynamic, 1, 6)
        topLayout.addWidget(self.stopDynamic, 1, 7)
        topLayout.addWidget(QLabel(), 0, 3, 1, 15)

        # Left panel
        searchBox = QLineEdit()
        searchButton = QPushButton('Search')

        self.poiList = QListWidget()
        leftPanelLabel = QLabel('Point of Interest View')
        leftPanelLabel.setAlignment(Qt.AlignCenter)

        leftLayout.addWidget(leftPanelLabel, 0, 0, 1, 4)
        leftLayout.addWidget(searchBox, 1, 0, 1, 3)
        leftLayout.addWidget(searchButton, 1, 3, 1, 1)
        leftLayout.addWidget(self.poiList, 2, 0, 1, 4)

        # Right panel
        rightPanelLabel = QLabel('Point of Interest View')
        rightPanelLabel.setAlignment(Qt.AlignCenter)
        self.poiContentArea = QTextEdit()
        self.terminal = QTextEdit()
        self.commentButton = QPushButton('Comments')
        self.outputButton = QPushButton('Output')
        self.analysisButton = QPushButton('Analysis')

        rightLayout.addWidget(rightPanelLabel, 0, 0, 1, 10)
        rightLayout.addWidget(self.poiContentArea, 1, 0, 10, 8)
        rightLayout.addWidget(self.terminal, 11, 0, 10, 8)
        rightLayout.addWidget(self.analysisButton, 1, 9)
        rightLayout.addWidget(self.outputButton, 2, 9)
        rightLayout.addWidget(self.commentButton, 2, 8)

        #Functionality
        self.commentButton.clicked.connect(self.openCommentWindow)
        self.analysisButton.clicked.connect(self.openAnalysisWindow)
        self.outputButton.clicked.connect(self.openOutputWindow)

        #set Plugin name
        pluginDropdown.addItem("Select Plugin")
        pluginDropdown.addItem("Network Plugin")
        pluginDropdown.addItem("dummy")
        pluginDropdown.activated[str].connect(self.onActivated)


        self.poiDropdown.activated[str].connect(self.displayPOI)
        runStatic.clicked.connect(self.clickStaticAnalysis)
        self.setLayout(mainlayout)
    def displayPOI(self,option):
        if option=="Strings":
            self.poiList.clear()
            for item in stringsPOI:
                item2=item.split()
                self.poiList.addItem(item2[2])
            #self.poiContentArea.setText(stringsPOI)
        elif option == "Variables":
            self.poiList.clear()
            #for item in variablesPOI:
             #   self.poiList.addItem(item)
            #self.poiContentArea.setText(variablesPOI)
        elif option == "Functions":
            self.poiList.clear()
            for item in functionsPOI:
                item2=item.split()
                if item2[3]=="->":
                    self.poiList.addItem(item2[5])
                else:
                    self.poiList.addItem(item2[3])
            #self.poiContentArea.setText(functionsPOI)
        elif option == "Structures":
            self.poiList.clear()
            #for item in structuresPOI:
             #   self.poiList.addItem(item)
            #self.poiContentArea.setText(structuresPOI)
        elif option == "Dlls":
            self.poiList.clear()
            for item in dllsPOI:
                self.poiList.addItem(item)
            #self.poiContentArea.setText(dllsPOI)
    def onActivated(self,option):
        if option == "Network Plugin":
            self.poiDropdown.clear()
            self.poiDropdown.addItem("Select POI to display")
            self.poiDropdown.addItem("Strings")
            self.poiDropdown.addItem("Functions")
            self.poiDropdown.addItem("Variables")
            self.poiDropdown.addItem("Dlls")
            self.poiDropdown.addItem("Structures")
        elif option == "dummy":
            self.poiDropdown.clear()
            self.poiDropdown.addItem("opps")
    def clickStaticAnalysis(self):
        bina=r2pipe.open("ping.exe")
        self.terminal.setText("Running Static Analysis..")
        global stringsPOI
        global variablesPOI
        global functionsPOI
        global dllsPOI
        global structuresPOI
        stringsPOI =bina.cmd("f;~str.").splitlines()
        dllsPOI = bina.cmd("ii").splitlines()
        functionsPOI = bina.cmd("aaa;afl").splitlines()
        #structuresPOI = bina.cmd("").splitlines()
        #variablesPOI = bina.cmd("").splitlines()
        self.terminal.append("Static Analysis done!")


# Methods to open windows
    def openCommentWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = comment_window()
        self.ui.setupUi(self.window)
        self.window.show()

    def openAnalysisWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = analysis_window()
        self.ui.setupUi(self.window)
        self.window.show()

    def openOutputWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = output_Field_Window()
        self.ui.setupUi(self.window)
        self.window.show()
