#!/usr/bin/python3
# Выбор интерфейса для работы
import sys
from PyQt5 import QtCore, QtSql, QtWidgets, uic
from PyQt5.QtSql import QSqlDatabase, QSqlRelation, QSqlRelationalTableModel, QSqlTableModel
from arrival_point.arrival_gui import ArrivalPoint
from laboratory.laboratory_gui import LaboratoryApp
from operators_gui.operator_gui import OperatorApp
from operators_gui.catalog import CatalogApp
from operators_gui.plotter import Plotter
from operators_gui.doc_print import DocPrinter, ThreadPrinter
from scales.scales_gui import Scales
from unload_point.unload_gui import Unloader
from sql.sql_queries import *
from sql.table_models import *
from sql.db_connection import *
from conf.parameters import *
from configparser import ConfigParser


class Launcher(QtWidgets.QWidget):

    def __init__(self):
        super(Launcher, self).__init__()
        # Файл настроек
        self.configuration = ConfigParser()
        self.configuration.read('./conf/configuration.ini')
        # Загрузить окно из ui файла
        self.launcher_window = uic.loadUi("./uis/launcher.ui")
        # Привязать действия к кнопкам
        self.launcher_window.arrivalButton.clicked.connect(
            lambda: self.start_gui(ArrivalPoint())
        )
        self.launcher_window.operatorButton.clicked.connect(
            # lambda: self.start_gui(AuthForm())
            lambda: self.start_gui(OperatorApp())
        )
        self.launcher_window.scaleButton.clicked.connect(
            lambda: self.start_gui(Scales())
        )
        self.launcher_window.unloadButton.clicked.connect(
            lambda: self.start_gui(Unloader())
        )
        self.launcher_window.laboratoryButton.clicked.connect(
            lambda: self.start_gui(LaboratoryApp())
        )
        self.launcher_window.refsEdit.triggered.connect(
            lambda: self.start_gui(CatalogApp())
        )
        # Окно настроек
        self.launcher_window.changeParameters.triggered.connect(self.parameters)
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

    # Настройки
    def parameters(self):
        self.parametersForm = uic.loadUi("./uis/parameters.ui")
        self.parametersForm.headerEdit.addAction(self.parametersForm.saveChanges, 1)
        self.parametersForm.headerEdit.addAction(self.parametersForm.closeForm, 1)
        self.parametersForm.saveChanges.triggered.connect(
            self.save_config
        )
        self.parametersForm.closeForm.triggered.connect(
            lambda: self.parametersForm.close()
        )
        self.parametersForm.tuSpinBox.setValue(table_update / 1000)
        self.parametersForm.mtSpinBox.setValue(msg_time / 1000)
        self.parametersForm.dbName.setText(db_name)
        self.parametersForm.dbUser.setText(db_user)
        self.parametersForm.dbPass.setText(db_password)
        self.parametersForm.dbHost.setText(db_host)
        self.center(self.parametersForm)
        self.parametersForm.show()
        
    # Сохранить настройки
    def save_config(self):
        self.configuration['intervals']['table_update'] = str(
            self.parametersForm.tuSpinBox.value() *1000
        )
        self.configuration['intervals']['msg_time'] = str(
            self.parametersForm.mtSpinBox.value() * 1000
        )
        self.configuration['database']['db_name'] = self.parametersForm.dbName.text()
        self.configuration['database']['db_user'] = self.parametersForm.dbUser.text()
        self.configuration['database']['db_password'] = self.parametersForm.dbPass.text()
        self.configuration['database']['db_host'] = self.parametersForm.dbHost.text()
        with open('./conf/configuration.ini', 'w') as cfg:
            self.configuration.write(cfg)
        self.parametersForm.close()


# Авторизация
class AuthForm(QtWidgets.QWidget):

    def __init__(self):
        super(AuthForm, self).__init__()
        self.authForm = uic.loadUi("./uis/authForm.ui")
        self.authForm.passEdit.returnPressed.connect(self.check_auth)
        self.authForm.passEdit.addAction(self.authForm.loginAction, 1)
        self.authForm.loginAction.triggered.connect(self.check_auth)
        self.authForm.errorLabel.setVisible(False)
        # Окно без заголовка
        self.authForm.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.center(self.authForm)
        self.authForm.show()

    # Проверка введенных логина и пароля
    def check_auth(self):
        db_user = self.authForm.loginEdit.text()
        db_password = self.authForm.passEdit.text()
        db.setUserName(db_user)
        db.setPassword(db_password)
        if db.open():
            self.launcher = OperatorApp()
            self.authForm.close()
        else:
            self.authForm.loginEdit.clear()
            self.authForm.passEdit.clear()
            self.authForm.errorLabel.setVisible(True)
            self.authForm.statusBar.showMessage(
                "Проверьте имя пользователя и пароль", msg_time
            )

    # Показать окно по центру экрана
    def center(self, _widget):
        self.widget_size = _widget.frameGeometry()
        self.display_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.widget_size.moveCenter(self.display_center)
        _widget.move(self.widget_size.topLeft())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _gui = Launcher()
    sys.exit(app.exec_())