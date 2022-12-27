'''
Содержит классы для обработки файла настроек
'''
import json

from common.worker import Worker

class SettingsParser(Worker):
    
    def __init__(self, log_level='ERROR') -> None:
        super().__init__(log_level)

    def get_settings_namespace(self):
        '''Загрузка настроек из файла настроек
        '''
        self.log.info('Парсинг файла настроек начат')
        try:
            with open('settings.json') as f:
                self.settings = json.load(f)
        except FileNotFoundError as e:
            self.log.error('Файл настроек не обнаружен')
            raise FileNotFoundError()
        self.log.info('Парсинг файла настроек закончен')
        return self.settings