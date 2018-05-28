# Подключение к базе данных
from PyQt5.QtSql import QSqlDatabase

# База данных
db_name = 'beetstock'
db_user = 'operator'
db_password = 'Password1!'
db_host = 'localhost'

# Подключение к базе данных
db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName(db_host)
db.setDatabaseName(db_name)
db.setUserName(db_user)
db.setPassword(db_password)
db.open()