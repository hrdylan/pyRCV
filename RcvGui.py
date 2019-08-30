from PyQt5 import QtWidgets, uic
from classes import *
import sys
#push_button_2 = choose vote data




class pyRCV:

    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.dlg = uic.loadUi("truePyRCV.ui")
        self.chose_data = self.dlg.pushButton_2
        self.chose_data.clicked.connect(self.load_file)
        self.vote_run = self.dlg.voteRunButton
        self.vote_run.clicked.connect(self.run_election)
        self.dlg.statusBar().showMessage("Welcome!")


    def show_message(self):
        self.dlg.showMessage("hi", 500)

    def load_file(self):
        self.dlg.statusBar().clearMessage()
        self.dlg.statusBar().showMessage("Loading File...")
        self.dlg.repaint()
        fname, search = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '/home')


        if not fname.endswith(".csv"):
            print("incorrect file type")
            return

        vp = VotesParser(fname)
        vp.separate_csv()

        self.dlg.statusBar().clearMessage()

    def run_election(self):
        fname, search = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '/home')
        self.dlg.statusBar().clearMessage()
        self.dlg.statusBar().showMessage("Analyzing votes in " + fname)
        self.dlg.repaint()


        if not fname.endswith(".csv"):
            print("incorrect file type")
            return

        em = ElectionManager(fname)
        em.run_election()

        self.dlg.statusBar().clearMessage()




    def run(self):
        self.dlg.show()
        self.app.exec()


if __name__ == "__main__":
     rcv = pyRCV()
     rcv.run()

