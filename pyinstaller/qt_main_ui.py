# https://github.com/Mr-DooSun/PyQt5-GUI/blob/master/ex6_message_box/message_box.py

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, process_payment):
        super().__init__()

        self.process_payment = process_payment

        self.setWindowIcon(QtGui.QIcon("res/server_logo.ico"))
        self.setWindowTitle("언택트 오더 POS 주문 서버")
        self.setFixedSize(970, 90)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # About_button
        self.about_button = QtWidgets.QPushButton(self.centralwidget)
        self.about_button.setGeometry(QtCore.QRect(20, 20, 200, 50))
        self.about_button.setObjectName("about_button")
        self.about_button.setText("서버 버전 정보")
        self.about_button.clicked.connect(self.about_event)

        # Information_button
        self.information_button = QtWidgets.QPushButton(self.centralwidget)
        self.information_button.setGeometry(QtCore.QRect(230, 20, 200, 50))
        self.information_button.setObjectName("information_button")
        self.information_button.setText("결제 진행하기")
        self.information_button.clicked.connect(self.information_event)

        # Critical_button
        self.critical_button = QtWidgets.QPushButton(self.centralwidget)
        self.critical_button.setGeometry(QtCore.QRect(700, 20, 250, 50))
        self.critical_button.setObjectName("critical_button")
        self.critical_button.setText("주문 서버 종료하기")
        self.critical_button.clicked.connect(self.critical_event)

        self.show()

    # About 버튼 클릭 이벤트
    def about_event(self):
        box = QMessageBox.about(self, "언택트 오더 정보", '언택트 오더 포스 서버 v1.0.0.0')

    # Information 버튼 클릭 이벤트
    def information_event(self):
        button_reply = QMessageBox.information(
            self, "결제를 진행합니다.", "테이블 번호를 선택 후 금액을 확인하여 결제를 진행해 주세요.",
            QMessageBox.Yes | QMessageBox.Cancel)

        if button_reply == QMessageBox.Yes:
            self.process_payment()

    # Critical 버튼 클릭 이벤트
    def critical_event(self):
        button_reply = QMessageBox.critical(
            self, "서버 종료 확인", "주문 서버를 종료하면 더 이상 주문을 받을 수 없습니다.\n종료할까요?",
            QMessageBox.Yes | QMessageBox.Cancel)

        if button_reply == QMessageBox.Yes:
            QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
