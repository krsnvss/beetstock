from operators_gui.sql.sql_queries import *
from operators_gui.sql.table_models import *
from operators_gui.misc.dates import *
from subprocess import Popen


# Create text files for gnuplot
def calculate_totals(shift):
    sums = []
    counts = []
    start_dt = shift[0]
    for _hour in range(1, 25):
        _query = QSqlQuery('''
        SELECT 
        COUNT(*) AS sup, SUM(net_weight)
    FROM
        trips
    WHERE
        tare_dt BETWEEN '{}' AND '{}'
        '''.format(start_dt,
                       start_dt + timedelta(seconds=3600)))
        while (_query.next()):
            counts.append("{} {} {}\n".format(_hour,
                                              int(_query.value(0)),
                                              int(_query.value(1))))
            sums.append("{} {}\n".format(_hour,
                                           int(_query.value(1))))
        start_dt += timedelta(seconds=3600)
        # Clear text files
        with open("plot_data_counts.txt", "w") as plot_txt:
            plot_txt.write('')
        with open("plot_data_sums.txt", "w") as plot_txt:
            plot_txt.write('')
        for row in counts:
            with open("plot_data_counts.txt", "a") as plot_txt:
                plot_txt.write(row)
        for row in sums:
            with open("plot_data_sums.txt", "a") as plot_txt:
                plot_txt.write(row)
    Popen("./plot_maker.sh")
    return True


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


print(calculate_totals(day_shift(datetime.now()-timedelta(days=2))))
