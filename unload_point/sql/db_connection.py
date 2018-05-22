# Подключение к базе данных и модели таблиц
from PyQt5.QtSql import QSqlDatabase

# База данных
db_name = 'beetstock'
db_user = 'root'
db_password = 'Root123456'
db_host = 'localhost'

# Подключение к базе данных
db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName(db_host)
db.setDatabaseName(db_name)
db.setUserName(db_user)
db.setPassword(db_password)
db.open()