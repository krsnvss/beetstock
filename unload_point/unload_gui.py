#!/usr/bin/python3
# Графический интерфейс пункта выгрузки
import sys
from PyQt5 import QtCore, QtWidgets, uic, QtPrintSupport
from datetime import datetime
from sql.db_connection import *
from sql.sql_queries import *


# Основное окно
class Unloader(QtWidgets.QWidget):

    def __init__(self):
        super(Unloader, self).__init__()
        # Загрузить форму
        self.mainWindow = uic.loadUi("./uis/unloadPoint.ui")
        self.layout = QtWidgets.QGridLayout()
        self.mainWindow.groupBox.setLayout(self.layout)
        # Загрузить настройки
        self.update_interval = 5000
        self.unload_id = 1
        self.unloader_id = 1
        # Установить таймеры:
        # Возврат на начальную страницу
        self.return_timer = QtCore.QTimer()
        self.return_timer.timeout.connect(self.return_to_input)
        self.return_timer.setInterval(self.update_interval)
        # Обновление списка грузовиков на выгрузке
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.fill_buttons)
        self.update_timer.setInterval(self.update_interval)
        self.update_timer.start()
        # Привязать действие к заголовку
        self.mainWindow.lineEdit.addAction(self.mainWindow.changeUnloaders, 1)
        self.mainWindow.changeUnloaders.triggered.connect(self.change_unloaders)
        # Сохранить текст, чтобы не потерять форматирование
        self.success_middle = self.mainWindow.successMiddleLabel.text()
        self.error_middle = self.mainWindow.errorMiddleLabel2.text()
        self.fill_buttons()
        self.mainWindow.show()

    # Заполнить кнопки
    def fill_buttons(self):
        self.top_six = get_unload_list(self.unload_id)
        # Очистить содержимое раскладки
        while self.layout.count():
            self.child = self.layout.takeAt(0)
            if self.child.widget():
                self.child.widget().deleteLater()
        # Заполнить раскладку
        for item in self.top_six:
            self.trip_id = item[0]
            self.driver = get_driver(item[1])[0]
            self.transport = get_driver(item[1])[1]
            self.button = QtWidgets.QPushButton(
                "{} / {}".format(
                    self.trip_id,
                    self.transport
                )
            )
            self.button.clicked.connect(self.click_button)
            self.layout.addWidget(self.button)

    # Нажатие кнопки
    def click_button(self):
        self.unload_check(self.sender().text().replace("&", "").split(" / ")[0])
        self.sender().setVisible(False)

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
    def unload_check(self, trip_id):
        self.trip_id = trip_id
        check_unload(
            self.trip_id,
            self.unload_id,
            self.unloader_id,
            QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        )

    # Смена бригады выгрузчиков
    def change_unloaders(self):
        print("change!")


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = Unloader()
    sys.exit(application.exec_())