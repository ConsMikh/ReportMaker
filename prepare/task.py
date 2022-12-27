'''
В модуле находятся классы для создания и обработки задачи создания отчета 
'''
import datetime

from common.worker import Worker

class TaskManager(Worker):
    '''Класс создает задачу и проверяет валидность параметров'''

    def __init__(self, log_level="ERROR") -> None:
        super().__init__(log_level)
        self.task = {}

    def set_task_param(self, settings, input, prog_name):
        '''Установка известных параметров'''
        self.settings = settings
        self.input = input
        self.log.debug("Установка известных параметров")
        self.task['report_date'] = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
        self.task['report_maker'] = prog_name
        self.task['report_type'] = input['command']
        self.task['entity_type'] = input['type']
        self.task['output'] = input['output']
        self.task['daily_path'] = self.settings['path']['daily_base']
        self.task['kbase_path'] = self.settings['path']['kbase']

        self.task['report_time_type'] = self._set_report_time_type()
        self.task['entity_name'] = self._set_entity_name()
        self.task['start_date'] = self._set_start_date()
        self.task['end_date'] = self._set_end_date()
        self.task['is_title'] = self._set_is_part('title')
        self.task['is_period'] = self._set_is_part('period')
        self.task['is_aggregated'] = self._set_is_part('aggregated')
        self.task['aggregated_size'] = self._set_is_part('aggregated_size')
        self.task['is_detailed'] = self._set_is_part('detailed')
        self.task['is_links'] = self._set_is_part('links')
        self.task['links_size'] = self._set_is_part('links_size')
        self.task['is_source'] = self._set_is_part('source')
        self.task['is_raw'] = self._set_is_part('raw')                
        self.task['output_path'] = self._set_output_path()
        self.task['norma'] = self._set_norma()        
             
        self.log.debug('Установка известных параметров завершена')

    def _set_report_time_type(self):
        return 'Функция не реализована'

    def _set_entity_name(self):
        return 'Функция не реализована'

    def _set_start_date(self):
        return 'Функция не реализована'

    def _set_end_date(self):
        return 'Функция не реализована'

    def _set_is_part(self, part):
        return 'Функция не реализована'

    def _set_output_path(self):
        return 'Функция не реализована'

    def _set_norma(self):
        return 'Функция не реализована'