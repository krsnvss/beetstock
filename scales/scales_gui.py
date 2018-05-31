#!/usr/bin/python3
# Графический интерфейс весового терминала
import sys
from PyQt5 import QtCore, QtWidgets, uic
from datetime import datetime
from sql.db_connection import *
from sql.sql_queries import *
from random import uniform


# Основное окно
class Scales(QtWidgets.QWidget):

    def __init__(self):
        super(Scales, self).__init__()
        # Загрузить форму
        self.mainWindow = uic.loadUi("./uis/scaleTerminal.ui")
        # Подключить действие по нажатию Enter
        self.mainWindow.rfidInput.returnPressed.connect(self.read_rfid)
        self.return_timer = QtCore.QTimer()
        self.return_timer.timeout.connect(self.return_to_input)
        self.return_timer.setInterval(10000)
        # Сохранить текст, чтобы не потерять форматирование
        self.success_header = self.mainWindow.successHeaderLabel.text()
        self.success_middle = self.mainWindow.successMiddleLabel.text()
        self.success_header_2 = self.mainWindow.successHeaderLabel_2.text()
        self.success_middle_2 = self.mainWindow.successMiddleLabel_2.text()
        self.error_middle = self.mainWindow.errorMiddleLabel2.text()
        # Окно без заголовка
        self.mainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        # При открытии окна, оно будет развернуто на всю доступную область
        self.mainWindow.setGeometry(QtWidgets.QDesktopWidget().availableGeometry())
        self.mainWindow.show()

    # Читать введенный номер карты
    def read_rfid(self):
        self.driver_id = rfid_to_driver(
            self.mainWindow.rfidInput.text()
        )
        if self.driver_id:
            self.trip_state = trip_status(self.driver_id)
            if self.trip_state[1] == 2:
                self.check_weight('gross')
                self.show_check_screen('gross')
                self.send_to_lab()
            elif self.trip_state[1] == 3:
                self.mainWindow.stackedWidget.setCurrentIndex(3)
                self.mainWindow.errorMiddleLabel2.setText(
                    self.error_middle.format(
                        get_unload_send(
                            self.trip_state[0]
                        )
                    )
                )
            elif self.trip_state[1] == 4:
                self.check_weight('tare')
                self.show_check_screen('tare')
            elif self.trip_state[1] == 5:
                self.mainWindow.stackedWidget.setCurrentIndex(4)
        else:
            self.mainWindow.stackedWidget.setCurrentIndex(2)
        # Включить таймер для возврата на главную страницу
        self.return_timer.start()
        self.mainWindow.rfidInput.clear()

    # Возврат на главную страницу по таймеру
    def return_to_input(self):
        self.mainWindow.stackedWidget.setCurrentIndex(0)
        self.return_timer.stop()

    # Показать окно отметки
    def show_check_screen(self, weight_type):
        self.weight_type = weight_type
        if self.weight_type == 'gross':
            self.mainWindow.stackedWidget.setCurrentIndex(1)
            self.driver_name = get_driver(self.driver_id)[0]
            self.mainWindow.successHeaderLabel.setText(
                self.success_header.format(self.driver_name)
            )
            self.mainWindow.successMiddleLabel.setText(
                self.success_middle.format(datetime.now().strftime("%H:%M:%S"),
                                           get_unload_send(self.trip_state[0])
                                           )
            )
        elif self.weight_type == 'tare':
            self.mainWindow.stackedWidget.setCurrentIndex(5)
            self.driver_name = get_driver(self.driver_id)[0]
            self.mainWindow.successHeaderLabel_2.setText(
                self.success_header_2.format(self.driver_name)
            )
            self.mainWindow.successMiddleLabel_2.setText(
                self.success_middle_2.format(datetime.now().strftime("%H:%M:%S"))
            )

    # Записать в БД
    def check_weight(self, weight_type):
        self.weight_type = weight_type
        check_weight(self.trip_state[0],
                     self.weight_type,
                     round(uniform(10.0, 50.0), 2),
                     QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
                     )

    # Отправить сообщение в лабораторию
    def send_to_lab(self):
        if get_sample_id(self.trip_state[0]) > 0:
            print("Quick! Do something! Make this manipulator move! This is sample", self.trip_state[0])
        else:
            print("Nothing to do. It's", self.trip_state[0])


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = Scales()
    sys.exit(application.exec_())