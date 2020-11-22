import sys
from PyQt5 import QtWidgets, uic
import chat_gui

app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('TestForm.ui')
window.btnQuit.clicked.connect(app.quit)
window.show()
sys.exit(app.exec)
