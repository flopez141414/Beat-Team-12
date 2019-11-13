import json
import r2pipe
import sys

#XML libraries
import xml.etree.ElementTree as ET
import xmltodict
import pprint
import json

sys.path.append("../DB")
sys.path.append("../windows")
import xmlUploader
import errorMessageGnerator
# from xmlUploader import uploadXml

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QPushButton, QLabel, QGridLayout, QTextEdit, \
    QLineEdit, QListWidget, QFileDialog, QMessageBox

#Global Variables to Save Project
projectNameHolder = ''
projectDescHolder = ''
projectPathHolder = ''
fileProperties = []

projectSelected = False

#sscess finished with exit code 0

class ProjectTab(QWidget):
    def __init__(self):
        super().__init__()

        global projectNameHolder
        global projectDescHolder
        global projectPathHolder

        mainlayout = QGridLayout()
        leftLayout = QGridLayout()
        rightLayout = QGridLayout()
        mainlayout.addLayout(leftLayout, 1, 0, 6, 1)
        mainlayout.addLayout(rightLayout, 1, 1, 6, 5)

        # Left panel
        searchBox = QLineEdit()
        searchButton = QPushButton('Search')
        newButton = QPushButton('New')
        self.searchList = QListWidget()
        leftPanelLabel = QLabel('Project View')
        leftPanelLabel.setAlignment(Qt.AlignCenter)

        leftLayout.addWidget(leftPanelLabel, 0, 0, 1, 4)
        leftLayout.addWidget(searchBox, 1, 0, 1, 3)
        leftLayout.addWidget(searchButton, 1, 3, 1, 1)
        leftLayout.addWidget(self.searchList, 2, 0, 1, 4)

        leftLayout.addWidget(newButton, 6, 0)

        # Right panel
        rightPanelLabel = QLabel('Detailed Project View')
        rightPanelLabel.setAlignment(Qt.AlignCenter)
        self.projNameArea = QTextEdit()
        projectNameHolder = self.projNameArea # storing global
        self.projDescriptionArea = QTextEdit()
        projectDescHolder = self.projDescriptionArea
        self.binaryFilePath = QTextEdit()
        projectPathHolder = self.binaryFilePath
        self.binaryFileProp = QTableWidget()
        self.binaryFileProp.horizontalHeader().setStretchLastSection(True)
        self.binaryFileProp.verticalHeader().setVisible(False)
        self.binaryFileProp.horizontalHeader().setVisible(False)
        self.binaryFileProp.setAlternatingRowColors(True)
        self.browseButton = QPushButton('Browse')
        self.browseButton.clicked.connect(self.OpenFile)

        rightLayout.addWidget(rightPanelLabel, 0, 0, 1, 14)
        rightLayout.addWidget(self.projNameArea, 1, 2, 10, 10)
        rightLayout.addWidget(self.projDescriptionArea, 2, 2, 5, 10)
        rightLayout.addWidget(self.binaryFilePath, 4, 2, 10, 10)
        rightLayout.addWidget(self.binaryFileProp, 6, 2, 8, 10)
        rightLayout.addWidget(self.browseButton, 4, 12)

        rightLayout.addWidget(QLabel('Project Name'), 1, 1, 1, 1)
        rightLayout.addWidget(QLabel('Project Description'), 2, 1, 1, 1)
        rightLayout.addWidget(QLabel('Binary File Path'), 5, 1, 1, 1)
        rightLayout.addWidget(QLabel('Binary File Properties'), 6, 1, 1, 1)

        self.deleteButton = QPushButton('Delete')

        saveButton = QPushButton('Save')

        saveButton.clicked.connect(self.saveFile)

        newButton.clicked.connect(self.createNew)

        rightLayout.addWidget(saveButton, 15, 8)
        rightLayout.addWidget(self.deleteButton, 15, 1)

        self.deleteButton.clicked.connect(self.deleteProject)
        self.setLayout(mainlayout)

        self.binaryFileProp.setRowCount(13)
        self.binaryFileProp.setColumnCount(2)
        self.binaryFileProp.setItem(0, 0, QTableWidgetItem("OS"))
        self.binaryFileProp.setItem(1, 0, QTableWidgetItem("Binary Type"))
        self.binaryFileProp.setItem(2, 0, QTableWidgetItem("Machine"))
        self.binaryFileProp.setItem(3, 0, QTableWidgetItem("Class"))
        self.binaryFileProp.setItem(4, 0, QTableWidgetItem("Bits"))
        self.binaryFileProp.setItem(5, 0, QTableWidgetItem("Language"))
        self.binaryFileProp.setItem(6, 0, QTableWidgetItem("Canary"))
        self.binaryFileProp.setItem(7, 0, QTableWidgetItem("Crypto"))
        self.binaryFileProp.setItem(8, 0, QTableWidgetItem("Nx"))
        self.binaryFileProp.setItem(9, 0, QTableWidgetItem("Pic"))
        self.binaryFileProp.setItem(10, 0, QTableWidgetItem("Relocs"))
        self.binaryFileProp.setItem(11, 0, QTableWidgetItem("Relro"))
        self.binaryFileProp.setItem(12, 0, QTableWidgetItem("Stripped"))
        self.binaryFileProp.setEnabled(False)
        #self.binaryFileProp.doubleClicked.connect(self.on_click)
        self.searchList.doubleClicked.connect(self.select_project)
        self.searchList.doubleClicked.connect(self.disableEditing)

        projectList = xmlUploader.retrieve_list_of_projects()
        for item in projectList:
            self.searchList.addItem(item)

    def disableEditing(self):
        self.browseButton.setEnabled(False)
        self.projNameArea.setEnabled(False)
        self.binaryFilePath.setEnabled(False)
        self.binaryFileProp.setEnabled(False)

    def staticAnalysis(self, filename):
        global fileProperties
        binPropertiesList = ["os", "bintype", "machine", "class", "bits", "lang", "canary", "crypto", "nx", "pic", "relocs",
                             "relro", "stripped"]
        rlocal = r2pipe.open(filename)
        colNum = 0
        binInfo = rlocal.cmd('iI').splitlines()
        for item in binPropertiesList:
            matchingline = [s for s in binInfo if item in s]
            a = matchingline[0].split()
            fileProperties.append(a[1])
            self.binaryFileProp.setItem(colNum, 1, QTableWidgetItem(a[1]))
            colNum += 1
        self.updateProjectList()

    # global.py
    myFileName = ""
    def OpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.binaryFilePath.setText(fileName)
            self.staticAnalysis(fileName)
            #             self.myFilename = fileName
            global myFileName
            myFileName = fileName
            return fileName
        self.updateProjectList()
        return "not found"

    def getFileName(self):
        return self.myFilename

    def saveFile(self):
        global projectNameHolder
        global projectDescHolder
        global projectPathHolder
        global projectSelected

        pname = projectNameHolder.toPlainText()
        pdesc = projectDescHolder.toPlainText()
        ppath = projectPathHolder.toPlainText()

        if pname != "" and pdesc != "" and ppath != "":
            # Adding to XMl
            tree = ET.parse('../xml/Project.xml')
            root = tree.getroot()
            b2tf = root.find("./Project_name")
            b2tf.text = pname
            b2tf = root.find("./projectDescription")
            b2tf.text = pdesc
            b2tf = root.find("./BinaryFilePath")
            b2tf.text = ppath
            b2tf = root.find("./StaticDataSet/OS")
            b2tf.text = fileProperties[0]
            b2tf = root.find("./StaticDataSet/BinaryType")
            b2tf.text = fileProperties[1]
            b2tf = root.find("./StaticDataSet/Machine")
            b2tf.text = fileProperties[2]
            b2tf = root.find("./StaticDataSet/Class")
            b2tf.text = fileProperties[3]
            b2tf = root.find("./StaticDataSet/Bits")
            b2tf.text = fileProperties[4]
            b2tf = root.find("./StaticDataSet/Language")
            b2tf.text = fileProperties[5]
            b2tf = root.find("./StaticDataSet/Canary")
            b2tf.text = fileProperties[6]
            b2tf = root.find("./StaticDataSet/Crypto")
            b2tf.text = fileProperties[7]
            b2tf = root.find("./StaticDataSet/NX")
            b2tf.text = fileProperties[8]
            b2tf = root.find("./StaticDataSet/Pic")
            b2tf.text = fileProperties[9]
            b2tf = root.find("./StaticDataSet/Relocs")
            b2tf.text = fileProperties[10]
            b2tf = root.find("./StaticDataSet/Relro")
            b2tf.text = fileProperties[11]
            b2tf = root.find("./StaticDataSet/Stripped")
            b2tf.text = fileProperties[12]
            my_dict = ET.tostring(root, encoding='utf8').decode('utf8')
            xmlUploader.uploadXML(my_dict)
            self.disableEditing()
        elif pname == "":
            errorMessageGnerator.showDialog("Enter a project name", "Project Name Error")
        elif pdesc == "":
            errorMessageGnerator.showDialog("Enter a description for the project","Project File Error")
        elif ppath == "":
            errorMessageGnerator.showDialog("Cannot create a project without a binary file","Binary File Error")
        self.updateProjectList()


    def select_project(self):
        project = [item.text() for item in self.searchList.selectedItems()]
        projectName = ' '.join([str(elem) for elem in project])
        project = xmlUploader.retrieve_selected_project(projectName)

        self.projNameArea.setText(project['Project']['Project_name']['#text'])
        self.projDescriptionArea.setText(project['Project']['projectDescription']['#text'])
        self.binaryFilePath.setText(project['Project']['BinaryFilePath']['#text'])
        self.binaryFileProp.setItem(0, 1, QTableWidgetItem(project['Project']['StaticDataSet']['OS']))
        self.binaryFileProp.setItem(1, 1, QTableWidgetItem(project['Project']['StaticDataSet']['BinaryType']))
        self.binaryFileProp.setItem(2, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Machine']))
        self.binaryFileProp.setItem(3, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Class']))
        self.binaryFileProp.setItem(4, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Bits']))
        self.binaryFileProp.setItem(5, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Language']))
        self.binaryFileProp.setItem(6, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Canary']))
        self.binaryFileProp.setItem(7, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Crypto']))
        self.binaryFileProp.setItem(8, 1, QTableWidgetItem(project['Project']['StaticDataSet']['NX']))
        self.binaryFileProp.setItem(9, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Pic']))
        self.binaryFileProp.setItem(10, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Relocs']))
        self.binaryFileProp.setItem(11, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Relro']))
        self.binaryFileProp.setItem(12, 1, QTableWidgetItem(project['Project']['StaticDataSet']['Stripped']))
        self.updateProjectList()


    def createNew(self):
        self.projDescriptionArea.clear()
        self.projNameArea.clear()
        self.binaryFilePath.clear()
        self.binaryFileProp.setItem(0, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(1, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(2, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(3, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(4, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(5, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(6, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(7, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(8, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(9, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(10, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(11, 1, QTableWidgetItem(""))
        self.binaryFileProp.setItem(12, 1, QTableWidgetItem(""))
        self.browseButton.setEnabled(True)
        self.projNameArea.setEnabled(True)
        self.binaryFilePath.setEnabled(True)
        self.binaryFileProp.setEnabled(True)
        self.updateProjectList()
        #self.deleteButton.setEnabled(False)


    def deleteProject(self):
        global projectNameHolder
        toErase = projectNameHolder.toPlainText()
        if not toErase:
            errorMessageGnerator.showDialog("Please select a project to delete")
        xmlUploader.delete_selected_project(toErase)
        for item in self.searchList.selectedItems():
            self.searchList.takeItem(self.searchList.row(item))
        self.updateProjectList()
        self.createNew()

    def updateProjectList(self):
        self.searchList.clear()
        projectList = xmlUploader.retrieve_list_of_projects()
        for item in projectList:
            self.searchList.addItem(item)


