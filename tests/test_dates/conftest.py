import pytest
import pandas as pd
import datetime
from dateutil.parser import *
import calendar


def pytest_generate_tests(metafunc):
    """Функция генерирует тесты для test_right_dates
    Для работы надо, чтобы у теста был входной параметр test_input
    Тесты генерируются на основе excel 'tests/testdata/dateinputs.xlsx' лист 'right'
    Для полей помеченных 'calc' проводится вычисление дат на основе сегодняшней даты

    Returns:
        параметризатор для теста
    """
    # Пропускаем все функции, у которых нет аргумента test_inputss
    if 'test_input' not in metafunc.fixturenames:
        return

    test_cases = []
    test_excel = pd.ExcelFile('tests/testdata/dateinputs.xlsx')
    dataset = test_excel.parse('right')
    dataset = dataset.fillna(False)
    variants = dataset.apply(row_parse, axis=1)

    for i, v in enumerate(variants):
        test_cases.append(pytest.param(v, id=f"line - {i+2}"))

    return metafunc.parametrize("test_input", test_cases)


def row_parse(row):
    """Преобразует данные dataframe pandas, полученного из листа 'right' excel в набор данных для выполнения тестов

    Args:
        row : строка из dataframe

    Returns:
    input: имитация словаря параметров входной строки
    settings: имитация словаря настроек
    (start_data, end_data): целевые значения начальной и конечной даты
    """
    mark = row[0]
    input = {
        'command': row[1] if row[1] else None,
        'type': row[2] if row[2] else None,
        'startdate': row[3] if row[3] else None,
        'enddate': row[4] if row[4] else None,
        'currentperiod': row[5] if row[5] else None,
        'monthname': row[6] if row[6] else None,
        'year': row[7] if row[7] else None
    }
    # Параметры max_year и min_year должны совпадать с указанными в таблице excel
    settings = {"analyst":
                {
                    "max_year": 2050,
                    "min_year": 2010
                }
                }
    if mark == 'calc':
        start_date, end_date = get_period_dates(row[2], row[5])
    else:
        start_date = parser().parse(row[-3]).date()
        end_date = parser().parse(row[-2]).date()

    return input, settings, (start_date, end_date)


def get_period_dates(type, cur_per):
    '''Определяет начальную и конечную дату для случаев, когда период указан параметрами last, last_week, last_month, week, month'''
    today = datetime.date.today()
    match cur_per:
        case "last":
            if type == 'week':
                start_date, end_date = get_last_weeks_dates(today)
                return start_date, end_date
            if type == 'month':
                start_date, end_date = get_last_month_dates(today)
                return start_date, end_date
        case "week":
            start_date = today - \
                datetime.timedelta(calendar.weekday(
                    today.year, today.month, today.day))
            end_date = start_date + datetime.timedelta(6)
            return start_date, end_date
        case "month":
            start_date = datetime.date(today.year, today.month, 1)
            _, days = calendar.monthrange(
                start_date.year, start_date.month)
            end_date = start_date + datetime.timedelta(days-1)
            return start_date, end_date
        case "last_week":
            start_date, end_date = get_last_weeks_dates(today)
            return start_date, end_date
        case "last_month":
            start_date, end_date = get_last_month_dates(today)
            return start_date, end_date


def get_last_weeks_dates(today):
    '''Возвращает начало и конец прошлой недели
    today: datetime.date - сегодняшняя дата
    '''
    start_date = today - datetime.timedelta(calendar.weekday(
        today.year, today.month, today.day)) - datetime.timedelta(7)
    end_date = start_date + datetime.timedelta(6)
    return start_date, end_date


def get_last_month_dates(today):
    '''Возвращает начало и конец прошлого мясяца
    today: datetime.date - сегодняшняя дата
    '''
    date_in_month = datetime.date(
        today.year, today.month, 1) - datetime.timedelta(5)
    start_date = datetime.date(
        date_in_month.year, date_in_month.month, 1)
    _, days = calendar.monthrange(
        start_date.year, start_date.month)
    end_date = start_date + datetime.timedelta(days-1)
    return start_date, end_date
