from operators_gui.sql.sql_queries import *
from operators_gui.sql.table_models import *
from operators_gui.misc.dates import *
from subprocess import Popen
from PyQt5.QtCore import QThread


class Plotter(QThread):

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)

    # Create text files for gnuplot
    def run(self):
        self.shift = day_shift(datetime.now())
        self.sums = []
        self.counts = []
        self.start_dt = self.shift[0]
        for _hour in range(1, 25):
            _query = QSqlQuery('''
            SELECT 
            COUNT(*) AS sup, SUM(net_weight)
        FROM
            trips
        WHERE
            tare_dt BETWEEN '{}' AND '{}'
            '''.format(self.start_dt,
                       self.start_dt + timedelta(seconds=3600)))
            while (_query.next()):
                self.counts.append("{} {} {}\n".format(_hour,
                                                       int(_query.value(0)),
                                                       int(_query.value(1))))
            self.start_dt += timedelta(seconds=3600)
            # Clear text files
            with open("plot_data_counts.txt", "w") as plot_txt:
                plot_txt.write('')
            for row in self.counts:
                with open("plot_data_counts.txt", "a") as plot_txt:
                    plot_txt.write(row)
        Popen("./plot_maker.sh")


    def calculate_totals_by_supplier(supplier, shift):
        totals = []
        start_dt = shift[0]
        supplier_name = get_supplier_name(supplier)
        for _hour in range(1, 25):
            _query = QSqlQuery('''
            SELECT 
            COUNT(*) AS sup, SUM(net_weight)
        FROM
            trips
        WHERE
            supplier = {}
                AND tare_dt BETWEEN '{}' AND '{}'
                '''.format(supplier,
                           start_dt,
                           start_dt + timedelta(seconds=3600)))
            while (_query.next()):
                totals.append("{} {}\n".format(_hour,
                                                int(_query.value(0))))
            start_dt += timedelta(seconds=3600)
            with open("plot_data.txt", "w") as plot_txt:
                plot_txt.write('')
            for row in totals:
                with open("plot_data.txt", "a") as plot_txt:
                    plot_txt.write(row)
        return totals


#print(calculate_totals(day_shift(datetime.now()-timedelta(days=2))))
