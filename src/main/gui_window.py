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

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import os
import sys
import time

py_version = sys.version.split(" ")[0].split(".")
if int(py_version[0]) < 3 or int(py_version[1]) < 8 or (int(py_version[1]) == 8 and int(py_version[2]) < 10):
    raise Exception("Python 3.8.10 or higher is required.")

if os.path.abspath(os.getcwd()) == os.path.dirname(os.path.abspath(__file__)):
    workdir = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
    os.chdir(workdir)  # 작업 디렉토리를 프로젝트 루트로 변경
    if workdir not in sys.path:
        sys.path.append(workdir)  # 프로젝트 루트를 파이썬 모듈 경로에 추가

from src.main.gui.core.functions import set_svg_icon
from src.main.gui.uis.windows.main_window.functions_main_window import MainFunctions

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from src.main.qt_core import SUPPORT_WINDOWS_7
from src.main.qt_core import QMainWindow
from src.main.qt_core import QApplication
from src.main.qt_core import QIcon
from src.main.qt_core import QTimer

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from src.main.gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from src.main.gui.uis.windows.main_window import UiMainWindow
from src.main.gui.uis.windows.main_window import SetupMainWindow
# SPLASH WINDOW
from src.main.gui.uis.windows.splash_window import UiSplashWindow

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
'from gui.widgets import *'

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"''


# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UiMainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # LOAD USER PAGE
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)

                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu=self.ui.left_column.menus.menu_2,
                    title="Info tab",
                    icon_path=set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu=self.ui.left_column.menus.menu_1,
                    title="Settings Left Column",
                    icon_path=set_svg_icon("icon_settings.svg")
                )

        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////

        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos() if SUPPORT_WINDOWS_7 else event.globalPosition().toPoint()


# SPLASH WINDOW
class SplashWindow(QMainWindow, UiSplashWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        UiSplashWindow.__init__(self)
        self.args = args

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # DEBUG
        # ///////////////////////////////////////////////////////////////
        # QTIMER ==> START=
        self.timer = QTimer()
        self.timer.timeout.connect(self.proceed)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION
        # ///////////////////////////////////////////////////////////////
        # Initial Text
        self.ui.label_title.setText("<strong>{}</strong> - {}".format(*self.settings['app_name'].split(" - ")))
        self.ui.label_small_title.setText("<strong>{}</strong> - {}".format(*self.settings['app_name'].split(" - ")))
        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")
        self.ui.label_credits.setText(f"<strong>{self.settings['company_name']} - {self.settings['version']}</strong>")
        # Change Texts
        QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        # SHOW ==> MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()
        UiSplashWindow.adjust_window_position(self)  # adjust window position

    # ==> APP FUNCTIONS
    # ///////////////////////////////////////////////////////////////
    def proceed(self):
        self.construct_shadow()  # 그림자 오류 수정 (로딩 객체 가려지는 문제 해결)

        # CLOSE SPLASH SCREE AND OPEN APP
        if self.get_progress() > 99:
            # STOP TIMER
            self.timer.stop()

            # SHOW LOGIN PANEL
            self.fade_objects(lambda: self.show_login_panel(self))

        # SET VALUE TO PROGRESS BAR
        self.set_progress(self.get_progress() + 1)

    @staticmethod
    def on_close_button_clicked(window, callback=None):
        # CLOSE SPLASH SCREEN
        super().on_close_button_clicked(window, lambda: time.sleep(0.01) or window.close())


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icon.ico"))
    app_args = {}

    # SHOW SPLASH WINDOW
    # ///////////////////////////////////////////////////////////////
    window = SplashWindow(app_args)
    result = app.exec_() if SUPPORT_WINDOWS_7 else app.exec()
    del window, SplashWindow, UiSplashWindow  # cache는 삭제되지 않음.

    if 'login_success' not in app_args or not app_args['login_success']:
        sys.exit(result)

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    window = MainWindow(app_args)
    sys.exit(app.exec_() if SUPPORT_WINDOWS_7 else app.exec())
