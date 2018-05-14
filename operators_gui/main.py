#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtGui, QtWidgets, uic

from operators_gui.sql.sql_queries import *
from operators_gui.sql.table_models import *
from operators_gui.misc.labels import *
from operators_gui.misc.checkers import *
from operators_gui.misc.dates import *
from operators_gui.misc.parameters import *
from operators_gui.plotter import Plotter


class OperatorApp(QtWidgets.QWidget):

    def __init__(self):
        super(OperatorApp, self).__init__()
        # автоматическое обновление таблиц. Настройка интервала в misc.parameters
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.table_update)
        self.timer.setInterval(table_update)
        self.timer.start()
        self.plotter = Plotter(self)
        self.gui()

    def gui(self):
        self.window = uic.loadUi("./uis/operator_gui.ui")
        # Действие по двойному клику по таблице
        self.window.mainTable.doubleClicked.connect(self.table_double_click)
        # Действие по смене значения в выпадающем меню
        self.table_change(0)
        self.window.tableSelector.currentIndexChanged.connect(
            lambda: self.table_change(self.window.tableSelector.currentIndex())
        )
        # Подключаем действия к пунктам меню
        self.window.actionExit.triggered.connect(QtWidgets.QApplication.quit)
        self.window.addCard.triggered.connect(self.add_new_card)
        self.window.addTrip.triggered.connect(self.edit_new_trip)
        # Установка текущей даты в поле выбора
        self.window.dateEdit.setDate(QtCore.QDate.currentDate())
        self.window.dateEdit.setVisible(False)
        self.window.dateEdit.dateChanged.connect(lambda: self.table_change(3))
        # При открытии окна, оно будет развернуто на всю доступную область
        #self.window.setGeometry(QtWidgets.QDesktopWidget().availableGeometry())
        self.center(self.window)
        self.window.show()

    # Двойной клик по таблице
    def table_double_click(self):
        # Получить данные о рейсе
        self.selected_id = [self.window.mainTable.model().data(index)
                            for index in self.window.mainTable.selectedIndexes()][0]
        self.trip_data = get_data(self.selected_id)
        if self.window.tableSelector.currentIndex() == 1:
            # Открыть форму вызова из очереди
            self.callForm = uic.loadUi("./uis/line_call.ui")
            self.callForm.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
            # Заполнить поля
            self.callForm.driverEdit.setText(self.trip_data[2])
            self.callForm.infoLbl.setText(info_label
                                          .format(self.trip_data[3],
                                                  self.trip_data[4],
                                                  self.trip_data[5], ))
            # Список выгрузок
            self.unloads = get_unloads()
            self.callForm.unloadsList.addItems([item for item in self.unloads])
            # Если выгрузка уже назначена, установим назначенное значение
            # if self.trip_data[6] is not None:
                # self.current_unload = self.trip_data[6]
                # self.callForm.unloadsList.setCurrentIndex(self.unloads[self.trip_data[9]] - 1)
            # Подключить действие к кнопкам
            self.callForm.saveBtn.clicked.connect(self.line_call)
            self.callForm.cancelBtn.clicked.connect(
                lambda: self.callForm.close()
            )
            # Выровнять по центру экрана и показать форму
            self.center(self.callForm)
            self.callForm.show()
        elif self.window.tableSelector.currentIndex() == 2 or \
                self.window.tableSelector.currentIndex() == 3:
            # Переменная нужна. чтобы отличить существующий рейс от нового
            self.record_id = 1
            # Открыть форму редактирования рейса
            self.editForm = uic.loadUi("./uis/trip_edit.ui")
            self.editForm.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
            # Заполнить поля
            self.editForm.headerLbl.setText(edit_header.format(str(self.trip_data[0])))
            self.editForm.docEdit.setText(str(self.trip_data[1]))
            self.editForm.driverEdit.setText(self.trip_data[2])
            self.editForm.infoLbl.setText(info_label
                                          .format(self.trip_data[3],
                                                  self.trip_data[4],
                                                  self.trip_data[5],))
            self.editForm.loadEdit.setText(self.trip_data[6])
            # Список выгрузок
            self.unloads = get_unloads()
            self.editForm.unloadsList.addItems([item for item in self.unloads])
            if self.trip_data[9] is not None:
                self.current_unload = self.trip_data[9]
                self.editForm.unloadsList.setCurrentIndex(self.unloads[self.trip_data[9]] - 1)
            # Подключить действия к кнопкам
            self.editForm.cancelBtn.clicked.connect(
                lambda: self.editForm.close()
            )
            self.editForm.saveBtn.clicked.connect(self.save_trip)
            # Кнопки на полях ввода
            if self.window.tableSelector.currentIndex() == 3:
                self.editForm.driverEdit.addAction(self.editForm.changeDriver, 1)
                self.editForm.changeDriver.triggered.connect(
                    lambda: self.read_rfid(self.driver_change))
                self.editForm.driverEdit.returnPressed.connect(
                    lambda: self.read_rfid(self.driver_change))
            self.editForm.loadEdit.addAction(self.editForm.changeLoad, 1)
            self.editForm.changeLoad.triggered.connect(self.select_loadpoint)
            self.editForm.loadEdit.returnPressed.connect(self.select_loadpoint)
            # Отобразить в центре экрана
            self.center(self.editForm)
            self.editForm.show()

    # Показать все колонки
    def show_all_columns(self):
        for col in range(0, 22):
            self.window.mainTable.setColumnHidden(col, False)

    # Скрыть нужные колонки
    def hide_columns(self, _col_list):
        for col in _col_list:
            self.window.mainTable.setColumnHidden(col, True)

    # Действие по смене типа таблицы
    def table_change(self, _int):
        if _int == 0:
            self.show_all_columns()
            self.window.mainTable.setModel(enrouteModel)
            self.enroute_hidden_columns = [1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            self.hide_columns(self.enroute_hidden_columns)
            self.window.dateEdit.setVisible(False)
        elif _int == 1:
            self.show_all_columns()
            self.window.mainTable.setModel(inlineModel)
            self.inline_hidden_columns = [1, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            self.hide_columns(self.inline_hidden_columns)
            self.window.dateEdit.setVisible(False)
        elif _int == 2:
            self.show_all_columns()
            self.window.mainTable.setModel(incompleteModel)
            self.incomplete_hidden_columns = [5, 6, 8, 10, 12, 15, 16, 17, 18, 19, 20, 21]
            self.hide_columns(self.incomplete_hidden_columns)
            self.window.dateEdit.setVisible(False)
        elif _int == 3:
            self.show_all_columns()
            self.window.mainTable.setModel(tripsModel)
            self.shift = day_shift(self.window.dateEdit.date().toPyDate())
            tripsModel.setFilter("tare_weight is not null and tare_dt between '{}' and '{}'".
                                 format(self.shift[0],
                                        self.shift[1]))
            self.complete_hidden_columns = [8, 10, 15, 18, 20, 21]
            self.hide_columns(self.complete_hidden_columns)
            self.window.dateEdit.setVisible(True)
        self.window.mainTable.setColumnWidth(0, 50)
        self.window.mainTable.resizeRowsToContents()

    # Сохранение рейса после редактирования
    def save_trip(self):
        # Добавить новый рейс или обновить существующий
        if self.record_id != 0:
            self.record_id = self.trip_data[0]
        # Данные для записи
        self.doc = self.editForm.docEdit.text()
        self.driver_info = get_driver(self.editForm.driverEdit.text())
        self.loadpoint = get_loadpoint(self.editForm.loadEdit.text())
        self.unloadpoint = self.unloads[self.editForm.unloadsList.currentText()]
        if self.record_id == 0:
            self.insert = record_insert(self.doc,
                                        self.driver_info[0],
                                        self.driver_info[1],
                                        self.driver_info[2],
                                        self.loadpoint,
                                        self.unloadpoint,
                                        QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'))
        elif self.record_id != 0:
            self.update = record_update(self.doc,
                                        self.driver_info[0],
                                        self.driver_info[1],
                                        self.driver_info[2],
                                        self.loadpoint,
                                        self.unloadpoint,
                                        self.record_id
                                        )
        self.table_update()
        self.editForm.close()

    # Вызвать из очереди
    def line_call(self):
        # Подготовим данные для обновления записи
        self.record_id = self.trip_data[0]
        self.unloadpoint = self.unloads[self.callForm.unloadsList.currentText()]
        self.update = set_unload(self.unloadpoint, self.record_id)
        self.callForm.close()

    # Показать окно по центру экрана
    def center(self, _widget):
        self.widget_size = _widget.frameGeometry()
        self.display_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.widget_size.moveCenter(self.display_center)
        _widget.move(self.widget_size.topLeft())

    # Обновить таблицу и графики
    def table_update(self):
        if self.window.mainTable.model() is not None:
            self.window.mainTable.model().select()
        self.plotter.start()
        self.window.tripChartLabel.setPixmap(QtGui.QPixmap("./res/plot_count.png"))
        self.window.tonnChartLabel.setPixmap(QtGui.QPixmap("./res/plot_sum.png"))

    # Прочитать карту водителя
    def read_rfid(self, _action):
        self.rfidInput = uic.loadUi("./uis/rfid.ui")
        self.animated_logo = QtGui.QMovie("./res/rfid.gif")
        self.rfidInput.label.setMovie(self.animated_logo)
        self.animated_logo.start()
        self.rfidInput.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.rfidInput.rfid.returnPressed.connect(_action)
        self.center(self.rfidInput)
        self.rfidInput.show()

    # Сменить водителя
    def driver_change(self):
        self.driver_id = int(rfid_to_driver(
            self.rfidInput.rfid.text()
        ))
        self.driver_info = get_driver(self.driver_id)
        if len(self.driver_info) == 4:
            self.editForm.driverEdit.setText(self.driver_info[0])
            self.editForm.infoLbl.setText(info_label
                                          .format(self.driver_info[1],
                                                  self.driver_info[2],
                                                  self.driver_info[3]))
            self.rfidInput.close()
            self.table_update()
        else:
            self.error_message = QtWidgets.QMessageBox()
            self.error_message.setText("Эта карта не зарегистрирована")
            self.error_message.show()
            self.rfidInput.rfid.clear()

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

    # Установить фильтр
    def set_filter(self, _model):
        if _model == loadsModel:
            loadsModel.setFilter("name like '%{}%'"
                                 .format(self.loadSelect.searchEdit.text()))
        elif _model == trucksModel:
            trucksModel.setFilter("plate like '%{}%'"
                                  .format(self.truckSelect.searchEdit.text()))
        elif _model == suppliersModel:
            suppliersModel.setFilter("transporter_only = 0 and full_name like '%{}%'"
                                     .format(self.supplierSelect.searchEdit.text()))

    # Действие по двойному клику. Таблица "Пункты погрузки"
    def selector_double_click(self, selector_id):
        if selector_id == 0:
            self.selected_load = [self.loadSelect.refTable.model().data(index)
                                for index in self.loadSelect.refTable.selectedIndexes()][1]
            self.editForm.loadEdit.setText(self.selected_load)
            self.loadSelect.close()
        elif selector_id == 1:
            self.selected_truck = [self.truckSelect.refTable.model().data(index)
                                for index in self.truckSelect.refTable.selectedIndexes()][1]
            self.cardForm.truckEdit.setText(self.selected_truck)
            self.truckSelect.close()
        elif selector_id == 2:
            self.selected_supplier = [self.supplierSelect.refTable.model().data(index)
                                for index in self.supplierSelect.refTable.selectedIndexes()][1]
            self.cardForm.supEdit.setText(self.selected_supplier)
            self.supplierSelect.close()

    # Выдать новую карту
    def add_new_card(self):
        self.cardForm = uic.loadUi("./uis/card_edit.ui")
        self.cardForm.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.cardForm.truckEdit.addAction(self.cardForm.changeTruck, 1)
        self.cardForm.changeTruck.triggered.connect(self.select_transport)
        self.cardForm.truckEdit.returnPressed.connect(self.select_transport)
        self.cardForm.supEdit.addAction(self.cardForm.changeEmployer, 1)
        self.cardForm.changeEmployer.triggered.connect(self.select_supplier)
        self.cardForm.supEdit.returnPressed.connect(self.select_supplier)
        self.cardForm.saveBtn.clicked.connect(
            lambda: self.read_rfid(self.save_card))
        self.cardForm.cancelBtn.clicked.connect(
            lambda: self.cardForm.close()
        )
        self.center(self.cardForm)
        self.cardForm.show()

    # Сохранить новую карту
    def save_card(self):
        try:
            self.driver = name_checker(self.cardForm.driverEdit.text())
            self.rfid = self.rfidInput.rfid.text()
            self.rfidInput.close()
            self.transport = get_transport(self.cardForm.truckEdit.text())
            self.supplier = get_supplier(self.cardForm.supEdit.text())
            self.insert = insert_driver(self.driver,
                                        self.transport,
                                        self.supplier,
                                        self.rfid)
            self.cardForm.close()
        except ValueError:
            self.name_check_error = QtWidgets.QMessageBox()
            self.name_check_error.setWindowTitle("Что-то не так!")
            self.name_check_error.setText(wrong_data)
            self.name_check_error.setIcon(2)
            self.rfidInput.close()
            self.name_check_error.show()
        except IndexError:
            self.name_check_error = QtWidgets.QMessageBox()
            self.name_check_error.setWindowTitle("Что-то не так!")
            self.name_check_error.setText(wrong_data)
            self.name_check_error.setIcon(2)
            self.rfidInput.close()
            self.name_check_error.show()

    # Начать новый рейс
    def edit_new_trip(self):
        # Пометить рейс как новый
        self.record_id = 0
        # Открыть пустую форму редактирования рейса
        self.editForm = uic.loadUi("./uis/trip_edit.ui")
        self.editForm.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        # Список выгрузок
        self.unloads = get_unloads()
        self.editForm.unloadsList.addItems([item for item in self.unloads])
        # Подключить действия к кнопкам
        self.editForm.cancelBtn.clicked.connect(
            lambda: self.editForm.close()
        )
        self.editForm.saveBtn.clicked.connect(self.save_trip)
        # Кнопки на полях ввода
        self.editForm.driverEdit.addAction(self.editForm.changeDriver, 1)
        self.editForm.changeDriver.triggered.connect(
            lambda: self.read_rfid(self.driver_change))
        self.editForm.driverEdit.returnPressed.connect(
            lambda: self.read_rfid(self.driver_change))
        self.editForm.loadEdit.addAction(self.editForm.changeLoad, 1)
        self.editForm.changeLoad.triggered.connect(self.select_loadpoint)
        self.editForm.loadEdit.returnPressed.connect(self.select_loadpoint)
        # Отобразить в центре экрана
        self.center(self.editForm)
        self.editForm.show()

    # Выбор автомобиля
    def select_transport(self):
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

    # Выбор поставщика
    def select_supplier(self):
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _gui = OperatorApp()
    sys.exit(app.exec_())
