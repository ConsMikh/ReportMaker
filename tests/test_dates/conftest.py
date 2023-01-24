import pytest
import pandas as pd


@pytest.fixture(scope='package')
def test_excel():
    '''Загрузка тестового excel с данными'''
    return pd.ExcelFile('tests/testdata/dateinputs.xlsx')
