#!/usr/bin/env python3

import sys
import r2pipe
import pymongo
import xml.etree.ElementTree as ET
import xmltodict
sys.path.append("../DB")
sys.path.append("../xml")
from xmlManager import SystemXmlManager


from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget
from PyQt5.QtGui import QPalette
from PyQt5.Qt import QColor

from PluginManagementTab import PluginManagementTab
from DocumentationTab import DocumentationTab
from analysisTab import AnalysisTab
from projectTab import ProjectTab

def main():
    # initialize stuff
    app = QApplication([])
    mainWindow = QMainWindow()
    
    # dark theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53,53,53))
    palette.setColor(QPalette.WindowText, QColor(255,255,255))
    palette.setColor(QPalette.WindowText, QColor(255,255,255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255,255,255))
    palette.setColor(QPalette.ToolTipText, QColor(255,255,255))
    palette.setColor(QPalette.Text, QColor(255,255,255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    palette.setColor(QPalette.BrightText, QColor(255,0,0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0,0,0))
    app.setPalette(palette)

    tabWidget = QTabWidget()
    tabWidget.addTab(ProjectTab(), "Project tab")
    tabWidget.addTab(PluginManagementTab(), "Plugin Management Tab")
    tabWidget.addTab(AnalysisTab(), "Analysis Tab")
    tabWidget.addTab(DocumentationTab(), "Documentation Tab")

    mainWindow.setWindowTitle("BEAT: Behavior Extraction and Analysis Tool")
    mainWindow.setWindowIcon(QtGui.QIcon('BEAT-logo.png'))
    mainWindow.setFont(QtGui.QFont('Helvetica', 12))
    mainWindow.setAutoFillBackground(True)
    mainWindow.setCentralWidget(tabWidget)
    mainWindow.show()
    
    sys.exit(app.exec())

systemManager = SystemXmlManager()
tree = ET.parse('../xml/Beat.xml')
root = tree.getroot()
my_dict = ET.tostring(root, encoding='utf8').decode('utf8')
if systemManager.isSystemEmpty():
    systemManager.uploadSystem(my_dict)
else:
    x=0

if __name__ == '__main__':
    main()

