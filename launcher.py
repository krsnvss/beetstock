#!/usr/bin/python3
# Выбор интерфейса для работы
import sys
from PyQt5 import QtCore, QtSql, QtWidgets, uic
from arrival_point.arrival_gui import ArrivalPoint
from operators_gui.operator_gui import OperatorApp
from operators_gui.plotter import Plotter
from operators_gui.doc_print import DocPrinter, ThreadPrinter
from scales.scales_gui import Scales
from unload_point.unload_gui import Unloader
from sql.sql_queries import *
from sql.db_connection import *


class Launcher(QtWidgets.QWidget):

    def __init__(self):
        super(Launcher, self).__init__()
        self.launcher_window = uic.loadUi("./uis/launcher.ui")
        self.launcher_window.arrivalButton.clicked.connect(
            lambda: self.start_gui(ArrivalPoint())
        )
        self.launcher_window.operatorButton.clicked.connect(
            lambda: self.start_gui(OperatorApp())
        )
        self.launcher_window.scaleButton.clicked.connect(
            lambda: self.start_gui(Scales())
        )
        self.launcher_window.unloadButton.clicked.connect(
            lambda: self.start_gui(Unloader())
        )
        # Системный трей
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_TitleBarMenuButton))
        self.launcher_window.showWindow.triggered.connect(
            lambda: self.center(self.launcher_window)
        )
        self.launcher_window.hideWindow.triggered.connect(
            self.launcher_window.hide
        )
        self.launcher_window.closeWindow.triggered.connect(
            QtWidgets.qApp.quit
        )
        self.tray_menu = QtWidgets.QMenu()
        self.tray_menu.addAction(self.launcher_window.showWindow)
        self.tray_menu.addAction(self.launcher_window.hideWindow)
        self.tray_menu.addAction(self.launcher_window.closeWindow)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        self.center(self.launcher_window)
        self.launcher_window.show()

    def start_gui(self, _gui):
        self.gui = _gui
        self.gui
        self.launcher_window.hide()

    # Показать окно по центру экрана
    def center(self, _widget):
        self.launcher_window.show()
        self.widget_size = _widget.frameGeometry()
        self.display_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.widget_size.moveCenter(self.display_center)
        _widget.move(self.widget_size.topLeft())


# Авторизация
class AuthForm(QtWidgets.QWidget):

    def __init__(self):
        super(AuthForm, self).__init__()
        self.auth_dialog()

    # Запрос авторизации для подключения к БД
    def auth_dialog(self):
        self.authForm = uic.loadUi("./uis/authForm.ui")
        self.authForm.errorLabel.setVisible(False)
        self.authForm.loginButton.clicked.connect(self.check_auth)
        self.authForm.show()

    # Проверка введенных логина и пароля
    def check_auth(self):
        db_user = self.authForm.loginEdit.text()
        db_password = self.authForm.passEdit.text()
        db.setUserName(db_user)
        db.setPassword(db_password)
        if db.open():
            self.launcher = Launcher()
            self.authForm.close()
        else:
            self.authForm.loginEdit.clear()
            self.authForm.passEdit.clear()
            self.authForm.errorLabel.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _gui = AuthForm()
    sys.exit(app.exec_())