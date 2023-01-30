import pytest
import os

from prepare.settings import *


@pytest.fixture(scope='function')
def settings():
    set = SettingsParser(log_level='CRITICAL')
    return set


@pytest.fixture(scope='function')
def empty_settings(settings):
    settings.settings_file = 'empty_file.json'
    settings.dirname = 'tests\\testdata\\Settings'
    yield settings
    with open(os.path.join(settings.dirname, settings.settings_file), "w") as f:
        f.write("")


@pytest.fixture(scope='function')
def full_settings(settings):
    settings.settings_file = 'full_file.json'
    settings.dirname = 'tests\\testdata\\Settings'
    yield settings
    def_set = {
        "path": {
            "kbase": "tests\\testdata\\KBase",
            "set": "set"
        },
        "analyst": {
            "norma": 14
        }
    }
    with open(os.path.join(settings.dirname, settings.settings_file), "w") as f:
        json.dump(def_set, f, indent=4)


@pytest.fixture(scope='function')
def no_settings(settings):
    settings.settings_file = 'no_file.json'
    settings.dirname = 'tests\\testdata\\Settings'
    yield settings
    os.remove(os.path.join(settings.dirname, settings.settings_file))
