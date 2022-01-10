# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
# from QtCore
from src.main.qt_core import QCoreApplication
from src.main.qt_core import QMetaObject
from src.main.qt_core import QRect
from src.main.qt_core import QSize
from src.main.qt_core import Qt
# from QtGui
from src.main.qt_core import QFont
# from QtWidgets
from src.main.qt_core import QWidget
from src.main.qt_core import QVBoxLayout
from src.main.qt_core import QFrame
from src.main.qt_core import QLabel
from src.main.qt_core import QProgressBar
from src.main.qt_core import QPushButton
from src.main.qt_core import QLineEdit

# IMPORT STYLES
# ///////////////////////////////////////////////////////////////
from src.main.gui.widgets.py_window.styles import Styles


class UiSplashScreen(object):
    def setup_ui(self, SplashScreen):
        if SplashScreen.objectName():
            SplashScreen.setObjectName(u"SplashScreen")
        SplashScreen.resize(600, 520)
        self.centralwidget = QWidget(SplashScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet("background: transparent")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)

        self.login_panel = QFrame(self.centralwidget)
        self.login_panel.setObjectName(u"login_panel")
        self.login_panel.setGeometry(QRect(0, 0, 560, 230))
        self.login_panel.setStyleSheet("background: transparent")
        self.login_panel.setFrameShape(QFrame.StyledPanel)
        self.login_panel.setFrameShadow(QFrame.Raised)
        self.login_panel.setVisible(False)
        self.login_panel_back = QFrame(self.login_panel)
        self.login_panel_back.setObjectName(u"login_panel")
        self.login_panel_back.setGeometry(QRect(10, 10, 500, 210))
        self.login_panel_back.setStyleSheet(
            u"QFrame {	\n"
            "	background-color: rgb(30, 30, 44);	\n"
            "	color: rgb(220, 220, 220);\n"
            "	border-width: 3px;\n"
            "	border-radius: 20px;\n"
            "	border-style: solid;\n"
            "	border-color: rgb(56, 58, 89);\n"
            "}")
        self.login_panel_back.setFrameShape(QFrame.StyledPanel)
        self.login_panel_back.setFrameShadow(QFrame.Raised)
        self.lock_icon = QFrame(self.login_panel)
        self.lock_icon.setObjectName(u"lock_icon")
        self.lock_icon.setGeometry(QRect(360, 70, 120, 120))
        self.lock_icon.setMinimumSize(QSize(120, 120))
        self.lock_icon.setMaximumSize(QSize(120, 120))
        self.lock_icon.setFrameShape(QFrame.NoFrame)
        self.lock_icon.setFrameShadow(QFrame.Raised)
        self.lock_icon.setVisible(False)
        self.lock_icon_layout = QVBoxLayout(self.lock_icon)
        self.lock_icon_layout.setSpacing(0)
        self.lock_icon_layout.setObjectName(u"lock_icon_layout")
        self.lock_icon_layout.setContentsMargins(0, 0, 0, 0)
        self.user_name = QLabel(self.login_panel)
        self.user_name.setObjectName(u"user_name")
        self.user_name.setGeometry(QRect(44, 70, 240, 34))
        user_name_font = QFont()
        user_name_font.setFamily(u"Segoe UI")
        user_name_font.setPointSize(22)
        self.user_name.setFont(user_name_font)
        self.user_name.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.user_name.setAlignment(Qt.AlignLeft)
        self.user_name.setVisible(False)
        self.user_name_description = QLabel(self.login_panel)
        self.user_name_description.setObjectName(u"user_name_description")
        self.user_name_description.setGeometry(QRect(44, 110, 240, 20))
        user_name_description_font = QFont()
        user_name_description_font.setFamily(u"Segoe UI")
        user_name_description_font.setPointSize(8)
        self.user_name_description.setFont(user_name_description_font)
        self.user_name_description.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.user_name_description.setAlignment(Qt.AlignLeft)
        self.user_name_description.setVisible(False)

        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet("background: transparent")
        self.dropShadowBackFrame = QFrame(self.dropShadowFrame)
        self.dropShadowBackFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowBackFrame.setGeometry(QRect(10, 10, 560, 300))
        self.dropShadowBackFrame.setStyleSheet(
            u"QFrame {	\n"
            "	background-color: rgb(44, 49, 60);	\n"
            "	color: rgb(220, 220, 220);\n"
            "	border-width: 3.2px;\n"
            "	border-radius: 20px;\n"
            "	border-style: solid;\n"
            "	border-color: rgb(72, 80, 98);\n"
            "}")
        self.dropShadowBackFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowBackFrame.setFrameShadow(QFrame.Raised)

        self.label_small_title = QLabel(self.dropShadowFrame)
        self.label_small_title.setObjectName(u"label_small_title")
        self.label_small_title.setGeometry(QRect(44, 36, 506, 34))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(15)
        self.label_small_title.setFont(font)
        self.label_small_title.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_small_title.setAlignment(Qt.AlignLeft)
        self.label_small_title.setVisible(False)
        self.logo = QFrame(self.dropShadowFrame)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(140, 10, 300, 300))
        self.logo.setMinimumSize(QSize(300, 300))
        self.logo.setMaximumSize(QSize(300, 300))
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Raised)
        self.logo.setVisible(False)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.label_title = QLabel(self.dropShadowFrame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(30, 70, 520, 60))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(30)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"color: rgb(254, 121, 199);")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_description = QLabel(self.dropShadowFrame)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setGeometry(QRect(10, 144, 560, 30))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(14)
        self.label_description.setFont(font1)
        self.label_description.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_description.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self.dropShadowFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(60, 180, 460, 22))
        self.progressBar.setStyleSheet(
            u"QProgressBar {\n"
            "	\n"
            "	background-color: rgb(98, 114, 164);\n"
            "	color: rgb(200, 200, 200);\n"
            "	border-style: none;\n"
            "	border-radius: 10px;\n"
            "	text-align: center;\n"
            "}\n"
            "QProgressBar::chunk{\n"
            "	border-radius: 10px;\n"
            "	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));\n"
            "}")
        self.progressBar.setValue(24)
        self.label_loading = QLabel(self.dropShadowFrame)
        self.label_loading.setObjectName(u"label_loading")
        self.label_loading.setGeometry(QRect(60, 210, 460, 22))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(12)
        self.label_loading.setFont(font2)
        self.label_loading.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_loading.setAlignment(Qt.AlignCenter)
        self.label_credits = QLabel(self.dropShadowFrame)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setGeometry(QRect(50, 260, 480, 20))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(8)
        self.label_credits.setFont(font3)
        self.label_credits.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_credits.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.close_button = QPushButton(self.dropShadowFrame)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setGeometry(QRect(524, 26, 30, 30))
        self.close_button.setStyleSheet(
            u"QPushButton {\n"
            "	border: none;\n"
            "	border-radius: 15px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: #55aaff;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "	background-color: #ff007f;\n"
            "}\n"
        )
        self.close_button.setVisible(False)

        self.login_button = QPushButton(self.centralwidget)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setGeometry(QRect(84, 424, 150, 36))
        login_button_font = QFont()
        login_button_font.setFamily(u"Segoe UI")
        login_button_font.setPointSize(12)
        self.login_button.setFont(login_button_font)
        self.login_button.setStyleSheet(
            u"QPushButton {\n"
            "	color: rgb(255, 255, 255);\n"
            "	border: none;\n"
            "	border-radius: 15px;\n"
            "	background-color: #485062;\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: #55aaff;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "	background-color: #ff007f;\n"
            "}\n"
        )
        self.login_button.setVisible(False)

        class QLineEditExt(QLineEdit):
            def focusInEvent(self, event):
                super(QLineEditExt, self).focusInEvent(event)
                try:
                    self.on_focus_in_event()
                except Exception:
                    pass

            def focusOutEvent(self, event):
                super(QLineEditExt, self).focusOutEvent(event)
                try:
                    self.on_focus_out_event()
                except Exception:
                    pass

            def set_on_focus_in_event(self, override):
                # 메서드 덮어쓰기
                self.on_focus_in_event = override

            def set_on_focus_out_event(self, override):
                # 메서드 덮어쓰기
                self.on_focus_out_event = override

        self.password_edit = QLineEditExt(self.centralwidget)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setAlignment(Qt.AlignHCenter)
        self.password_edit.setGeometry(QRect(310, 390, 160, 35))
        password_edit_font = QFont()
        password_edit_font.setFamily(u"Segoe UI")
        password_edit_font.setPointSize(12)
        self.password_edit.setFont(password_edit_font)
        self.PW_EDIT_STYLE = (
            u"QLineEdit {\n"
            "	color: rgb(100, 116, 166);\n"
            "	border: solid;\n"
            "	border-width: 4px;\n"
            "	border-radius: 10px;\n"
            "	border-color: rgb(98, 114, 164);\n"
            "	background-color: #404859;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "	background-color: #485062;\n"
            "}\n"
            "QLineEdit:focus {\n"
            "	color: rgb(255, 255, 255);\n"
            "	border-color: #55aaff;\n"
            "	background-color: #4f5f6f;\n"
            "}\n",
            u"QLineEdit {\n"
            "	color: rgb(0, 172, 86);\n"
            "	border: solid;\n"
            "	border-width: 4px;\n"
            "	border-radius: 10px;\n"
            "	border-color: rgb(0, 172, 86);\n"
            "	background-color: #404859;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "	background-color: #485062;\n"
            "}\n"
            "QLineEdit:focus {\n"
            "	background-color: #4f5f6f;\n"
            "}\n",
            u"QLineEdit {\n"
            "	color: rgb(139, 50, 67);\n"
            "	border: solid;\n"
            "	border-width: 4px;\n"
            "	border-radius: 10px;\n"
            "	border-color: rgb(139, 50, 67);\n"
            "	background-color: rgb(34, 34, 48);\n"
            "}\n"
            "QLineEdit:hover {\n"
            "	background-color: rgb(32, 32, 46);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "	background-color: rgb(30, 30, 44);\n"
            "}\n"
        )  # 0: plane, 1: correct, 2: incorrect
        self.password_edit.setStyleSheet(self.PW_EDIT_STYLE[0])
        self.password_edit.setVisible(False)

        self.verticalLayout.addWidget(self.dropShadowFrame)
        # 버튼 클릭 하려면 레이아웃 안에 넣어야 하는데 귀찮아서 그냥 상위 레이아웃에 갖다 붙였음.
        #self.verticalLayout.addWidget(self.login_panel)

        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)

        QMetaObject.connectSlotsByName(SplashScreen)
    # setupUi

    def retranslateUi(self, SplashScreen):
        SplashScreen.setWindowTitle(QCoreApplication.translate("SplashScreen", u"SplashScreen", None))
        self.label_title.setText(QCoreApplication.translate("SplashScreen", u"<strong>YOUR</strong> APP NAME", None))
        self.label_small_title.setText(QCoreApplication.translate("SplashScreen", u"<strong>YOUR</strong> APP NAME", None))
        self.label_description.setText(QCoreApplication.translate(
            "SplashScreen",
            u"<strong>APP</strong> DESCRIPTION",
            None
        ))
        self.label_loading.setText(QCoreApplication.translate("SplashScreen", u"loading...", None))
        self.label_credits.setText(QCoreApplication.translate(
            "SplashScreen",
            u"<strong>Created</strong>: Wanderson M. Pimenta",
            None
        ))
        self.user_name.setText(QCoreApplication.translate("SplashScreen", u"<strong>YOUR</strong> NAME", None))
        self.user_name_description.setText(QCoreApplication.translate(
            "SplashScreen",
            u"press login button to open main window.",
            None
        ))
        self.login_button.setText(QCoreApplication.translate("SplashScreen", u"LOGIN", None))
        self.password_edit.setPlaceholderText(QCoreApplication.translate("SplashScreen", u"Your Password", None))
    # retranslateUi
