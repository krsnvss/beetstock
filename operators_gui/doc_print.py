#!/usr/bin/python3
# Печать ТТН по завершении рейса
import sys
from PyQt5 import QtWidgets, QtPrintSupport, uic
from PyQt5.QtCore import QThread, QDateTime
from sql.db_connection import *
from sql.sql_queries import *


class DocPrinter(QtWidgets.QWidget):

    def __init__(self):
        super(DocPrinter, self).__init__()
        self.preview = uic.loadUi('./uis/report.ui')
        self.preview.printAction.triggered.connect(self.printer)
        # self.invoice_print()

    def invoice_print(self, trip_id):
        self.trip_id = trip_id
        self.preview.closeAction.triggered.connect(lambda:
            self.preview.destroy())
        # Получить данные для ТТН
        self.trip_data = get_data(self.trip_id)
        with open("./rep/invoice_template.html", 'r') as inv_template:
            self.template = inv_template.read()
        self.preview.webView.setHtml(self.template.format(
            QDateTime.currentDateTime().toString('hh:mm:ss dd.MM.yyyy'),
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
        # self.preview.printAction.triggered.connect(self.printer)
        self.preview.show()

    def common_report(self, _date):
        self._date = _date
        self.totals = get_daily_totals(self._date)
        with open("./rep/daily_totals.html", 'r') as _template:
            self.template = _template.read()
        with open("./rep/daily_totals_odd_row.html", 'r') as _template:
            self.odd_row_template = _template.read()
        with open("./rep/daily_totals_even_row.html", 'r') as _template:
            self.even_row_template = _template.read()
        self.rows = ''
        self.row_num = 1
        for item in self.totals:
            if (self.row_num % 2) == 0:
                self.row_template = self.even_row_template
            else:
                self.row_template = self.odd_row_template
            self.rows += self.row_template.format(
                item[2],
                item[3],
                round(item[4], 2),
                round(item[5], 2),
                item[0],
                item[1]
            )
            self.row_num += 1
        self.preview.webView.setHtml(
            self.template.format(
                _date[0],
                _date[1],
                self.rows
            )
        )
        self.preview.show()


    def printer(self):
        self.print_dialog = QtPrintSupport.QPrintDialog()
        if self.print_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.preview.webView.print_(self.print_dialog.printer())
            self.preview.close()


class ThreadPrinter(QThread):

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    def run(self, trip_id):
        self.trip_id = trip_id
        self.printer = DocPrinter(self.trip_id)


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = DocPrinter()
    sys.exit(application.exec_())