# -*- coding: utf-8 -*-
# SQL запросы используемые в интерфейсе оператора
from PyQt5.QtSql import QSqlQuery
# import to test query, remove it in release
# from operators_gui.sql.table_models import *

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

# Добавить запись
def record_insert(doc, driver, transport, supplier, loadpoint, unloadpoint, arrival_dt):
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
        suppliers.name
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
    return _data

# Пункт погрузки
def get_loadpoint(name):
    _query = QSqlQuery("SELECT id FROM loadpoints WHERE name = '{}'"
                       .format(name))
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
