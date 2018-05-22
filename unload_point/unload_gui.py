#!/usr/bin/python3
# Графический интерфейс пункта выгрузки
import sys
from PyQt5 import QtCore, QtWidgets, uic
from datetime import datetime
from sql.db_connection import *
from sql.sql_queries import *


# Основное окно
class Unloader(QtWidgets.QWidget):

    def __init__(self):
        super(Unloader, self).__init__()
        # Загрузить форму
        self.mainWindow = uic.loadUi("./uis/unloadPoint.ui")
        self.return_timer = QtCore.QTimer()
        self.return_timer.timeout.connect(self.return_to_input)
        self.return_timer.setInterval(5000)
        # Сохранить текст, чтобы не потерять форматирование
        self.success_middle = self.mainWindow.successMiddleLabel.text()
        self.error_middle = self.mainWindow.errorMiddleLabel2.text()
        self.fill_buttons()
        self.mainWindow.show()

    # Заполнить кнопки
    def fill_buttons(self):
        self.top_six = get_unload_list(1)
        self.layout = QtWidgets.QGridLayout()
        for item in self.top_six:
            self.trip_id = item[0]
            self.driver = get_driver(item[1])[0]
            self.transport = get_driver(item[1])[1]
            self.button = QtWidgets.QPushButton(self.transport)
            self.button.clicked.connect(
                lambda: self.check_unload(self.trip_id)
            )
            self.layout.addWidget(self.button)
        self.mainWindow.groupBox.setLayout(self.layout)


    # Читать введенный номер карты
    def read_rfid(self):
        self.driver_id = rfid_to_driver(
            self.mainWindow.rfidInput.text()
        )
        if self.driver_id:
            self.trip_state = trip_status(self.driver_id)
            if self.trip_state[1] == 2:
                self.check_weight('gross')
                self.show_check_screen()
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
                self.show_check_screen()
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
    def show_check_screen(self):
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

    # Записать в БД
    def check_unload(self, trip_id):
        check_weight(self.trip_state[0],
                     self.weight_type,
                     10,
                     QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
                     )


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = Unloader()
    sys.exit(application.exec_())