# Функции для установки и проверки дат
from datetime import date, datetime, timedelta


# Границы смены для отчетов и отображения завершенных ресов
def day_shift(_date):
    shift_start = datetime(year=_date.year,
                         month=_date.month,
                         day=_date.day,
                         hour=8, 
                         minute=0,
                         second=0)
    shift_finish = shift_start + timedelta(hours=23, minutes=59, seconds=59)
    return [shift_start, shift_finish]


# Границы смены для графиков и настоящего времени
def shift_time(_datetime):
    if _datetime.hour < 8:
        _tomorrow = _datetime - timedelta(days=1)
        shift_start = datetime(year=_tomorrow.year,
                                month=_tomorrow.month,
                                day=_tomorrow.day,
                                hour=20,
                                minute=0,
                                second=0)
    elif 8 <= _datetime.hour < 20:
        shift_start = datetime(year=_datetime.year,
                               month=_datetime.month,
                               day=_datetime.day,
                               hour=8,
                               minute=0,
                               second=0)
    else:
        shift_start = datetime(year=_datetime.year,
                               month=_datetime.month,
                               day=_datetime.day,
                               hour=20,
                               minute=0,
                               second=0)
    shift_finish = shift_start + timedelta(hours=11, minutes=59, seconds=59)
    return [shift_start, shift_finish]
