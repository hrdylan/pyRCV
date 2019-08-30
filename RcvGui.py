from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])
dlg = uic.loadUi("truePyRCV.ui")

dlg.show()
app.exec()
