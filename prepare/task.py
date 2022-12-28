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
        self.task['report_type'] = self.input['command']
        self.task['entity_type'] = self.input['type']
        self.task['output'] = self.input['output']
        self.task['daily_path'] = self.settings['path']['daily_base']
        self.task['kbase_path'] = self.settings['path']['kbase']
        self.task['raw_path'] = self.settings['path']['raw_path']

        # self.task['report_time_type'] = self._set_report_time_type() # Решил, что это ненужное свойство
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
        self.task['is_footer'] = self._set_is_part('footer')
        self.task['is_raw'] = self._set_is_part('raw')                
        self.task['output_path'] = self._set_output_path()
        self.task['norma'] = self._set_norma()        
             
        self.log.debug('Установка известных параметров завершена')

    def _set_entity_name(self):
        '''Возвращает название сущности из входных параметров'''
        if self.input.get('entityname', False):
            return self.input['entityname']
        else:
            return False
        

    def _set_start_date(self):
        if self._check_start_date_param():
            return "Начальная дата корректна"
        return 'Функция не реализована'

    def _set_end_date(self):
        return 'Функция не реализована'

    def _set_is_part(self, part):
        '''Определяет наличие/отсутствие раздела в отчета на основе входных параметров'''
        part_map = {
            'short':{
                'title': True,
                'period': True,
                'aggregated': True,
                'aggregated_size': 'short',
                'detailed': False,
                'links': False,
                'links_size': False,
                'source': False,
                'footer': True,
                'raw': True
            },
            'summary':{
                'title': True,
                'period': True,
                'aggregated': True,
                'aggregated_size': 'full',
                'detailed': False,
                'links': False,
                'links_size': False,
                'source': False,
                'footer': True,
                'raw': True
            },
            'detailed':{
                'title': True,
                'period': True,
                'aggregated': True,
                'aggregated_size': 'full',
                'detailed': True,
                'links': True,
                'links_size': 'short',
                'source': True,
                'footer': True,
                'raw': True
            },
            'full':{
                'title': True,
                'period': True,
                'aggregated': True,
                'aggregated_size': 'full',
                'detailed': True,
                'links': True,
                'links_size': 'full',
                'source': True,
                'footer': True,
                'raw': True
            },
            'raw':{
                'title': False,
                'period': False,
                'aggregated': False,
                'aggregated_size': False,
                'detailed': False,
                'links': False,
                'links_size': False,
                'source': False,
                'footer': False,
                'raw': True
            }
        }
        if self.input['command'] == 'raw':
            structure = 'raw'
        else:
            structure = self.input['structure']
        try:
            is_part = part_map.get(structure, "Неизвестный тип структуры").get(part,"Неизвестный тип раздела")
        except Exception as e:
            self.log.error(f'Ошибка обработки параметров: структура - {structure}, часть - {part}. Ошибка: {e}')
        return is_part

    def _set_output_path(self):
        '''Возвращает путь сохранения отчета'''
        if self.input['reportpath']:
            return self.input['reportpath']
        elif self.input['command'] == 'raw':
            return self.settings['path']['raw_path']
        elif self.input['output'] == 'md':
            return self.settings['path']['output_md_path']
        elif self.input['output'] == 'json':
            return self.settings['path']['output_json_path']
        else:
            return False

    def _set_norma(self):
        '''Возвращает нормативное количество помидорок из файла настроек. Если не указано, возвращает 14'''
        norma = self.settings.get('analyst', 14)
        if isinstance(norma, dict):
            return norma.get('norma', 14)
        else:
            return norma

    def _check_start_date_param(self):
        '''Функция проверяет корректность сочетания входных параметров для начальной даты
        Возможные ошибки
        type: period
        - в input отсутствует startdate в явном виде 
        - startdate не является датой или не может быть преобразован в дату
        - в input есть любой из параметров: currentperiod, monthname, year

        type: week
        - нет startdate и нет currentperiod +
        - есть startdate и есть currentperiod +
        - есть monthname
        - есть startdate и есть year
        - есть currentperiod == 'last' и есть year

        '''
        if self.input['type'] == 'period':
            if self.input.get('currentperiod', False) or self.input.get('monthname', False) or self.input.get('year', False):
                self.log.error('В отчете типа period не могут быть указаны параметры currentperiod, monthname, year')
                raise WrongDatesParameter('В отчете типа period не могут быть указаны параметры currentperiod, monthname, year')
            elif not self.input.get('startdate'):
                self.log.error('В отчете типа period должна быть указана начальная дата (параметр --startdate, -s)')
                raise WrongDatesParameter('В отчете типа period должна быть указана начальная дата (параметр --startdate, -s)')
            elif not isinstance(self.input.get('startdate'), datetime.date):
                try:
                    datetime.date.fromisoformat(self.input.get('startdate'))
                except ValueError:
                    self.log.error(f"Неверный формат начальной даты {self.input.get('startdate')}")
                    raise WrongDatesParameter(f"Неверный формат начальной даты {self.input.get('startdate')}")
            return True

        if self.input['type'] == 'week':
            if (not self.input.get('startdate', False) and not self.input.get('currentperiod', False)) or (self.input.get('startdate', False) and self.input.get('currentperiod', False)):
                self.log.error('В отчете типа week должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp)')
                raise WrongDatesParameter('В отчете типа week должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp)')                



class WrongDatesParameter(Exception):
    pass