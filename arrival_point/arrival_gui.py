#!/usr/bin/python3
# Графический интерфейс терминала в точке отметки прибытия
import sys
from PyQt5 import QtCore, QtWidgets, uic
from sql.db_connection import *
from sql.sql_queries import *
from misc.dates import *


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
        # Окно без заголовка
        self.mainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        # При открытии окна, оно будет развернуто на всю доступную область
        self.mainWindow.setGeometry(QtWidgets.QDesktopWidget().availableGeometry())
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
                    self.success_middle.format(QtCore.QDateTime.currentDateTime().toString("hh:mm:ss"))
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
            self.trip_state = trip_status(self.driver_id)
            if self.trip_state[1] == 1 or self.trip_state[1] == 2:
                self.lab_line = get_lab_line(
                    2,
                    self.driver_info[2],
                    self.loadpoint,
                    shift_time(datetime.now())[0],
                    shift_time(datetime.now())[1]
                )
                if len(self.lab_line) > 0:
                    if (self.trip_state[0] in self.lab_line) or (self.trip_state[0] == self.lab_line[0]):
                        print("to the laboratory!")
                    else:
                        print("good news, everyone! It's", self.trip_state[0], " of", self.lab_line)

    # Направить на отбор пробы
    def set_sample(self, trip_id):
        pass


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = ArrivalPoint()
    sys.exit(application.exec_())
