# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlDatabase, QSqlRelation, QSqlRelationalTableModel, QSqlTableModel
from PyQt5 import QtCore

# Подключение к базе данных и модели таблиц

# База данных
db_name = 'beetcount'
db_user = 'root'
db_password = ''
db_host = 'localhost'

# Подключение к базе данных
db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName(db_host)
db.setDatabaseName(db_name)
db.setUserName(db_user)
db.setPassword(db_password)
db.open()

# Модель таблицы "Рейсы"
tripsModel = QSqlRelationalTableModel()
tripsModel.setTable("trips")
tripsModel.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)
# Добавляем связи для отображения имен вместо идентификаторов
tripsModel.setRelation(2, QSqlRelation('drivers', 'id', 'name'))
tripsModel.setRelation(3, QSqlRelation('transport', 'id', 'plate'))
tripsModel.setRelation(4, QSqlRelation('suppliers', 'id', 'name'))
tripsModel.setRelation(5, QSqlRelation('loadpoints', 'id', 'name'))
tripsModel.setRelation(9, QSqlRelation('unloadpoints', 'id', 'name'))
tripsModel.setRelation(10, QSqlRelation('unloadpoints', 'id', 'name'))
tripsModel.setRelation(12, QSqlRelation('unloaders', 'id', 'name'))
# Сортрируем записи по возрастанию в колонке "Номер документа"
tripsModel.setSort(0, QtCore.Qt.AscendingOrder)
tripsModel.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
tripsModel.setHeaderData(1, QtCore.Qt.Horizontal, "Документ")
tripsModel.setHeaderData(2, QtCore.Qt.Horizontal, "Водитель")
tripsModel.setHeaderData(3, QtCore.Qt.Horizontal, "Транспорт")
tripsModel.setHeaderData(4, QtCore.Qt.Horizontal, "Поставщик")
tripsModel.setHeaderData(5, QtCore.Qt.Horizontal, "Поле")
tripsModel.setHeaderData(6, QtCore.Qt.Horizontal, "Загружен")
tripsModel.setHeaderData(7, QtCore.Qt.Horizontal, "Прибыл")
tripsModel.setHeaderData(8, QtCore.Qt.Horizontal, "Прибыл, фото")
tripsModel.setHeaderData(9, QtCore.Qt.Horizontal, "Направлен")
tripsModel.setHeaderData(10, QtCore.Qt.Horizontal, "Выгрузка")
tripsModel.setHeaderData(11, QtCore.Qt.Horizontal, "Время выгрузки")
tripsModel.setHeaderData(12, QtCore.Qt.Horizontal, "Выгрузчики")
tripsModel.setHeaderData(13, QtCore.Qt.Horizontal, "Брутто")
tripsModel.setHeaderData(14, QtCore.Qt.Horizontal, "Брутто, время")
tripsModel.setHeaderData(15, QtCore.Qt.Horizontal, "Брутто, фото")
tripsModel.setHeaderData(16, QtCore.Qt.Horizontal, "Тара")
tripsModel.setHeaderData(17, QtCore.Qt.Horizontal, "Тара, время")
tripsModel.setHeaderData(18, QtCore.Qt.Horizontal, "Тара, фото")
tripsModel.setHeaderData(19, QtCore.Qt.Horizontal, "Нетто")
tripsModel.setHeaderData(20, QtCore.Qt.Horizontal, "Проба")
tripsModel.setHeaderData(21, QtCore.Qt.Horizontal, "Зачет")
tripsModel.select()

