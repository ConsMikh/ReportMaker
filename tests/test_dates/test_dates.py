import pytest
import pandas as pd
import datetime
import calendar


def pytest_generate_tests(metafunc):

    # Пропускаем все функции, у которых нет аргумента test_inputss
    if 'test_input' not in metafunc.fixturenames:
        return

    test_cases = []
    test_excel = pd.ExcelFile('tests/testdata/dateinputs.xlsx')
    dataset = test_excel.parse('right')
    variants = dataset.apply(row_parse, axis=1)

    for i, v in enumerate(variants):
        test_cases.append(pytest.param(v, id=str(i+1)))

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
        'command': row[1],
        'type': row[2],
        'startdate': row[3],
        'enddate': row[4],
        'currentperiod': row[5],
        'monthname': row[6],
        'year': row[7]
    }
    settings = {"analyst":
                {
                    "max_year": 2050,
                    "min_year": 2010
                }
                }
    if mark == 'calc':
        start_date, end_date = get_period_dates(row[2], row[5])
    else:
        start_date = datetime.date.fromisoformat(row[-3])
        end_date = datetime.date.fromisoformat(row[-2])
    return input, settings, (start_date, end_date)


def get_period_dates(type, cur_per):
    '''Определяет начальную и конечную дату для случаев, когда период указан параметрами last, last_week, last_month, week, month'''
    today = datetime.date.today()
    match cur_per:
        case "last":
            if type == 'week':
                start_date = today - datetime.timedelta(calendar.weekday(
                    today.year, today.month, today.day)) - datetime.timedelta(7)
                end_date = start_date + datetime.timedelta(6)
                return start_date, end_date
            if type == 'month':
                date_in_month = datetime.date(
                    today.year, today.month, 1) - datetime.timedelta(5)
                start_date = datetime.date(
                    date_in_month.year, date_in_month.month, 1)
                _, days = calendar.monthrange(
                    start_date.year, start_date.month)
                end_date = start_date + datetime.timedelta(days-1)
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
            start_date = today - datetime.timedelta(calendar.weekday(
                today.year, today.month, today.day)) - datetime.timedelta(7)
            end_date = start_date + datetime.timedelta(6)
            return start_date, end_date
        case "last_month":
            date_in_month = datetime.date(
                today.year, today.month, 1) - datetime.timedelta(5)
            start_date = datetime.date(
                date_in_month.year, date_in_month.month, 1)
            _, days = calendar.monthrange(
                start_date.year, start_date.month)
            end_date = start_date + datetime.timedelta(days-1)
            return start_date, end_date


def test_dates_right(test_input):
    '''Описание теста'''
    v = test_input[0]
    w = test_input[1]
    z = test_input[2]
    assert test_input == test_input
