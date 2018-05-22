# -*- coding: utf-8 -*-
# SQL запросы используемые в интерфейсе оператора
from PyQt5.QtSql import QSqlQuery


# Данные о рейсе для форм редактирования
def get_data(record_id):
    _query = QSqlQuery('''
    SELECT 
    trips.id AS tripid,
    trips.trip AS tripnumber,
    drivers.name AS drivername,
    transport.plate AS transportplate,
    transport.trailer AS transporttrailer,
    suppliers.full_name AS suppliername,
    loadpoints.name AS loadpointname,
    trips.load_dt AS loaddatetime,
    trips.arrival_dt AS arrivaldatetime,
    unloadpoints.name AS unloadsend,
    unloadpoints.name AS unloadfact,
    trips.unload_dt AS unloaddatetime,
    unloaders.name AS unloadersname,
    trips.gross_weight AS grossweight,
    trips.gross_dt AS grossdt,
    trips.tare_weight AS tareweight,
    trips.tare_dt AS taredt,
    trips.net_weight AS netweight
FROM
    trips,
    drivers,
    transport,
    suppliers,
    loadpoints,
    unloadpoints,
    unloaders
WHERE
    drivers.id = trips.driver
        AND transport.id = trips.transport
        AND suppliers.id = trips.supplier
        AND loadpoints.id = trips.loadpoint
        AND unloadpoints.id = trips.unload_send
        AND unloaders.id = trips.unloaders
        AND trips.id = {}'''.format(record_id))
    _data = []
    while(_query.next()):
        for index in range(0, 18):
            _data.append(_query.value(index))
    if len(_data) > 0:
        return _data
    elif len(_data) == 0:
        _query = QSqlQuery('''
            SELECT 
    trips.id AS tripid,
    trips.trip AS tripnumber,
    drivers.name AS drivername,
    transport.plate AS transportplate,
    transport.trailer AS transporttrailer,
    suppliers.full_name AS suppliername,
    loadpoints.name AS loadpointname
FROM
    trips,
    drivers,
    transport,
    suppliers,
    loadpoints
WHERE
    drivers.id = trips.driver
        AND transport.id = trips.transport
        AND suppliers.id = trips.supplier
        AND loadpoints.id = trips.loadpoint
        AND trips.id = {}'''.format(record_id))
        _data = []
        while (_query.next()):
            for index in range(0, 18):
                _data.append(_query.value(index))
        return _data


# Список выгрузок для выпадающего списка
def get_unloads():
    _query = QSqlQuery("SELECT id, name FROM unloadpoints")
    _data = {}
    while (_query.next()):
        _data[_query.value(1)] = _query.value(0)
    return _data


# Имя пункта погрузки
def get_unload_send(trip_id):
    _query = QSqlQuery('''
    SELECT 
    unloadpoints.name
    FROM
    trips,
    unloadpoints
    WHERE
    trips.unload_send = unloadpoints.id
        AND trips.id = {}
    '''.format(trip_id))
    _data = []
    while (_query.next()):
        _data.append(_query.value(0))
    return _data[0]


# Добавить запись
def record_insert(doc, driver, transport, supplier, loadpoint, unloadpoint, arrival_dt, full):
    if full:
        _query = QSqlQuery('''
    INSERT INTO trips 
    (trip,
    driver,
    transport,
    supplier,
    loadpoint,
    unload_send,
    arrival_dt)
    VALUES
    ({}, {}, {}, {}, {}, {}, '{}')'''.format(doc,
                                             driver,
                                             transport,
                                             supplier,
                                             loadpoint,
                                             unloadpoint,
                                             arrival_dt))
    else:
        _query = QSqlQuery('''
            INSERT INTO trips 
            (trip,
            driver,
            transport,
            supplier,
            loadpoint,
            arrival_dt)
            VALUES
            ({}, {}, {}, {}, {}, '{}')'''.format(doc,
                                                 driver,
                                                 transport,
                                                 supplier,
                                                 loadpoint,
                                                 arrival_dt))
    return True


# Обновить запись
def record_update(doc, driver, transport, supplier, loadpoint, unloadpoint, record_id):
    _query = QSqlQuery('''
    UPDATE trips 
SET 
    trip = {},
    driver = {},
    transport = {},
    supplier = {},
    loadpoint = {},
    unload_send = {}
WHERE
    id = {}'''.format(doc,
                      driver,
                      transport,
                      supplier,
                      loadpoint,
                      unloadpoint,
                      record_id))
    return True


# Установить пункт выгрузки
def set_unload(unloadpoint, record_id):
    _query = QSqlQuery('''
    UPDATE trips 
SET 
    unload_send = {}
WHERE
    id = {}'''.format(unloadpoint,
                      record_id))
    return True


