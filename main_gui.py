import asyncio
import sys

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel, QAbstractListModel, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QListView, QHBoxLayout, QVBoxLayout

from TelegramClient import STelegramClient
from main import init_clients


class QTelegramClientWidget(QWidget):
    def __init__(self,client: STelegramClient,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elem_height = 20
        self.elem_width = 150
        layout = QVBoxLayout()
        self.s_tg_client = client
        self.client_name_wd = QtWidgets.QLineEdit(self.s_tg_client.name)
        self.client_phone_wd = QtWidgets.QLineEdit(str(self.s_tg_client.phone))
        self.client_status_wd = QtWidgets.QLineEdit('Status :')

        self.client_name_wd.setReadOnly(True)
        self.client_name_wd.setStyleSheet('background-color: rgb(0,0,0,0)')
        self.client_phone_wd.setReadOnly(True)
        self.client_status_wd.setReadOnly(True)
        self.client_status_wd.setStyleSheet('background-color: rgb(0,0,0,0);border-style: outset;border-width: 0px;')


        self.client_name_wd.setFixedHeight( self.elem_height)
        self.client_phone_wd.setFixedHeight( self.elem_height)
        self.client_status_wd.setFixedHeight( self.elem_height)
        self.client_name_wd.setFixedWidth( self.elem_width)
        self.client_phone_wd.setFixedWidth( self.elem_width)
        self.client_status_wd.setFixedWidth( self.elem_width)
        layout.addWidget(self.client_name_wd)
        layout.addWidget(self.client_phone_wd)
        layout.addWidget(self.client_status_wd)
        self.setLayout(layout)






class QTelegramClients(QWidget):

    def __init__(self,tg_clients, *args, **kwargs):
        self.clients = tg_clients
        super().__init__(*args, **kwargs)
        funList = QtWidgets.QListWidget()
        for client in self.clients:
            item_n = QtWidgets.QListWidgetItem()
            widget = QTelegramClientWidget(client)
            item_n.setSizeHint(widget.sizeHint())
            funList.addItem(item_n)
            funList.setItemWidget(item_n, widget)
        lay = QHBoxLayout()
        lay.addWidget(funList,alignment=Qt.AlignCenter)
        funList.setFixedSize(900,300)
        # lay.addWidget(widget)
        self.setLayout(lay)


if __name__ == '__main__':
    q, resultQu, clients, users = asyncio.run(init_clients([380675111025, 380666913447]))
    app = QApplication(sys.argv)
    qt = QTelegramClients(clients)
    qt.show()
    app.exec_()
