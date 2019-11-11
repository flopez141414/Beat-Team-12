import sys
import r2pipe
import pymongo
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLabel, QFileDialog, QSplitter, \
    QHBoxLayout, QFrame, QGridLayout, QTabWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QListWidget, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore, QtGui
import xmlUploader


class PluginManagementTab(QWidget):
    def __init__(self):
        super().__init__()

        mainlayout = QGridLayout()
        leftLayout = QGridLayout()
        self.rightLayout = QGridLayout()
        mainlayout.addLayout(leftLayout, 1, 0, 6, 1)
        mainlayout.addLayout(self.rightLayout, 1, 1, 6, 5)

        # Left panel
        searchBox = QLineEdit()
        searchButton = QPushButton('Search')
        newButton = QPushButton('New')
        self.searchList = QListWidget()
        leftPanelLabel = QLabel('Plugin View')
        leftPanelLabel.setAlignment(Qt.AlignCenter)
#         leftPanelLabel.setStyleSheet("background-color: rgba(173,216,230 ,1 )")
        leftPanelLabel.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont().Bold))

        leftLayout.addWidget(leftPanelLabel, 0, 0, 1, 5)
        leftLayout.addWidget(searchBox, 1, 0, 1, 3)
        leftLayout.addWidget(searchButton, 1, 4, 1, 1)
        leftLayout.addWidget(self.searchList, 2, 0, 1, 5)
        leftLayout.addWidget(newButton, 6, 0)

        # Right panel
        self.rightPanelLabel = QLabel('Detailed Plugin View')
        self.rightPanelLabel.setAlignment(Qt.AlignCenter)
#         rightPanelLabel.setStyleSheet("background-color: rgba(173,216,230 ,1 )")
        self.rightPanelLabel.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont().Bold))
        self.pluginStructArea = QTextEdit()
        self.pluginDataSet = QTextEdit()
        self.pluginName = QTextEdit()
        self.pluginDesc = QTextEdit()
        self.pointsOI = QTextEdit()
        self.defaultOutDropdown = QComboBox()
        self.browseButton1 = QPushButton('Browse')
        self.browseButton2 = QPushButton('Browse')
        newButton.clicked.connect(self.createNew)
      #  self.browseButton1.clicked.connect(self.clickEvent)
        self.deleteButton = QPushButton('Delete')
        self.saveButton = QPushButton('Save')
        button = QPushButton("My Button")
       # button.clicked.connect(self.clickEvent)
        self.setLayout(mainlayout)

        self.searchList.doubleClicked.connect(self.select_project)
        #self.searchList.doubleClicked.connect(self.disableEditing)

        #retrieve plugin titles and display on list
        projectList = xmlUploader.retrieve_list_of_projects()
        for item in projectList:
            self.searchList.addItem(item)

    def loadRightLayout(self):
        self.rightLayout.addWidget(self.browseButton1, 1, 6)
        self.rightLayout.addWidget(self.browseButton2, 2, 6)
        self.rightLayout.addWidget(self.rightPanelLabel, 0, 0, 1, 10)
        self.rightLayout.addWidget(self.pluginStructArea, 1, 2, 2, 1)
        self.rightLayout.addWidget(self.pluginDataSet, 2, 2, 2, 1)
        self.rightLayout.addWidget(self.pluginName, 3, 2, 2, 1)
        self.rightLayout.addWidget(self.pluginDesc, 4, 2, 2, 1)
        self.rightLayout.addWidget(self.defaultOutDropdown, 5, 2, 1, 1)
        self.rightLayout.addWidget(self.pointsOI, 6, 2, 4, 1)

        self.rightLayout.addWidget(QLabel('Plugin Structure'), 1, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Plugin Predefined Data Set'), 2, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Plugin Name'), 3, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Plugin Description'), 4, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Default Output Field'), 5, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Points of Interest'), 6, 1, 1, 1)
        self.rightLayout.addWidget(self.saveButton, 15, 7)
        self.rightLayout.addWidget(self.deleteButton, 15, 1)
        self.browseButton1.clicked.connect(self.OpenFile)
        self.browseButton2.clicked.connect(self.OpenFile)

    def select_project(self):
        #for this mode we will load the right layout
        print('mama mia')
        self.loadRightLayout()

        project = [item.text() for item in self.searchList.selectedItems()]
        projectName = ' '.join([str(elem) for elem in project])
        project = xmlUploader.retrieve_selected_project(projectName)

    myFileName = ""
    def OpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            #self.binaryFilePath.setText(fileName)
            #self.staticAnalysis(fileName)

            global myFileName
            myFileName = fileName
            return fileName
        #self.updateProjectList()
        return "not found"


    def createNew(self):
        self.loadRightLayout()
        self.deleteButton.hide()

    def clickEvent(self):
        print("Clicked")

    def savexml(self):
        print('saving xml')