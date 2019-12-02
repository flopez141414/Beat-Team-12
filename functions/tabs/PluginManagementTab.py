import sys
import r2pipe
import pymongo
import xmlUploader
import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import json
import xmltodict
import pprint
import urllib
import os.path

sys.path.append("../DB")
sys.path.append("../windows")

import errorMessageGnerator

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QPushButton, QLabel, QGridLayout, QTextEdit, \
    QLineEdit, QListWidget, QFileDialog, QMessageBox, QComboBox

# Global Vars
xml1 = []
xml2 = []
nameH = ""
descH = ""
structH = ""
pdatasetH = ""
listCounter = 0


class PluginManagementTab(QWidget):
    def __init__(self):
        super().__init__()

        global nameH
        global descH
        global structH
        global pdatasetH

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
        leftPanelLabel.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont().Bold))

        leftLayout.addWidget(leftPanelLabel, 0, 0, 1, 5)
        leftLayout.addWidget(searchBox, 1, 0, 1, 3)
        leftLayout.addWidget(searchButton, 1, 4, 1, 1)
        leftLayout.addWidget(self.searchList, 2, 0, 1, 5)
        leftLayout.addWidget(newButton, 6, 0)

        # Right panel
        self.rightPanelLabel = QLabel('Detailed Plugin View')
        self.rightPanelLabel.setAlignment(Qt.AlignCenter)
        self.rightPanelLabel.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont().Bold))
        self.pluginStructArea = QTextEdit()
        structH = self.pluginStructArea
        self.pluginDataSet = QTextEdit()
        pdatasetH = self.pluginDataSet
        self.pluginName = QTextEdit()
        nameH = self.pluginName
        self.pluginDesc = QTextEdit()
        descH = self.pluginDesc
        self.pointsOI = QListWidget()
        self.browseButton1 = QPushButton('Browse')
        self.browseButton2 = QPushButton('Browse')
        newButton.clicked.connect(self.createNew)
        self.deleteButton = QPushButton('Delete')
        self.saveButton = QPushButton('Save')
        button = QPushButton("My Button")
        self.setLayout(mainlayout)

        self.searchList.doubleClicked.connect(self.select_plugin)
        self.searchList.doubleClicked.connect(self.disableEditing)

        # retrieve plugin titles and display on list
        pluginList = xmlUploader.retrieve_list_of_plugin()
        for item in pluginList:
            self.searchList.addItem(item)

    def loadRightLayout(self):
        self.rightLayout.addWidget(self.browseButton1, 1, 6)
        self.rightLayout.addWidget(self.browseButton2, 2, 6)
        self.rightLayout.addWidget(self.rightPanelLabel, 0, 0, 1, 10)
        self.rightLayout.addWidget(self.pluginStructArea, 1, 2, 2, 1)
        self.rightLayout.addWidget(self.pluginDataSet, 2, 2, 2, 1)
        self.rightLayout.addWidget(self.pluginName, 3, 2, 2, 1)
        self.rightLayout.addWidget(self.pluginDesc, 4, 2, 2, 1)
        # self.rightLayout.addWidget(self.defaultOutDropdowndefaultOutDropdown, 5, 2, 1, 1)
        self.rightLayout.addWidget(self.pointsOI, 5, 2, 4, 1)

        self.rightLayout.addWidget(QLabel('Plugin Structure'), 1, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Plugin Predefined Data Set'), 2, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Plugin Name'), 3, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Plugin Description'), 4, 1, 1, 1)
        # self.rightLayout.addWidget(QLabel('Default Output Field'), 5, 1, 1, 1)
        self.rightLayout.addWidget(QLabel('Points of Interest'), 5, 1, 1, 1)
        self.rightLayout.addWidget(self.saveButton, 15, 7)
        self.rightLayout.addWidget(self.deleteButton, 15, 1)
        self.browseButton1.clicked.connect(self.browse1)
        self.browseButton2.clicked.connect(self.browse2)
        self.saveButton.clicked.connect(self.savexml)
        self.deleteButton.clicked.connect(self.deletePluggin)

    # aids in opening a file. Tells which button was clicked
    def browse1(self):
        self.openFile(1)

    def browse2(self):
        self.openFile(2)

    def select_plugin(self):
        global nameH
        self.loadRightLayout()
        self.deleteButton.show()
        self.browseButton1.hide()
        self.browseButton2.hide()
        self.saveButton.hide()

        plugins = [item.text() for item in self.searchList.selectedItems()]
        pluginName = ' '.join([str(elem) for elem in plugins])

        #get list from db
        plugin = xmlUploader.retrieve_selected_plugin(pluginName)

        print('*******')
        self.pluginName.setText(plugin['Plugin']['Plugin_name']['#text'])
        self.pluginDesc.setText(plugin['Plugin']['Plugin_Desc']['#text'])
        self.pluginStructArea.setText(plugin['Plugin']['structure_path']['#text'])
        self.pluginDataSet.setText(plugin['Plugin']['predefined_dataset_path']['#text'])
        list_of_poi = self.update_poi_list(plugin)
        self.updatePluginList()
        for item in list_of_poi:
            self.pointsOI.addItem(item)

    # checks which browse button was clicked. Sends address and button number
    myFileName = ""

    def openFile(self, caller):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            if caller == 1:
                self.pluginStructArea.setText(fileName)
                self.pluginxmlhandler(fileName, 1)
                poi_list = retrieve_poi_list()
                #add pois to gui list
                for item in poi_list:
                    self.pointsOI.addItem(item)

            elif caller == 2:
                self.pluginDataSet.setText(fileName)
                self.pluginxmlhandler(fileName, 2)

            global myFileName
            myFileName = fileName
            return fileName

        self.updatePluginList()
        return "not found"

    # stores xml1 and xml2 from browse buttons
    def pluginxmlhandler(self, filePath, caller):
        global xml1
        global xml2
        if caller == 1:
            tree = ET.parse(filePath)
            xml1 = tree.getroot()
        elif caller == 2:
            tree = ET.parse(filePath)
            xml2 = tree.getroot()

    def updatePluginList(self):
        self.searchList.clear()
        pluginList = xmlUploader.retrieve_list_of_plugin()
        for item in pluginList:
            self.searchList.addItem(item)

    def update_poi_list(self,plugin):
        self.pointsOI.clear()

        # get poi list
        list_of_poi = []
        x = plugin['Plugin']['DataInPlugin']
        for y in x:
            print(x)
            print('///////////////////')
            print(y)
            #self.pointsOI.addItem(str(y.attrib['name']))
            list_of_poi.append(y)

        return list_of_poi
        '''''
        # add pois to gui list
        for item in list_of_poi:
            self.pointsOI.addItem(item)
        '''''

    def enableEditing(self):
        self.pluginStructArea.setEnabled(True)
        self.pluginDataSet.setEnabled(True)
        self.pluginName.setEnabled(True)
        self.pluginDesc.setEnabled(True)

    def disableEditing(self):
        self.pluginStructArea.setEnabled(False)
        self.pluginDataSet.setEnabled(False)
        self.pluginName.setEnabled(False)
        self.pluginDesc.setEnabled(False)

    def createNew(self):
        # load buttons and Layout
        self.loadRightLayout()
        self.deleteButton.hide()
        self.browseButton1.show()
        self.browseButton2.show()
        self.saveButton.show()
        # Clear
        self.pluginName.clear()
        self.pluginDesc.clear()
        self.pluginStructArea.clear()
        self.pluginDataSet.clear()
        self.pointsOI.clear()

        self.updatePluginList()
        self.enableEditing()

    def deletePluggin(self):
        global nameH
        toErase = nameH.toPlainText()

        if not toErase:
            errorMessageGnerator.showDialog("Please select a Plugin to delete", 'Delete plugin')

        xmlUploader.delete_selected_plugin(toErase)
        for item in self.searchList.selectedItems():
            self.searchList.takeItem(self.searchList.row(item))

        self.updatePluginList()
        # self.createNew()

    def savexml(self):
        global xml1
        global xml2
        global nameH
        global descH

        pname = nameH.toPlainText()
        pdesc = descH.toPlainText()

        if pname != "" and pdesc != "":
            # gui text to xml
            b2tf = xml1.find("./Plugin_name")
            b2tf.text = pname
            b2tf = xml1.find("./Plugin_Desc")
            b2tf.text = pdesc
            b2tf = xml1.find("./structure_path")
            b2tf.text = structH.toPlainText()
            b2tf = xml1.find("./predefined_dataset_path")
            b2tf.text = pdatasetH.toPlainText()
            #convert then upload
            my_dict = ET.tostring(xml1, encoding='utf8').decode('utf8')
            xmlUploader.uploadPlugin(my_dict)

            self.updatePluginList()
            self.disableEditing()

        elif pname == "":
            errorMessageGnerator.showDialog("Enter a Plugin name", "Plugin Name Error")

        elif pdesc == "":
            errorMessageGnerator.showDialog("Enter a description for the Plugin", "Plugin File Error")

def save_xml_local(self):
    global xml2
    savePath = ("/mnt/c/Users/RedFlash05/Desktop")
    name_of_file = ('testingSavingFunctionalitytolocal')
    completeName = os.path.join(savePath, name_of_file + ".txt")

    print('Saving Locally')

#Returns a list of strings from XML1 only
def retrieve_poi_list():
    global xml1
    x = xml1.find("./DataInPlugin")
    list_of_poi = []

    for y in x:
        list_of_poi.append(str(y.attrib['name']))
        print(str(y.attrib['name']))

    return list_of_poi