# Модель таблицы "Незавершенные рейсы"
incompleteModel = QSqlRelationalTableModel()
incompleteModel.setTable("trips")
incompleteModel.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)
# Добавляем связи для отображения имен вместо идентификаторов
incompleteModel.setRelation(2, QSqlRelation('drivers', 'id', 'name'))
incompleteModel.setRelation(3, QSqlRelation('transport', 'id', 'plate'))
incompleteModel.setRelation(4, QSqlRelation('suppliers', 'id', 'name'))
incompleteModel.setRelation(5, QSqlRelation('loadpoints', 'id', 'name'))
incompleteModel.setRelation(9, QSqlRelation('unloadpoints', 'id', 'name'))
# Сортрируем записи по возрастанию в колонке "Номер документа"
incompleteModel.setSort(0, QtCore.Qt.AscendingOrder)
incompleteModel.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
incompleteModel.setHeaderData(1, QtCore.Qt.Horizontal, "Документ")
incompleteModel.setHeaderData(2, QtCore.Qt.Horizontal, "Водитель")
incompleteModel.setHeaderData(3, QtCore.Qt.Horizontal, "Транспорт")
incompleteModel.setHeaderData(4, QtCore.Qt.Horizontal, "Поставщик")
incompleteModel.setHeaderData(5, QtCore.Qt.Horizontal, "Поле")
incompleteModel.setHeaderData(6, QtCore.Qt.Horizontal, "Загружен")
incompleteModel.setHeaderData(7, QtCore.Qt.Horizontal, "Прибыл")
incompleteModel.setHeaderData(8, QtCore.Qt.Horizontal, "Прибыл, фото")
incompleteModel.setHeaderData(9, QtCore.Qt.Horizontal, "Направлен")
incompleteModel.setHeaderData(10, QtCore.Qt.Horizontal, "Выгрузка")
incompleteModel.setHeaderData(11, QtCore.Qt.Horizontal, "Время выгрузки")
incompleteModel.setHeaderData(12, QtCore.Qt.Horizontal, "Выгрузчики")
incompleteModel.setHeaderData(13, QtCore.Qt.Horizontal, "Брутто")
incompleteModel.setHeaderData(14, QtCore.Qt.Horizontal, "Брутто, время")
incompleteModel.setHeaderData(15, QtCore.Qt.Horizontal, "Брутто, фото")
incompleteModel.setHeaderData(16, QtCore.Qt.Horizontal, "Тара")
incompleteModel.setHeaderData(17, QtCore.Qt.Horizontal, "Тара, время")
incompleteModel.setHeaderData(18, QtCore.Qt.Horizontal, "Тара, фото")
incompleteModel.setHeaderData(19, QtCore.Qt.Horizontal, "Нетто")
incompleteModel.setHeaderData(20, QtCore.Qt.Horizontal, "Проба")
incompleteModel.setHeaderData(21, QtCore.Qt.Horizontal, "Зачет")
incompleteModel.setFilter("unload_send is not null and tare_weight is null")
incompleteModel.select()

# # Делаем копию модели для применения в таблице "В пути"
# enrouteModel = tripsModel
# enrouteModel.setFilter("arrival_dt is null")
#
# # Делаем копию модели для применения в таблице "В очереди"
# inlineModel = tripsModel
# inlineModel.setFilter("gross_weight is null")
#
# # Делаем копию модели для применения в таблице "Незавершенные рейсы"
# incompleteModel = tripsModel
# incompleteModel.setFilter("tare_weight is not null")

# Модель для таблицы "Выгрузчики"
unloadsModel = QSqlTableModel()
unloadsModel.setTable("unloadpoints")
unloadsModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
unloadsModel.setSort(0, QtCore.Qt.AscendingOrder)
unloadsModel.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
unloadsModel.setHeaderData(1, QtCore.Qt.Horizontal, "Выгрузка")
unloadsModel.select()

# Модель для таблицы "Водители"
driversModel = QSqlRelationalTableModel()
driversModel.setTable("drivers")
driversModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
driversModel.setSort(0, QtCore.Qt.AscendingOrder)
driversModel.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
driversModel.setHeaderData(1, QtCore.Qt.Horizontal, "Выгрузка")
driversModel.select()

# Модель для таблицы "Пункты погрузки"
loadsModel = QSqlTableModel()
loadsModel.setTable("loadpoints")
loadsModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
loadsModel.setSort(0, QtCore.Qt.AscendingOrder)
loadsModel.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
loadsModel.setHeaderData(1, QtCore.Qt.Horizontal, "Пункт погрузки")
loadsModel.setHeaderData(2, QtCore.Qt.Horizontal, "Нас. пункт")
loadsModel.select()

# Модель для таблицы "Автомобили"
trucksModel = QSqlRelationalTableModel()
trucksModel.setTable("transport")
trucksModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
trucksModel.setSort(0, QtCore.Qt.AscendingOrder)
trucksModel.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
trucksModel.setHeaderData(2, QtCore.Qt.Horizontal, "Рег. номер")
trucksModel.setHeaderData(3, QtCore.Qt.Horizontal, "Прицеп")
trucksModel.select()

# Модель для таблицы "Поставщики"
suppliersModel = QSqlRelationalTableModel()
suppliersModel.setTable("suppliers")
suppliersModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
suppliersModel.setSort(0, QtCore.Qt.AscendingOrder)
suppliersModel.setRelation(3, QSqlRelation("regions", "id", "name"))
suppliersModel.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
suppliersModel.setHeaderData(2, QtCore.Qt.Horizontal, "Наименование")
suppliersModel.setHeaderData(3, QtCore.Qt.Horizontal, "Район")
suppliersModel.select()