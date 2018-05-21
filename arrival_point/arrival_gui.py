#!/usr/share/python3
# Графический интерфейс терминала в точке отметки прибытия
import sys
from PyQt5 import QtCore, QtWidgets, uic
from datetime import datetime
from operators_gui.sql.db_connection import *
from operators_gui.sql.sql_queries import *


# Основное окно
class ArrivalPoint(QtWidgets.QWidget):

    def __init__(self):
        super(ArrivalPoint, self).__init__()
        # Загрузить форму
        self.mainWindow = uic.loadUi("./uis/arrivalPoint.ui")
        # Подключить действие по нажатию Enter
        self.mainWindow.rfidInput.returnPressed.connect(self.read_rfid)
        self.return_timer = QtCore.QTimer()
        self.return_timer.timeout.connect(self.return_to_input)
        self.return_timer.setInterval(10000)
        # Сохранить текст, чтобы не потерять форматирование
        self.success_header = self.mainWindow.successHeaderLabel.text()
        self.success_middle = self.mainWindow.successMiddleLabel.text()
        self.error_middle = self.mainWindow.errorMiddleLabel2.text()
        self.mainWindow.show()

    # Читать введенный номер карты
    def read_rfid(self):
        self.driver_id = rfid_to_driver(self.mainWindow.rfidInput.text())
        if self.driver_id:
            self.trip_state = trip_status(self.driver_id)
            if self.trip_state[1] == 1 or self.trip_state[1] == 5:
                self.mainWindow.stackedWidget.setCurrentIndex(1)
                self.driver_name = get_driver(self.driver_id)[0]
                self.mainWindow.successHeaderLabel.setText(
                    self.success_header.format(self.driver_name)
                )
                self.mainWindow.successMiddleLabel.setText(
                    self.success_middle.format(datetime.now().strftime("%H:%M:%S"))
                )
                self.check_arrival()
            elif 1 < self.trip_state[1] < 5:
                self.mainWindow.stackedWidget.setCurrentIndex(3)
                self.mainWindow.errorMiddleLabel2.setText(
                    self.error_middle.format(self.trip_state[0])
                )
        else:
            self.mainWindow.stackedWidget.setCurrentIndex(2)
        # Включить таймер для возврата на главную страницу
        self.return_timer.start()
        self.mainWindow.rfidInput.clear()

    # Возврат на главную страницу по таймеру
    def return_to_input(self):
        self.mainWindow.stackedWidget.setCurrentIndex(0)
        self.return_timer.stop()

    # Записать в БД
    def check_arrival(self):
        self.driver_info = get_driver(self.driver_name)
        self.loadpoint = get_default_loadpoint(self.driver_info[2])
        # TODO добавить для прибывших с поля
        if self.trip_state[1] == 1:
            pass
        elif self.trip_state[1] == 5:
            record_insert(0,
                          self.driver_info[0],
                          self.driver_info[1],
                          self.driver_info[2],
                          self.loadpoint,
                          0,
                          QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'),
                          False)


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = ArrivalPoint()
    sys.exit(application.exec_())
