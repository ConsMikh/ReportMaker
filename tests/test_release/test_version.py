'''
Тестируется номер версии repmaker и его совпадение с номером релиза на github
'''

import json
import requests
import pytest


def test_version_is(version):
    '''Проверка наличия номера версии в модуле repmaker'''
    assert version


@pytest.mark.skip("Rep is public now")
def test_version_github_with_auth(github, version):
    '''Проверка совпадения версии последнего релиза на github и в модуле repmaker'''

    response = json.loads(github.get(
        "https://api.github.com/repos/ConsMikh/ReportMaker/releases/latest").text)
    assert response['tag_name'] == version


def test_version_github(version):
    '''Проверка совпадения версии последнего релиза на github и в модуле repmaker'''

    response = json.loads(requests.get(
        "https://api.github.com/repos/ConsMikh/ReportMaker/releases/latest").text)
    assert response['tag_name'] == version
