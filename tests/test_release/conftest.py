import pytest
import requests

import repmaker as app


@pytest.fixture(scope="session")
def github():
    '''Соединение с github'''
    username = "ConsMikh"
    token = "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"

    gh_session = requests.Session()
    gh_session.auth = (username, token)

    yield gh_session


@pytest.fixture(scope="session")
def version():
    '''Возвращает версию из модуля repmaker'''
    return app.__version__
