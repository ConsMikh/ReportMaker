import pytest
import requests

import repmaker as app


import os


@pytest.fixture(scope="session")
def github():
    '''Соединение с github'''
    username = "ConsMikh"
    dir = 'tests\\test_release'
    path = os.path.join(dir, 'token.txt')
    with open(path, 'r') as f:
        token = f.readline()

    gh_session = requests.Session()
    gh_session.auth = (username, token)

    yield gh_session


@pytest.fixture(scope="session")
def version():
    '''Возвращает версию из модуля repmaker'''
    return app.__version__
