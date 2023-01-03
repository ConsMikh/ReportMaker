'''
Содержит классы для обработки файла настроек
'''
import json
import os

from common.worker import Worker

class SettingsParser(Worker):
    
    DEFAULT_SETTINGS = {
        'path': {
            'daily_base': 'Docs/Base/DailyBase', 
            'kbase': 'Docs/Base/KBase',
            'output_md_path': 'Docs/Base/Reports/md', 
            'output_json_path': 'Docs/Base/Reports/json', 
            'raw_path': 'Docs/Base/Reports/raw'}, 
        'analyst': {
            'norma': 14}
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
        try:
            with open('settings.json') as f:
                self.settings = json.load(f)
        except FileNotFoundError as e:
            self.log.warning('Файл настроек не обнаружен! Настройки должны храниться в файле settings.json в той же папке, из которой запускается скрипт')
            self.log.warning('Используются настройки по-умолчанию')
        except Exception as e:
            self.log.warning(f'Получена ошибка при выполнении парсинга файла настроек: {e} Настройки выставлены в значения по-умолчанию')

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

