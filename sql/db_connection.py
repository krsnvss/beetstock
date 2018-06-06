# Подключение к базе данных
from PyQt5.QtSql import QSqlDatabase
from conf.parameters import db_host, db_name, db_password, db_user

# Подключение к базе данных
db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName(db_host)
db.setDatabaseName(db_name)
db.setUserName(db_user)
db.setPassword(db_password)
db.open()
