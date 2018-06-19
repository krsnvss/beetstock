#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from sql.table_models import driversModel, loadsModel, trucksModel, suppliersModel
from sql.sql_queries import get_driver, set_driver, get_supplier, get_transport, \
    get_photo, add_photo, get_supplier_data, get_loadpoint, set_supplier


class CatalogApp(QtWidgets.QWidget):

    def __init__(self):
        super(CatalogApp, self).__init__()
        self.window = uic.loadUi('./uis/catalog.ui')
        # Таблица "Водители"
        self.window.driversTable.setModel(driversModel)
        self.window.driversTable.resizeColumnsToContents()
        self.drivers_hidden_columns = [2, 3, 4, 5, 8]
        for col in self.drivers_hidden_columns:
            self.window.driversTable.setColumnHidden(col, True)
        self.window.driversTable.doubleClicked.connect(
            lambda: self.driver_table_click())
        # Таблица "Поставщики"
        self.window.suppliersTable.setModel(suppliersModel)
        self.suppliers_hidden_columns = [3, 4, 5, 6, 7, 8]
        for col in self.suppliers_hidden_columns:
            self.window.suppliersTable.setColumnHidden(col, True)
        self.window.suppliersTable.setColumnWidth(0, 50)
        self.window.suppliersTable.setColumnWidth(1, 160)
        self.window.suppliersTable.setColumnWidth(2, 170)
        self.window.suppliersTable.doubleClicked.connect(
            self.supplier_table_click
        )
        # Значения по умолчанию
        self.selected_id = 0
        self.supplier_id = 0
        self.driver_photo = 1
        # Подключить действия к кнопкам
        self.window.driverSave.clicked.connect(self.save_driver)
        self.window.driverTruck.addAction(
            self.window.selectTruck, 1
        )
        self.window.driverEmployer.addAction(
            self.window.selectEmployer, 1
        )
        self.window.selectEmployer.triggered.connect(self.select_employer)
        self.window.selectTruck.triggered.connect(self.select_truck)
        self.window.addPhoto.clicked.connect(self.choose_photo)
        self.window.defaultLoad.addAction(
            self.window.selectLoad, 1
        )
        self.window.selectLoad.triggered.connect(self.select_loadpoint)
        self.window.supplierSave.clicked.connect(self.save_supplier)
        self.window.clearButton.clicked.connect(self.clear_edits)
        self.window.clearButton_2.clicked.connect(self.clear_edits)
        self.center(self.window)
        self.window.show()

    # Показать окно по центру экрана
    def center(self, _widget):
        self.widget_size = _widget.frameGeometry()
        self.display_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.widget_size.moveCenter(self.display_center)
        _widget.move(self.widget_size.topLeft())

    def driver_table_click(self):
        self.selected_id = [self.window.driversTable.model().data(index)
                            for index in self.window.driversTable.selectedIndexes()][0]
        self.driver_data = get_driver(self.selected_id)
        self.window.driverName.setText(self.driver_data[0])
        self.window.driverPhone.setText(str(self.driver_data[4]))
        self.window.driverEmail.setText(self.driver_data[5])
        self.window.driverComment.setText(self.driver_data[6])
        self.window.driverTruck.setText(self.driver_data[1])
        self.window.driverEmployer.setText(self.driver_data[3])
        self.window.driverRfid.setText(str(self.driver_data[8]))
        self.driver_pixmap = QtGui.QPixmap(get_photo(self.driver_data[7]))
        self.window.driverPhoto.setPixmap(
            self.driver_pixmap.scaled(128,
                                      128,
                                      QtCore.Qt.KeepAspectRatio,
                                      QtCore.Qt.SmoothTransformation)
        )

    def save_driver(self):
        if self.selected_id == 0:
            self.insert = True
        else:
            self.insert = False
        set_driver(self.selected_id,
                   self.window.driverName.text(),
                   self.window.driverPhone.text(),
                   self.window.driverEmail.text(),
                   self.window.driverComment.text(),
                   self.driver_photo,
                   get_transport(self.window.driverTruck.text()),
                   get_supplier(self.window.driverEmployer.text()),
                   self.window.driverRfid.text(),
                   self.insert)
        self.clear_edits()
        driversModel.select()

    # Выбрать пункт погрузки
    def select_loadpoint(self):
        self.loadSelect = uic.loadUi("./uis/selector.ui")
        self.loadSelect.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.loadSelect.refTable.setModel(loadsModel)
        self.center(self.loadSelect)
        self.loadSelect.refTable.setColumnHidden(3, True)
        self.loadSelect.refTable.setColumnHidden(4, True)
        self.loadSelect.refTable.setColumnWidth(0, 50)
        self.loadSelect.refTable.setColumnWidth(1, 120)
        self.loadSelect.refTable.setColumnWidth(2, 120)
        # Подключить действие к полю ввода
        self.loadSelect.searchEdit.textChanged.connect(
            lambda: self.set_filter(loadsModel))
        # Действие по двойному клику
        self.loadSelect.refTable.doubleClicked.connect(
            lambda: self.selector_double_click(0))
        self.loadSelect.show()

    # Выбор поставщика
    def select_employer(self):
        self.supplierSelect = uic.loadUi("./uis/selector.ui")
        self.supplierSelect.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.center(self.supplierSelect)
        self.supplierSelect.refTable.setModel(suppliersModel)
        self.supplierSelect.searchEdit.textChanged.connect(
            lambda: self.set_filter(suppliersModel))
        self.supplierSelect.refTable.setColumnHidden(1, True)
        self.supplierSelect.refTable.setColumnHidden(4, True)
        self.supplierSelect.refTable.setColumnHidden(5, True)
        self.supplierSelect.refTable.setColumnHidden(6, True)
        self.supplierSelect.refTable.setColumnHidden(7, True)
        self.supplierSelect.refTable.setColumnWidth(0, 50)
        self.supplierSelect.refTable.setColumnWidth(1, 120)
        self.supplierSelect.refTable.setColumnWidth(2, 120)
        self.supplierSelect.refTable.doubleClicked.connect(
            lambda: self.selector_double_click(2))
        self.supplierSelect.show()

    # Выбор автомобиля
    def select_truck(self):
        self.truckSelect = uic.loadUi("./uis/selector.ui")
        self.truckSelect.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.center(self.truckSelect)
        self.truckSelect.refTable.setModel(trucksModel)
        self.truckSelect.searchEdit.textChanged.connect(
            lambda: self.set_filter(trucksModel))
        self.truckSelect.refTable.setColumnHidden(1, True)
        self.truckSelect.refTable.setColumnHidden(4, True)
        self.truckSelect.refTable.setColumnHidden(5, True)
        self.truckSelect.refTable.setColumnHidden(6, True)
        self.truckSelect.refTable.setColumnWidth(0, 50)
        self.truckSelect.refTable.setColumnWidth(1, 120)
        self.truckSelect.refTable.setColumnWidth(2, 120)
        self.truckSelect.refTable.doubleClicked.connect(
            lambda: self.selector_double_click(1))
        self.truckSelect.show()

    # Действие по двойному клику. Таблица "Пункты погрузки"
    def selector_double_click(self, selector_id):
        if selector_id == 0:
            self.selected_load = [self.loadSelect.refTable.model().data(index)
                                for index in self.loadSelect.refTable.selectedIndexes()][1]
            self.window.defaultLoad.setText(self.selected_load)
            self.loadSelect.close()
        elif selector_id == 1:
            self.selected_truck = [self.truckSelect.refTable.model().data(index)
                                for index in self.truckSelect.refTable.selectedIndexes()][1]
            self.window.driverTruck.setText(self.selected_truck)
            self.truckSelect.close()
        elif selector_id == 2:
            self.selected_supplier = [self.supplierSelect.refTable.model().data(index)
                                for index in self.supplierSelect.refTable.selectedIndexes()][1]
            self.window.driverEmployer.setText(self.selected_supplier)
            self.supplierSelect.close()

    # Выбор фото
    def choose_photo(self):
        self.photo_selector = QtWidgets.QFileDialog()
        self.photo_selector.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if self.photo_selector.exec_():
            self.selected_photo = self.photo_selector.selectedFiles()[0]
            self.driver_photo = add_photo(self.selected_photo)
            self.driver_pixmap = QtGui.QPixmap(self.selected_photo)
            self.window.driverPhoto.setPixmap(
                self.driver_pixmap.scaled(128,
                                          128,
                                          QtCore.Qt.KeepAspectRatio,
                                          QtCore.Qt.SmoothTransformation)
            )

    # Очистка полей ввода
    def clear_edits(self):
        self.window.driverName.clear()
        self.window.driverTruck.clear()
        self.window.driverPhone.clear()
        self.window.driverEmail.clear()
        self.window.driverEmployer.clear()
        self.window.driverComment.clear()
        self.window.driverRfid.clear()
        self.window.driverPhoto.clear()
        self.window.supplierName.clear()
        self.window.supplierFullName.clear()
        self.window.supplierEmail.clear()
        self.window.supplierPhone.clear()
        self.window.supplierReq.clear()
        self.window.defaultLoad.clear()
        self.window.transporterOnly.setCheckState(0)
        self.selected_id = 0
        self.supplier_id = 0

    # Двойной щелчок по таблице поставщики
    def supplier_table_click(self):
        self.supplier_id = [self.window.suppliersTable.model().data(index)
                            for index in self.window.suppliersTable.selectedIndexes()][0]
        self.supplier_data = get_supplier_data(self.supplier_id)
        self.window.supplierName.setText(self.supplier_data[0])
        self.window.supplierFullName.setText(self.supplier_data[1])
        self.window.supplierEmail.setText(self.supplier_data[2])
        self.window.supplierPhone.setText(str(self.supplier_data[3]))
        self.window.supplierReq.setText(self.supplier_data[4])
        self.window.defaultLoad.setText(
            get_loadpoint(
                self.supplier_data[6]
            )
        )
        self.window.transporterOnly.setCheckState(
            self.supplier_data[5]
        )

    # Сохранить поставщика
    def save_supplier(self):
        if self.supplier_id == 0:
            self.insert = True
        else:
            self.insert = False
        set_supplier(self.supplier_id,
                     self.window.supplierName.text().upper(),
                     self.window.supplierFullName.text(),
                     self.window.supplierPhone.text(),
                     self.window.supplierEmail.text(),
                     self.window.supplierReq.text(),
                     self.window.transporterOnly.checkState(),
                     get_loadpoint(
                         self.window.defaultLoad.text()
                     ),
                     self.insert
                     )
        self.clear_edits()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _gui = CatalogApp()
    sys.exit(app.exec_())
