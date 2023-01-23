'''
Тестируется номер версии repmaker и его совпадение с номером релиза на github
'''

import json


def test_version_is(version):
    '''Проверка наличия номера версии в модуле repmaker'''
    assert version


def test_version_github(github, version):
    '''Проверка совпадения версии последнего релиза на github и в модуле repmaker'''

    response = json.loads(github.get(
        "https://api.github.com/repos/ConsMikh/ReportMaker/releases/latest").text)
    assert response['tag_name'] == version
