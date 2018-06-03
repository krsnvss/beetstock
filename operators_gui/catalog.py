#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtGui, QtWidgets, uic
from sql.table_models import driversModel
from sql.sql_queries import get_driver


class CatalogApp(QtWidgets.QWidget):

    def __init__(self):
        super(CatalogApp, self).__init__()
        self.gui()

    def gui(self):
        self.window = uic.loadUi('./uis/catalog.ui')
        self.window.driversTable.setModel(driversModel)
        self.window.driversTable.resizeColumnsToContents()
        self.drivers_hidden_columns = [2, 3, 4, 5, 8]
        for col in self.drivers_hidden_columns:
            self.window.driversTable.setColumnHidden(col, True)
        self.window.driversTable.doubleClicked.connect(
            lambda: self.driver_table_click())
        self.window.show()

    def driver_table_click(self):
        self.selected_id = [self.window.driversTable.model().data(index)
                            for index in self.window.driversTable.selectedIndexes()][0]
        self.driver_data = get_driver(self.selected_id)
        self.window.driverName.setText(self.driver_data[0])
        self.window.driverPhone.setText(str(self.driver_data[4]))
        self.window.driverEmail.setText(self.driver_data[5])
        self.window.driverComment.setText(self.driver_data[6])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _gui = CatalogApp()
    sys.exit(app.exec_())
