from prepare.task import TaskManager
import datetime


def test_right_dates_list(test_input):
    '''Тест проверяет правильность формирования начальной и конечной даты периода при различных входных параметрах'''
    input = test_input[0]
    settings = test_input[1]
    target = test_input[2]

    tm = TaskManager(input, settings, log_level="CRITICAL")
    tm.task['start_date'] = tm._set_start_date()
    tm.task['end_date'] = tm._set_end_date()

    test_start_date = tm.task['start_date']
    test_end_date = tm.task['end_date']

    assert (test_start_date, test_end_date) == target


def test_right_dates_single():
    '''Тест проверяет правильность формирования начальной и конечной даты периода при различных входных параметрах'''
    input = {
        'command': 'raw',
        'type': None,
        'startdate': None,
        'enddate': None,
        'currentperiod': None,
        'monthname': None,
        'year': None
    }
    settings = {"analyst":
                {
                    "max_year": 2050,
                    "min_year": 2010
                }
                }
    target_start = "2010-01-01"
    target_end = "2050-12-31"

    target = (datetime.date.fromisoformat(target_start),
              datetime.date.fromisoformat(target_end))

    tm = TaskManager(input, settings, log_level="CRITICAL")
    tm.task['start_date'] = tm._set_start_date()
    tm.task['end_date'] = tm._set_end_date()

    test_start_date = tm.task['start_date']
    test_end_date = tm.task['end_date']

    assert (test_start_date, test_end_date) == target
