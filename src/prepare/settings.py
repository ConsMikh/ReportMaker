'''
Содержит классы для обработки файла настроек
'''
import json
import os

from common.worker import Worker

class SettingsParser(Worker):
    
    DEFAULT_SETTINGS = {
    "path": {
        "daily_base": "tests\\testdata\\DailyBase",
        "kbase": "tests\\testdata\\KBase",
        "output_md_path": "tests\\testdata\\Reports\\md",
        "output_json_path": "tests\\testdata\\Reports\\json",
    },
    "analyst": {
        "norma": 14,
        "max_year": 2100,
        "min_year": 2010
    }
}

    def __init__(self, log_level='ERROR') -> None:
        super().__init__(log_level)
        self.settings = self._set_default_settings(self)

    def _set_default_settings(self, dir = None):
        self.settings = SettingsParser.DEFAULT_SETTINGS

    def _set_setting(self, part, key, value):
        self.settings[part][key] = value

    def get_settings_namespace(self):
        '''Загрузка настроек из файла настроек
        '''
        self.log.info('Парсинг файла настроек начат')
        dirname, _ = os.path.split(os.path.abspath(__file__))
        path = os.path.join(dirname, 'settings.json')
        try:
            with open(path) as f:
                self.settings = json.load(f)
        except FileNotFoundError as e:
            self.log.warning('Файл настроек не обнаружен! Используются настройки по-умолчанию')
        except Exception as e:
            self.log.warning(f'Получена ошибка при выполнении парсинга файла настроек: {e} Настройки выставлены в значения по-умолчанию')
        else:
            for dir, path in self.settings['path'].items():
                self.log.debug(f'Проверка пути: {dir} - {path}')
                if os.path.isdir(path):
                    self.log.debug(f'{dir} - {path} - существует')
                    self._set_setting('path', dir, path)
                else:
                    self.log.debug(f'{dir} - {path} - не существует. Установлен в значение по умолчанию')
                    self._set_setting('path', dir, SettingsParser.DEFAULT_SETTINGS['path'][dir])


        self.log.info('Парсинг файла настроек закончен')
        return self.settings

