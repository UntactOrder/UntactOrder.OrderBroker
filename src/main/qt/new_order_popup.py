# https://stackoverflow.com/questions/46024724/pyqt-how-to-create-a-scrollable-window

import os
import sys
import time
#from playsound import playsound

from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton,
                             QScrollArea, QApplication, QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui


MUSIC_PATH = os.path.dirname(
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)))) + "/resource/new_order_sound.mp3"


class ScrollWindow(QMainWindow):
    def __init__(self, title, msg_list):
        super().__init__()
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(
            os.path.abspath(os.path.dirname(os.path.abspath(__file__))))))))+"/icon/server_logo.ico"))

        for msg in msg_list:
            self.vbox.addWidget(QLabel(msg))

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 800, 500)
        self.setWindowTitle(title)
        self.show()


def get_scroll_view(table, order, price):
    view = ScrollWindow("언택트 오더 - 새 주문 팝업", [
        f"주문자 정보 : 테이블 {table}", "----------------------------", "주문 상세보기 :", ""
    ]+order+["----------------------------", f"총 금액 : {price}"])
    return view


def run_order_popup(popup_queue, get_menu):
    app = QtWidgets.QApplication(sys.argv)
    while True:
        if popup_queue.qsize() > 0:
            #playsound(MUSIC_PATH, block=False)
            msg = []
            order = popup_queue.get()
            if order == -1:
                break
            for menu_id, count in order.items():
                menu = get_menu(int(menu_id))
                msg.append(menu.get_name() + "  x" + count)
            view = get_scroll_view(order.get_user_id(), msg, order.get_price())
            app.exec_()
        else:
            time.sleep(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = get_scroll_view("1", ["베이컨 필라프  x1", "까르보나라  x2", "베이컨 필라프  x1", "까르보나라  x2", "베이컨 필라프  x1", "까르보나라  x2", "베이컨 필라프  x1", "까르보나라  x2"], 50000)
    app.exec_()
