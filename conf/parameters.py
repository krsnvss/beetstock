from configparser import ConfigParser

configuration = ConfigParser()
configuration.read('./conf/configuration.ini')
# Различные задержки и таймеры
# Интервал обновления таблиц (ms)
table_update = int(configuration['intervals']['table_update'])
# Время отображения информационных сообщений для терминалов
msg_time = int(configuration['intervals']['msg_time'])

# Параметры БД
db_name = configuration['database']['db_name']
db_user = configuration['database']['db_user']
db_password = configuration['database']['db_password']
db_host = configuration['database']['db_host']

# Каталог для фотографий
photo_dir = configuration['storage']['photo_dir']
