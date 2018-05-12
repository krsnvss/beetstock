from operators_gui.sql.sql_queries import *
from operators_gui.sql.table_models import *
from operators_gui.misc.dates import *


def calculate_totals(supplier, shift):
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


for x in range(1,3):
    for y in calculate_totals(x, day_shift(datetime.now())):
        print(y)
