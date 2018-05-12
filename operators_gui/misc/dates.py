# Функции для установки и проверки дат
from datetime import date, datetime, timedelta


def day_shift(_date):
    shift_start = datetime(year=_date.year,
                         month=_date.month,
                         day=_date.day,
                         hour=8, 
                         minute=0,
                         second=0)
    shift_finish = shift_start + timedelta(hours=23, minutes=59, seconds=59)
    return [shift_start, shift_finish]

# print(day_shift(date.today()))
