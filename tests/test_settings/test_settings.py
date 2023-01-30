
from prepare.settings import *

import os
import json


def test_get_namespace_with_empty_file(settings):
    '''Проверка считывания пустого файла настроек'''
    settings.settings_file = 'empty_file.json'
    settings.dirname = 'tests\\testdata\\Settings'

    test = settings.get_settings_namespace()

    assert {} == test


def test_add_group_empty_file(empty_settings):
    '''Добавление новой группы в пустой файл'''
    input = {
        "group": "path",
    }

    target = {
        "path":
        {
        }
    }
    empty_settings.change_settings(input)

    with open(os.path.join('tests\\testdata\\Settings', 'empty_file.json'), 'r') as f:
        test = json.load(f)

    assert target == test


def test_add_group_param_empty_file(empty_settings):
    '''Добавление новой группы и нового параметра в пустой файл'''
    input = {
        "group": "path",
        "set_param": "daily_base = D:\\Base\\"
    }
    target = {
        "path":
        {
            "daily_base": "D:\\Base\\"
        }
    }
    empty_settings.change_settings(input)
    with open(os.path.join('tests\\testdata\\Settings', 'empty_file.json'), 'r') as f:
        test = json.load(f)
    assert target == test




def test_add_param_full_file(full_settings):
    '''Добавление нового параметра в существующий файл'''
    input = {
        "group": "path",
        "set_param": "daily_base = D:\\Base\\"
    }
    target = {
        "path":
        {
            "kbase": "tests\\testdata\\KBase",
            "set": "set",
            "daily_base": "D:\\Base\\"
        },
        "analyst":
        {
            "norma": 14
        }
    }
    full_settings.change_settings(input)
    with open(os.path.join('tests\\testdata\\Settings', 'full_file.json'), 'r') as f:
        test = json.load(f)
    assert target == test



def test_change_param_full_file(full_settings):
    '''Изменить параметр в существующем файле'''
    input = {
        "group": "path",
        "set_param": "kbase = D:\\Base\\"
    }
    target = {
        "path":
        {
            "kbase": "D:\\Base\\",
            "set": "set"
        },
        "analyst":
        {
            "norma": 14
        }
    }
    full_settings.change_settings(input)
    with open(os.path.join('tests\\testdata\\Settings', 'full_file.json'), 'r') as f:
        test = json.load(f)
    assert target == test


def test_add_err_param_full_file(full_settings):
    '''Тестирование попытки добавить некорректный параметр'''
    input = {
        "group": "path",
        "set_param": "wrong_param = D:\\Base\\"
    }
    target = {
        "path":
        {
            "kbase": "tests\\testdata\\KBase",
            "set": "set"
        },
        "analyst":
        {
            "norma": 14
        }
    }
    full_settings.change_settings(input)
    with open(os.path.join('tests\\testdata\\Settings', 'full_file.json'), 'r') as f:
        test = json.load(f)
    assert target == test



def test_add_new_group_new_param_full_file(full_settings):
    '''Тестирование попытки добавить новую группу (не path, не analyst) и новый параметр'''
    input = {
        "group": "group",
        "set_param": "new_param = 1"
    }
    target = {
        "path":
        {
            "kbase": "tests\\testdata\\KBase",
            "set": "set"
        },
        "analyst":
        {
            "norma": 14
        },
        "group":
        {
            "new_param": "1"
        }
    }
    full_settings.change_settings(input)
    with open(os.path.join('tests\\testdata\\Settings', 'full_file.json'), 'r') as f:
        test = json.load(f)
    assert target == test


def test_del_group_full_file(full_settings):
    '''Удалить группу в существующем файле'''
    input = {
        "del_param": "path"
    }
    target = {
        "analyst":
        {
            "norma": 14
        }
    }
    full_settings.change_settings(input)
    with open(os.path.join('tests\\testdata\\Settings', 'full_file.json'), 'r') as f:
        test = json.load(f)
    assert target == test


def test_del_param_full_file(full_settings):
    '''Удалить параметр в существующем файле'''
    input = {
        "group": "path",
        "del_param": "kbase"
    }

    target = {
        "path": {
            "set": "set"
        },
        "analyst": {
            "norma": 14
        }
    }
    full_settings.change_settings(input)
    with open(os.path.join('tests\\testdata\\Settings', 'full_file.json'), 'r') as f:
        test = json.load(f)
    assert target == test


def test_no_file(no_settings):
    '''Создание файла настроек, если не обнаружен'''
    input = {
        "group": "path",
    }

    target = {
        "path":
        {
        }
    }
    no_settings.change_settings(input)

    with open(os.path.join('tests\\testdata\\Settings', 'no_file.json'), 'r') as f:
        test = json.load(f)

    assert target == test