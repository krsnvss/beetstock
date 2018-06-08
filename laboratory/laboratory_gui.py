#!/usr/bin/python3
# Графический интерфейс лаборанта
import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from sql.sql_queries import *
from sql.table_models import samplesModel
from misc.dates import day_shift


class LaboratoryApp(QtWidgets.QWidget):

    def __init__(self):
        super(LaboratoryApp, self).__init__()
        self.window = uic.loadUi("./uis/laboratory_gui.ui")
        # Подключить модель к таблице
        self.window.mainTable.setModel(samplesModel)
        self.window.mainTable.setColumnWidth(0, 50)
        self.window.mainTable.setColumnWidth(1, 120)
        self.window.mainTable.setColumnWidth(2, 120)
        self.window.mainTable.setColumnWidth(3, 50)
        self.window.mainTable.setColumnWidth(4, 50)
        self.window.mainTable.setColumnWidth(5, 50)
        self.window.mainTable.setColumnWidth(6, 150)
        # Значения по умолчанию
        self.selected_sample = 0
        # Установить текущую дату
        self.window.dateEdit.setDate(QtCore.QDate.currentDate())
        self.window.dateEdit.dateChanged.connect(self.date_changed)
        # Переключатель режима редактирования
        self.window.editSwitch.stateChanged.connect(self.edit_mode_change)
        # Отцентровать и показать окно
        self.center(self.window)
        self.window.show()

    # Показать окно по центру экрана
    def center(self, _widget):
        self.widget_size = _widget.frameGeometry()
        self.display_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.widget_size.moveCenter(self.display_center)
        _widget.move(self.widget_size.topLeft())

    # Действие по двойному клику по таблице
    def table_click(self):
        self.selected_sample = [self.window.mainTable.model().data(index)
                                for index in self.window.mainTable.selectedIndexes()][0]
        self.sample_data = get_sample_data(self.selected_sample)
        # TODO: добавить отображение подробностей  по пробе, включая имя поставщика в qlabel
        # добавить форму редактирования (ползунок править таблицу,
        # который переключает edittriggers maintable)

    # Обновить таблицу и графики
    def table_update(self):
        if self.window.mainTable.model() is not None:
            self.window.mainTable.model().select()

    # Действие по смене даты
    def date_changed(self):
        self.shift = day_shift(self.window.dateEdit.date().toPyDate())
        samplesModel.setFilter("sample_dt between '{}' and '{}'".
                               format(self.shift[0], self.shift[1]))
        self.table_update()

    # Переключатель
    def edit_mode_change(self):
        if self.window.editSwitch.isChecked():
            self.window.mainTable.setSelectionBehavior(0)
            self.window.mainTable.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        else:
            self.window.mainTable.setSelectionBehavior(1)
            self.window.mainTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _gui = LaboratoryApp()
    sys.exit(app.exec_())