# -*- coding: utf-8 -*-
# SQL запросы используемые в интерфейсе оператора
from PyQt5.QtSql import QSqlQuery
from statistics import median

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
    if len(_data) > 0:
        return _data[0]
    else:
        return "Выгрузка не назначена"


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
        drivers.photo,
        drivers.rfid
    FROM
        drivers,
        transport,
        suppliers
    WHERE
        drivers.id = {}
            AND transport.id = drivers.transport
            AND suppliers.id = drivers.employer'''.
                           format(driver_id_or_name))
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
            _data.append(_query.value(8))
    return _data


# Пункт погрузки
def get_loadpoint(id_or_name):
    if type(id_or_name) is str:
        _query = QSqlQuery("SELECT id FROM loadpoints WHERE name = '{}'"
                           .format(id_or_name))
        _data = []
        while _query.next():
            _data.append(_query.value(0))
        return _data[0]
    elif type(id_or_name) is int:
        _query = QSqlQuery("SELECT name FROM loadpoints WHERE id = {}"
                           .format(id_or_name))
        _data = []
        while _query.next():
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


# Получить полные сведения о поставщике
def get_supplier_data(_id):
    _query = QSqlQuery('''
    SELECT 
    name,
    full_name,
    email,
    phone,
    requisites,
    transporter_only,
    default_load
    FROM
    suppliers
    WHERE id = {}'''.format(_id))
    _data = []
    while _query.next():
        _data.append(_query.value(0))
        _data.append(_query.value(1))
        _data.append(_query.value(2))
        _data.append(_query.value(3))
        _data.append(_query.value(4))
        _data.append(_query.value(5))
        _data.append(_query.value(6))
    return _data


# Записать водителя
def set_supplier(_id, name, full_name, phone, email, requisites, transporter_only, default_load, insert):
    if insert:
         _query = QSqlQuery('''
        insert into suppliers 
        (name, full_name. phone, email, requisites, transporter_only, default_load) 
        values ('{}', '{}', '{}', '{}', '{}', {}, {})'''.format(
            name, full_name, phone, email, requisites, transporter_only, default_load
        )
        )
    else:
         _query = QSqlQuery('''
        update suppliers
            set name = '{}',
                full_name = '{}',
                phone = '{}',
                email = '{}',
                requisites = '{}',
                transporter_only = {},
                default_load = {}
        where id = {}'''.format(
             name, full_name, phone, email, requisites, transporter_only, default_load, _id
        )
        )
    return True


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


# Отметить выгрузку
def check_unload(trip_id, unload_fact, unloaders, unload_dt):
    _query = QSqlQuery('''
        UPDATE trips 
        SET 
            unload_fact = {},
            unloaders = {},
            unload_dt = '{}'
        WHERE
            id = {}'''.format(
        unload_fact,
        unloaders,
        unload_dt,
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
    AND gross_weight > 0
    ORDER BY gross_dt ASC
    LIMIT 6'''.format(unload_id))
    _data = []
    while _query.next():
        _data.append([_query.value(0),
                      _query.value(1),
                      _query.value(2)])
    return _data


# получить сведения о бригаде выгрузчиков
def get_unloaders(rfid):
    _query = QSqlQuery('''
        SELECT 
        id, name, assistant1, assistant2, assistant3, unload_point
        FROM
        unloaders
        WHERE
        rfid = {}'''.format(rfid))
    _data = []
    while _query.next():
        _data.append(_query.value(0))
        _data.append(_query.value(1))
        _data.append(_query.value(2))
        _data.append(_query.value(3))
        _data.append(_query.value(4))
        _data.append(_query.value(5))
    return _data


# Получить список каждых n записей для направления на анализы
def get_lab_line(ordinal, supplier, loadpoint, dt_start, dt_end):
    _query = QSqlQuery('''
    SELECT 
    id
    FROM
        trips
    WHERE
        supplier = {} AND loadpoint = {}
            AND arrival_dt BETWEEN '{}' AND '{}'
    '''.format(
        supplier,
        loadpoint,
        dt_start,
        dt_end
    ))
    _data = []
    row_number = 0
    while _query.next():
        if row_number % ordinal == 0:
            _data.append(_query.value(0))
        row_number += 1
    return _data


# Поставить номер пробы
def create_sample():
    insert_query = QSqlQuery('''INSERT INTO samples (refuse) values (0)''')
    return True


# Поставить дату пробы
def set_sample_dt(sample_id, dt):
    _query = QSqlQuery('''
    UPDATE samples 
    SET sample_dt = '{}'
    WHERE id = {}
    '''.format(
        dt,
        sample_id
    )
    )
    return True


# Получить номер последней пробы
def get_last_sample_number():
    select_query = QSqlQuery('''
    SELECT 
    id
    FROM
    samples
    ORDER BY id DESC
    LIMIT 1''')
    last_sample = int()
    while select_query.next():
        last_sample = select_query.value(0)
    return last_sample


