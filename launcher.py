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
        self.launcher_window.show()

    def start_gui(self, _gui):
        self.gui = _gui
        self.gui


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _gui = Launcher()
    sys.exit(app.exec_())