import sys
import time

from PyQt5.QtCore import QObject
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QListWidgetItem
# from client_class import ClientReaderClass, ClientSenderClass


from client_chat_gui import Ui_MainWindow



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, transport=None, client_name=None, parent=None):

        # self.transport = transport
        # self.client_name = client_name

        # self.connect_to_server(transport, client_name)
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send_message)

        self.show()



    def get_user_contact_list(self, userlist):
        pass

    def send_message(self):
        print('Send msg')
        arr = ['lol', 'lol1', 'lol2']

        for i in arr:
            item = QListWidgetItem(i)
            self.ui.listWidget.addItem(item)

        # self.ui.listView.a

    def add_user_to_contact_list(self):
        pass

    def get_contact_list(self):
        pass


    # def connect_to_server(self, transport, client_name):
    #     md_reciver = ClientReaderClass(client_name, transport)
    #     md_reciver.daemon = True
    #     md_reciver.start()
    #
    #     md_sender = ClientSenderClass(client_name, transport)
    #     md_sender.daemon = True
    #     md_sender.start()
    #
    #     while True:
    #         time.sleep(1)
    #         if md_reciver.is_alive() and md_sender.is_alive():
    #             continue
    #         break


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     # progress = MainWindow()
#     # progress.show()
#     sys.exit(app.exec_())

