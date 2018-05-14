from PyQt5.QtSql import QSqlQuery
from operators_gui.sql.table_models import *
from operators_gui.sql.sql_queries import *
from datetime import datetime, timedelta
from random import choice, randint, uniform
from time import sleep

def random_dt():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)
    return datetime(year, month, day, hour, minute, second)


def fill_with_completed():
    driver_query = QSqlQuery('''
    select id from drivers''')
    all_drivers = []
    while (driver_query.next()):
        all_drivers.append(driver_query.value(0))
    random_driver = choice(all_drivers)
    driver_data = get_driver(random_driver)
    trip = randint(1, 999999)
    transport = get_transport(driver_data[1])
    supplier = get_supplier(driver_data[3])
    unload_send = choice(list(get_unloads().items()))[1]
    unload_fact = choice(list(get_unloads().items()))[1]
    arrival_dt = random_dt()
    gross_dt = arrival_dt + timedelta(seconds=randint(300, 3600))
    unload_dt = gross_dt + timedelta(seconds=randint(300, 1200))
    tare_dt = gross_dt + timedelta(seconds=randint(300, 1200))
    gross_weight = round(uniform(30.0, 50.0), 2)
    tare_weight = round(uniform(14.0, 19.0), 2)
    net_weight = round((gross_weight - tare_weight), 2)
    _query = QSqlQuery('''
            INSERT INTO trips 
            (trip, driver, transport, supplier, loadpoint, arrival_dt, 
            unload_send, unload_fact, unload_dt, unloaders,
            gross_weight, gross_dt, tare_weight, tare_dt, net_weight)
            VALUES
            ({}, {}, {}, {}, {}, '{}',
            {}, {}, '{}', {}, 
            {}, '{}', {}, '{}', {})'''
                       .format(trip, random_driver, transport, supplier,
                               supplier, arrival_dt, unload_send, unload_fact,
                               unload_dt, unload_fact, gross_weight, gross_dt,
                               tare_weight, tare_dt, net_weight))


def fill_with_incompleted():
    driver_query = QSqlQuery('''
    select id from drivers''')
    all_drivers = []
    while (driver_query.next()):
        all_drivers.append(driver_query.value(0))
    random_driver = choice(all_drivers)
    driver_data = get_driver(random_driver)
    trip = randint(1, 999999)
    transport = get_transport(driver_data[1])
    supplier = get_supplier(driver_data[3])
    unload_send = choice(list(get_unloads().items()))[1]
    arrival_dt = random_dt()
    gross_dt = arrival_dt + timedelta(seconds=randint(300, 3600))
    gross_weight = round(uniform(30.0, 50.0), 2)
    type = randint(1, 2)
    if type == 2:
        unload_dt = gross_dt + timedelta(seconds=randint(300, 1200))
        unload_fact = choice(list(get_unloads().items()))[1]
    else:
        unload_dt = None
        unload_fact = None
    _query = QSqlQuery('''
            INSERT INTO trips 
            (trip, driver, transport, supplier, loadpoint, arrival_dt, 
            unload_send, unload_fact, unload_dt, unloaders,
            gross_weight, gross_dt)
            VALUES
            ({}, {}, {}, {}, {}, '{}',
            {}, {}, '{}', {}, {}, '{}')'''
                       .format(trip, random_driver, transport, supplier,
                               supplier, arrival_dt, unload_send, unload_fact,
                               unload_dt, unload_fact, gross_weight, gross_dt))


def fill_with_inline():
    driver_query = QSqlQuery('''
        select id from drivers''')
    all_drivers = []
    while (driver_query.next()):
        all_drivers.append(driver_query.value(0))
    random_driver = choice(all_drivers)
    driver_data = get_driver(random_driver)
    transport = get_transport(driver_data[1])
    supplier = get_supplier(driver_data[3])
    arrival_dt = random_dt()
    trip = randint(1, 999999)
    _query = QSqlQuery('''
                INSERT INTO trips 
                (trip, driver, transport, supplier, loadpoint, arrival_dt)
                VALUES
                ({}, {}, {}, {}, {}, '{}')'''
                       .format(trip, random_driver, transport, supplier,
                               supplier, arrival_dt))


c = 0
for x in range(100):
    fill_with_completed()
    sleep(5)
    c += 1
    print(c, " records inserted", end='\r')