# Добавить номер пробы
def set_sample_number(trip_id, sample_id):
    update_query = QSqlQuery('''
        UPDATE trips 
        SET 
        sample = {}
        WHERE
        id = {}'''.format(
        sample_id,
        trip_id
    ))
    return True


# Проверить нужно ли отправлять на пробу
def get_sample_id(trip_id):
    _query = QSqlQuery('''
    SELECT
    sample
    FROM
    trips
    WHERE
    id = {}
    '''.format(
        trip_id
    ))
    sample_id = 0
    while _query.next():
        sample_id = _query.value(0)
    return sample_id


# Получить данные по пробе
def get_sample_data(_id):
    _query = QSqlQuery('''
    SELECT
    refuse,
    polarisation,
    k,
    n,
    an
    FROM
    samples
    WHERE
    id = {}
    '''.format(_id))
    _data = []
    while _query.next():
        _data.append(_query.value(0))
        _data.append(_query.value(1))
        _data.append(_query.value(2))
        _data.append(_query.value(3))
        _data.append(_query.value(4))
    return _data


# Записать водителя
def set_driver(_id, name, phone, email, comment, photo, transport, employer, rfid, insert):
    if insert:
        _query = QSqlQuery('''
        insert into drivers 
        (name, phone, email, comment, photo,transport, employer, rfid) 
        values ('{}', '{}', '{}', '{}', {}, {}, {}, {})'''.format(
            name, phone, email, comment, photo, transport, employer, rfid
        )
        )
    else:
         _query = QSqlQuery('''
        update drivers 
            set name = '{}',
                phone = '{}',
                email = '{}',
                comment = '{}',
                photo = {},
                transport = {},
                employer = {},
                rfid = {}
        where id = {}'''.format(
            name, phone, email, comment, photo, transport, employer, rfid, _id
        )
        )

    return True


# Получить фото по id
def get_photo(id):
    _query = QSqlQuery('''
    SELECT
    photo
    FROM
    photos
    WHERE
    id = {}
    '''.format(id))
    path_to_photo = ''
    while _query.next():
        path_to_photo = _query.value(0)
    return path_to_photo


# Добавить фото
def add_photo(url):
    _query = QSqlQuery('''
    insert into photos (photo) values ('{}')'''.format(url))
    select_query = QSqlQuery('''
        SELECT 
        id
        FROM
        photos
        ORDER BY id DESC
        LIMIT 1''')
    last_photo = int()
    while select_query.next():
        last_photo = select_query.value(0)
    return last_photo


# Рассчитать зачетный вес
def set_clear_weight(_date, supplier, refuse):
    _query = QSqlQuery('''
    update trips
    set clear_weight = net_weight * (100 - {})/100
    WHERE
    tare_dt BETWEEN '{}' AND '{}'
    AND supplier = {}
    '''.format(
        refuse,
        _date[0],
        _date[1],
        supplier
    )
    )
    return True


# Получить данные по хозяйствам для отчета
def get_daily_totals(_date):
    sup_query = QSqlQuery('''
    SELECT DISTINCT
    supplier
    FROM
    trips
    WHERE
    tare_dt BETWEEN '{}' AND '{}'
    '''.format(
        _date[0],
        _date[1]
    )
    )
    _suppliers = []
    while sup_query.next():
        _suppliers.append(sup_query.value(0))
    _totals = []
    for item in _suppliers:
        sup_totals = []
        samples = []
        _query = QSqlQuery('''
                        SELECT sample
                        FROM trips
                        WHERE tare_dt BETWEEN '{}' AND '{}'
                        AND supplier = {} AND sample > 0
                        '''.format(
            _date[0],
            _date[1],
            item
        )
        )
        while _query.next():
            samples.append(_query.value(0))
        refuse = []
        polarisation = []
        for sample in samples:
            samples_query = QSqlQuery('''
                            select refuse, polarisation
                            from samples
                            where id = {}'''.format(
                sample
            ))
            while samples_query.next():
                refuse.append(samples_query.value(0))
                polarisation.append(samples_query.value(1))
        refuse_value = median(refuse)
        polarisation_value = median(polarisation)
        sup_totals.append(refuse_value)
        sup_totals.append(polarisation_value)
        _totals.append(sup_totals)
        # Перезаписать значения в БД
        set_clear_weight(_date, item, refuse_value)
        _query = QSqlQuery('''
        SELECT
        suppliers.full_name,
        COUNT(trips.id),
        SUM(trips.net_weight),
        SUM(trips.clear_weight)
        FROM
        suppliers,
        trips
        WHERE
        suppliers.id = trips.supplier
        AND tare_dt BETWEEN '{}' AND '{}'
        AND supplier = {}
        '''.format(
            _date[0],
            _date[1],
            item
            )
        )
        while _query.next():
            sup_totals.append(_query.value(0))
            sup_totals.append(_query.value(1))
            sup_totals.append(_query.value(2))
            sup_totals.append(_query.value(3))
    return _totals