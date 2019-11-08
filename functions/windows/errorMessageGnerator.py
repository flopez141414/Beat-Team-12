import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

def showDialog(message,title):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Warning)
   msgBox.setText(message)
   msgBox.setWindowTitle(title)
   msgBox.setStandardButtons(QMessageBox.Ok)
   msgBox.setSizeIncrement(1, 1)
   msgBox.setSizeGripEnabled(True)
   #msgBox.buttonClicked.connect(msgButtonClick)

   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok:
      print('OK clicked')

def infoToast(message,title):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Information)
   msgBox.setText(message)
   msgBox.setWindowTitle(title)
   msgBox.setStandardButtons(QMessageBox.Ok)
   msgBox.setSizeIncrement(1, 1)
   msgBox.setSizeGripEnabled(True)
   returnValue = msgBox.exec()


