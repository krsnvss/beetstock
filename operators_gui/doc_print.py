#!/usr/bin/python3
# Печать ТТН по завершении рейса
import sys
from PyQt5 import QtWidgets, QtPrintSupport, uic
from sql.db_connection import *
from sql.sql_queries import *


class DocPrinter(QtWidgets.QWidget):

    def __init__(self):
        super(DocPrinter, self).__init__()
        self.preview = uic.loadUi('./uis/report.ui')
        self.invoice_print(1400)

    def invoice_print(self, trip_id):
        self.preview.closeAction.triggered.connect(lambda:
            self.preview.close())
        # Получить данные для ТТН
        self.trip_data = get_data(trip_id)
        with open("./rep/invoice_template.html", 'r') as inv_template:
            self.template = inv_template.read()
        self.preview.webView.setHtml(self.template.format(
            self.trip_data[1],
            self.trip_data[16].toString('dd.MM.yyyy'),
            self.trip_data[5],
            self.trip_data[3],
            self.trip_data[4],
            self.trip_data[5],
            self.trip_data[2],
            self.trip_data[6],
            self.trip_data[10],
            self.trip_data[13],
            self.trip_data[15],
            self.trip_data[17],
        )
                                     )
        self.preview.printAction.triggered.connect(self.printer)
        self.preview.show()

    def printer(self):
        self.print_dialog = QtPrintSupport.QPrintDialog()
        if self.print_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.preview.webView.print_(self.print_dialog.printer())
            self.preview.close()


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = DocPrinter()
    sys.exit(application.exec_())