import sys
from PyQt5 import QtWidgets


def window():
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()

    window.setWindowTitle("BEAT: Behavior Extraction and Analysis Tool")

    window.setGeometry(50, 50, 500, 500)

    window.show()

    sys.exc_info(app.exec_())


window()