# Список водителей
def get_driver(driver_id_or_name):
    if type(driver_id_or_name) is str:
        _query = QSqlQuery("SELECT id, transport, employer FROM drivers WHERE name = '{}'"
                           .format(driver_id_or_name))
        _data = []
        while (_query.next()):
            _data.append(_query.value(0))
            _data.append(_query.value(1))
            _data.append(_query.value(2))
    elif type(driver_id_or_name) is int:
        _query = QSqlQuery('''SELECT 
        drivers.name,
        transport.plate,
        transport.trailer,
        suppliers.name,
        drivers.phone,
        drivers.email,
        drivers.comment,
        drivers.photo
    FROM
        drivers,
        transport,
        suppliers
    WHERE
        drivers.id = {}
            AND transport.id = drivers.transport
            AND suppliers.id = drivers.employer'''
                               .format(driver_id_or_name))
        _data = []
        while (_query.next()):
            _data.append(_query.value(0))
            _data.append(_query.value(1))
            _data.append(_query.value(2))
            _data.append(_query.value(3))
            _data.append(_query.value(4))
            _data.append(_query.value(5))
            _data.append(_query.value(6))
            _data.append(_query.value(7))
    return _data


# Пункт погрузки
def get_loadpoint(name):
    _query = QSqlQuery("SELECT id FROM loadpoints WHERE name = '{}'"
                       .format(name))
    _data = []
    while (_query.next()):
        _data.append(_query.value(0))
    return _data[0]


# Пункт погрузки по умолчанию
def get_default_loadpoint(supplier_id):
    _query = QSqlQuery("SELECT default_load FROM suppliers WHERE id = {}"
                       .format(supplier_id))
    _data = []
    while (_query.next()):
        _data.append(_query.value(0))
    return _data[0]


# Выбрать водителя по карте
def rfid_to_driver(rfid):
    _query = QSqlQuery("SELECT id FROM drivers WHERE rfid = {}"
                       .format(rfid))
    _data = []
    while (_query.next()):
        _data.append(_query.value(0))
    if len(_data) > 0:
        return _data[0]
    else:
        return False


# Поставщик
def get_supplier(name):
    _query = QSqlQuery("SELECT id FROM suppliers WHERE full_name = '{}'"
                       .format(name))
    _data = []
    while (_query.next()):
        _data.append(_query.value(0))
    if len(_data) == 0:
        _query = QSqlQuery("SELECT id FROM suppliers WHERE name = '{}'"
                           .format(name))
        _data = []
        while (_query.next()):
            _data.append(_query.value(0))
    return _data[0]


def get_supplier_name(id):
    _query = QSqlQuery("SELECT name FROM suppliers WHERE id = '{}'"
                       .format(id))
    _data = []
    while (_query.next()):
        _data.append(_query.value(0))
    return _data[0]


# Транспорт
def get_transport(name):
    _query = QSqlQuery("SELECT id FROM transport WHERE plate = '{}'"
                       .format(name))
    _data = []
    while (_query.next()):
        _data.append(_query.value(0))
    return _data[0]


# Добавить водителя
def insert_driver(name, transport, employer, rfid):
    _query = QSqlQuery('''
        INSERT INTO drivers 
        (name,
        transport,
        employer,
        rfid)
        VALUES
        ('{}', {}, {}, {})'''.format(name,
                                     transport,
                                     employer,
                                     rfid))
    return True


# Состояние рейса
# 0 - нет рейсов для этого водителя
# 1 - есть загрузка, не прибыл
# 2 - прибыл, нет брутто
# 3 - есть брутто, нет выгрузки
# 4 - есть выгрузка, нет тары
# 5 - рейс завершен
def trip_status(driver_id):
    _query = QSqlQuery('''
    SELECT 
    load_dt, arrival_dt, gross_dt, unload_dt, tare_dt, id
    FROM
    trips
    WHERE
    driver = {} order by arrival_dt desc limit 1
    '''.format(driver_id))
    _data = []
    while _query.next():
        _data.append(_query.value(0))
        _data.append(_query.value(1))
        _data.append(_query.value(2))
        _data.append(_query.value(3))
        _data.append(_query.value(4))
        _data.append(_query.value(5))
    if len(_data) == 6:
        if _data[1].isNull():
            status = 1
        elif _data[2].isNull():
            status = 2
        elif _data[3].isNull():
            status = 3
        elif _data[4].isNull():
            status = 4
        else:
            status = 5
    else:
        status = 0
    return [_data[5], status]


# Отметить брутто
def check_weight(trip_id, weight_type, weight, weight_dt):
    if weight_type == 'gross':
        _query = QSqlQuery('''
        UPDATE trips 
        SET 
            gross_weight = {},
            gross_dt = '{}'
        WHERE
            id = {}'''.format(
            weight,
            weight_dt,
            trip_id)
        )
    elif weight_type == 'tare':
        _query = QSqlQuery('''
        UPDATE trips 
                SET 
                    tare_weight = {},
                    tare_dt = '{}',
                    net_weight = gross_weight - tare_weight
                WHERE
                    id = {}'''.format(
            weight,
            weight_dt,
            trip_id)
        )


# Список машин на выгрузке
def get_unload_list(unload_id):
    _query = QSqlQuery('''
    SELECT 
    id, driver, transport
    FROM
    trips
    WHERE
    unload_send = {} AND unload_dt IS NULL
    ORDER BY gross_dt ASC
    LIMIT 6'''.format(unload_id))
    _data = []
    while _query.next():
        _data.append([_query.value(0),
                      _query.value(1),
                      _query.value(2)])
    return _data

#from operators_gui.sql.db_connection import *
#print(trip_status(1))
