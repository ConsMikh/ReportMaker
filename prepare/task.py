'''
В модуле находятся классы для создания и обработки задачи создания отчета 
'''
import datetime
import calendar

from common.worker import Worker


class WrongDatesParameter(Exception):
    pass


class TaskManager(Worker):
    '''Класс создает задачу и проверяет валидность параметров'''

    MONTH_LIST = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', None]
    MIN_YEAR = 1970
    MAX_YEAR = 9999
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, log_level="ERROR") -> None:
        super().__init__(log_level)
        self.task = {}

    def set_task_param(self, task_input, prog_name):
        '''Установка известных параметров'''
        self.settings = task_input['settings']
        self.input = task_input['input']
        self.log.debug("Установка известных параметров")
        self.task['report_date'] = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
        self.task['report_maker'] = prog_name
        self.task['report_type'] = self.input.get('command')
        self.task['entity_type'] = self.input.get('type')
        self.task['output'] = self.input.get('output')
        self.task['daily_path'] = self.settings.get('path',{}).get('daily_base')
        self.task['kbase_path'] = self.settings.get('path',{}).get('kbase')
        self.task['raw_path'] = self.settings.get('path',{}).get('raw_path')

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
        '''Функция определяет корректную начальную дату'''
        if self._check_start_date_param() and self._check_end_date_param():
            if self.input.get('startdate'):
                start = self._get_datetime_format(self.input.get('startdate'))
                if self.input.get('type') == 'week':
                    delta = datetime.timedelta(calendar.weekday(start.year, start.month, start.day))
                    if delta > 0 and self.input.get('enddate'):
                        self.log.warning(f"Дата {start.strftime(TaskManager.DATE_FORMAT)} не является началом недели. Выставлен ближайший понедельник")
                        start -= delta # Если дата среди недели, то возвращается первый день недели
                if self.input.get('type') == 'month':
                    if start.day > 1 and self.input.get('enddate'):
                        self.log.warning(f"Дата {start.strftime(TaskManager.DATE_FORMAT)} не является началом месяца. Выставлено 1 число")
                    start = datetime.date(start.year, start.month, 1) # Если дата среди месяца, то возвращается первый день месяца
                return start
            elif self.input.get('currentperiod'):
                if self.input.get('currentperiod') in ['last', 'last_week', 'month', 'last_month', 'week']:
                    today = datetime.date.today()
                    if (self.input.get('type') == 'week' and self.input.get('currentperiod') == 'last') or (self.input.get('command') in ['entity', 'raw'] and self.input.get('currentperiod') == 'last_week'):
                        return today - datetime.timedelta(calendar.weekday(today.year, today.month, today.day)) - datetime.timedelta(7)
                    elif (self.input.get('type') == 'month' and self.input.get('currentperiod') == 'last') or (self.input.get('command') in ['entity', 'raw'] and self.input.get('currentperiod') == 'last_month'):
                        date_in_month = datetime.date(today.year, today.month, 1) - datetime.timedelta(5) # Попадаем в нужный месяц
                        return datetime.date(date_in_month.year, date_in_month.month, 1)
                    elif self.input.get('command') in ['entity', 'raw'] and self.input.get('currentperiod') == 'week':
                        return today - datetime.timedelta(calendar.weekday(today.year, today.month, today.day))
                    elif self.input.get('command') in ['entity', 'raw'] and self.input.get('currentperiod') == 'month':
                        return datetime.date(today.year, today.month, 1)
                if self._is_int(self.input.get('currentperiod')):
                    if self.input.get('type') == 'week':
                        num_week = int(self.input.get('currentperiod')) - 1
                        tek_year = datetime.date.today().year
                        if self.input.get('year') == None:
                            year = datetime.date.today().year
                        first_year_day = datetime.date(year,1,1)
                        first_monday = first_year_day - datetime.timedelta(calendar.weekday(first_year_day.year, first_year_day.month, first_year_day.day))
                        return first_monday + datetime.timedelta(num_week*7)


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
        Общие
        - неверный формат даты
        - в currentperiod что-то кроме
            week 'last' или от 1 до 53
            month:'last' или от 1 до 12
            entity/raw: 'last week/week/last month/month' или от 1 до 12
        - в monthname не имя месяца
        - в year не число от 1970 до 9999
        
        type: period
        - в input отсутствует startdate в явном виде 
        - startdate не является датой или не может быть преобразован в дату
        - в input есть любой из параметров: currentperiod, monthname, year

        type: week
        - нет startdate и нет currentperiod 
        - есть startdate и есть currentperiod 
        - есть monthname 
        - есть startdate и есть year 
        - есть currentperiod == 'last' и есть year

        type: month
        - нет startdate и нет currentperiod или monthname
        - есть startdate и (есть currentperiod или monthname или year)
        - есть monthname и есть currentperiod
        - есть currentperiod == 'last' и есть year

        type: entity (theme/epic/project/task)
        - нет startdate и нет (currentperiod или monthname или year)
        - есть startdate и (currentperiod или monthname или year)
        - есть currentperiod и monthname
        - есть currentperiod == 'last week/week/last month/ month' и есть monthname или year

        type: raw
        - нет (currentperiod или monthname или year)
        - есть что-то кроме currentperiod или monthname или year
        - есть currentperiod и monthname
        - есть currentperiod == 'last week/week/last month/ month' и есть monthname или year
        '''
        if self.input.get('startdate') and not isinstance(self.input.get('startdate'), datetime.date):
            try:
                datetime.date.fromisoformat(self.input.get('startdate'))
            except ValueError:
                self.log.error(f"Неверный формат начальной даты {self.input.get('startdate')}")
                raise WrongDatesParameter(f"Неверный формат начальной даты {self.input.get('startdate')}")

        if self.input.get('currentperiod') and self.input.get('type') in ['week', 'month'] and not (self._is_int(self.input.get('currentperiod')) or self.input.get('currentperiod')=='last'):
            self.log.error(f"Неверный формат относительного периода {self.input.get('currentperiod')}")
            raise WrongDatesParameter(f"Неверный формат относительного периода {self.input.get('currentperiod')}")

        if self.input.get('type') == 'week' and self._is_int(self.input.get('currentperiod')):
            if self.input.get('currentperiod') < 1 or self.input.get('currentperiod') > 53: 
                    self.log.error(f"Неверный номер недели: {self.input.get('currentperiod')}")
                    raise WrongDatesParameter(f"Неверный номер недели: {self.input.get('currentperiod')}")

        if (self.input.get('type') == 'month' or self.input.get('command') in ['entity', 'raw']) and self._is_int(self.input.get('currentperiod')):
            if self.input.get('currentperiod') < 1 or self.input.get('currentperiod') > 12: 
                    self.log.error(f"Неверный номер месяца: {self.input.get('currentperiod')}")
                    raise WrongDatesParameter(f"Неверный номер месяца: {self.input.get('currentperiod')}")

        if self.input.get('currentperiod') and self.input.get('command') in ['entity', 'raw'] and not (self._is_int(self.input.get('currentperiod')) or self.input.get('currentperiod') in ['last_week','week','last_month','month',None]):
            self.log.error(f"Неверный формат относительного периода {self.input.get('currentperiod')}")
            raise WrongDatesParameter(f"Неверный формат относительного периода {self.input.get('currentperiod')}")

        if not self.input.get('monthname') in TaskManager.MONTH_LIST:
            self.log.error(f"Неверный формат наименования месяца {self.input.get('monthname')}. Должен быть {TaskManager.MONTH_LIST}")
            raise WrongDatesParameter(f"Неверный формат наименования месяца {self.input.get('monthname')}. Должен быть {TaskManager.MONTH_LIST}")

        if self.input.get('year') and not isinstance(self.input.get('year'),int):
            self.log.error(f"Неверный формат года {self.input.get('year')}")
            raise WrongDatesParameter(f"Неверный формат года {self.input.get('year')}")

        if isinstance(self.input.get('year'),int) and self.input.get('year') < TaskManager.MIN_YEAR and self.input.get('year') > TaskManager.MAX_YEAR:
            self.log.error(f"Неверный диапазон года {self.input.get('year')}. Год должен быть между {TaskManager.MIN_YEAR} и {TaskManager.MAX_YEAR}")
            raise WrongDatesParameter(f"Неверный диапазон года {self.input.get('year')}. Год должен быть между {TaskManager.MIN_YEAR} и {TaskManager.MAX_YEAR}")
        
        if self.input.get('type') == 'period':
            if self.input.get('currentperiod', False) or self.input.get('monthname', False) or self.input.get('year', False):
                self.log.error('В отчете типа period не могут быть указаны параметры currentperiod, monthname, year')
                raise WrongDatesParameter('В отчете типа period не могут быть указаны параметры currentperiod, monthname, year')
            elif not self.input.get('startdate'):
                self.log.error('В отчете типа period должна быть указана начальная дата (параметр --startdate, -s)')
                raise WrongDatesParameter('В отчете типа period должна быть указана начальная дата (параметр --startdate, -s)')

            return True

        if self.input.get('type') == 'week':
            if (not self.input.get('startdate', False) and not self.input.get('currentperiod', False)) or (self.input.get('startdate', False) and self.input.get('currentperiod', False)):
                self.log.error('В отчете типа week должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp)')
                raise WrongDatesParameter('В отчете типа week должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp)')
            elif self.input.get('monthname'):
                self.log.error('В отчете типа week не может быть задано название месяца (параметр --monthname, -mn)')
                raise WrongDatesParameter('В отчете типа week не может быть задано название месяца (параметр --monthname, -mn)')
            elif self.input.get('startdate') and self.input.get('year'):
                self.log.error('В отчете типа week не может быть одновременно задана начальная дата (параметр --startdate, -s) и год (параметр --year, -y)')
                raise WrongDatesParameter('В отчете типа week не может быть одновременно задана начальная дата (параметр --startdate, -s) и год (параметр --year, -y)')
            elif self.input.get('currentperiod') == 'last' and self.input.get('year'):
                self.log.error("В отчете типа week не может быть одновременно задан относительный период 'прошлая неделя' (параметр --currentperiod last) и год (параметр --year, -y)")
                raise WrongDatesParameter("В отчете типа week не может быть одновременно задан относительный период 'прошлая неделя' (параметр --currentperiod last) и год (параметр --year, -y)")
            return True

        if self.input.get('type') == 'month':
            if not self.input.get('startdate', False) and not (self.input.get('currentperiod', False) or self.input.get('monthname', False)):
                self.log.error('В отчете типа month должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn)')
                raise WrongDatesParameter('В отчете типа month должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn)')
            elif self.input.get('startdate', False) and (self.input.get('currentperiod', False) or self.input.get('monthname', False) or self.input.get('year', False)):
                self.log.error('В отчете типа month не может быть одновременно задана начальная дата (параметр --startdate, -s) и название месяца (параметр --monthname, -mn), относительный период (параметр --currentperiod, -cp) или год (параметр --year, -y)')
                raise WrongDatesParameter('В отчете типа month не может быть одновременно задана начальная дата (параметр --startdate, -s) и название месяца (параметр --monthname, -mn), относительный период (параметр --currentperiod, -cp) или год (параметр --year, -y)')
            elif self.input.get('currentperiod', False) and self.input.get('monthname', False):
                self.log.error('В отчете типа month не может быть одновременно заданы относительный период (параметр --currentperiod, -cp) и название месяца (параметр --monthname, -mn)')
                raise WrongDatesParameter('В отчете типа month не может быть одновременно заданы относительный период (параметр --currentperiod, -cp) и название месяца (параметр --monthname, -mn)')
            elif self.input.get('currentperiod') == 'last' and self.input.get('year'):
                self.log.error("В отчете типа month не может быть одновременно задан относительный период 'прошлый месяц' (параметр --currentperiod last) и год (параметр --year, -y)")
                raise WrongDatesParameter("В отчете типа week не может быть одновременно задан относительный период 'прошлый месяц' (параметр --currentperiod last) и год (параметр --year, -y)")
            return True

        if self.input.get('command') == 'entity':
            if not self.input.get('startdate', False) and not (self.input.get('currentperiod', False) or self.input.get('monthname', False) or self.input.get('year', False)):
                self.log.error(f"В отчете типа {self.input['type']} должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
                raise WrongDatesParameter(f"В отчете типа {self.input['type']} должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
            elif self.input.get('startdate', False) and (self.input.get('currentperiod', False) or self.input.get('monthname', False) or self.input.get('year', False)):
                self.log.error(f"В отчете типа {self.input['type']} должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
                raise WrongDatesParameter(f"В отчете типа {self.input['type']} должен быть задан один из параметров: начальная дата (параметр --startdate, -s) либо относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
            elif self.input.get('currentperiod', False) and self.input.get('monthname', False):
                self.log.error(f"В отчете типа {self.input['type']} должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn)")
                raise WrongDatesParameter(f"В отчете типа {self.input['type']} должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn)")
            elif self.input.get('currentperiod', False) in ['last_week', 'week', 'last_month', 'month'] and (self.input.get('monthname', False) or self.input.get('year', False)):
                self.log.error(f"В отчете типа {self.input['type']} должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn) или год (параметр --year, -y)")
                raise WrongDatesParameter(f"В отчете типа {self.input['type']} должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn) или год (параметр --year, -y)")
            return True

        if self.input.get('command') == 'raw':
            if not (self.input.get('currentperiod', False) or self.input.get('monthname', False) or self.input.get('year', False)):
                self.log.error(f"В отчете типа raw может быть задан один из параметров: относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
                raise WrongDatesParameter(f"В отчете типа raw может быть задан один из параметров: относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
            elif self.input.get('startdate', False):
                self.log.error(f"В отчете типа raw начальная дата не задается. Может быть задан один из параметров: относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
                raise WrongDatesParameter(f"В отчете типа raw начальная дата не задается. Может быть задан один из параметров: относительный период (параметр --currentperiod, -cp), либо название месяца (параметр --monthname, -mn), либо год (параметр --year, -y)")
            elif self.input.get('currentperiod', False) and self.input.get('monthname', False):
                self.log.error(f"В отчете типа raw должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn)")
                raise WrongDatesParameter(f"В отчете типа raw должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn)")
            elif self.input.get('currentperiod', False) in ['last_week', 'week', 'last_month', 'month'] and (self.input.get('monthname', False) or self.input.get('year', False)):
                self.log.error(f"В отчете типа raw должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn) или год (параметр --year, -y)")
                raise WrongDatesParameter(f"В отчете типа raw должен быть либо относительный период (параметр --currentperiod, -cp) либо название месяца (параметр --monthname, -mn) или год (параметр --year, -y)")
            return True

    def _check_end_date_param(self):
        '''Функция проверяет корректность сочетания входных параметров для конечной даты
        Возможные ошибки
        Общие
        - неверный формат даты
        - конечная дата раньше начальной
        '''
        if self.input.get('enddate') and not isinstance(self.input.get('enddate'), datetime.date):
            try:
                datetime.date.fromisoformat(self.input.get('enddate'))
            except ValueError:
                self.log.error(f"Неверный формат конечной даты {self.input.get('enddate')}")
                raise WrongDatesParameter(f"Неверный формат конечной даты {self.input.get('enddate')}")
        
        elif self.input.get('startdate') and self.input.get('enddate'):
            start = self.input.get('startdate')
            end = self.input.get('enddate')
            if not isinstance(start, datetime.date):
                start = datetime.date.fromisoformat(self.input.get('startdate'))
            if not isinstance(end, datetime.date):            
                end = datetime.date.fromisoformat(self.input.get('enddate'))
            if end < start:
                self.log.error(f"Конечная дата {end.strftime('%Y-%m-%d')} раньше начальной {start.strftime('%Y-%m-%d')}")
                raise WrongDatesParameter(f"Конечная дата {end.strftime('%Y-%m-%d')} раньше начальной {start.strftime('%Y-%m-%d')}")
        return True
        
    def _get_datetime_format(self, date):
        '''Проверяет формат даты и возвращает datetime.date, если возможно'''
        if not isinstance(date, datetime.date):
            try:
                date = datetime.date.fromisoformat(date)
                return date
            except ValueError as e:
                self.log.error(f"Неверный формат даты {date}")
                raise WrongDatesParameter(f"Неверный формат даты {date}")
        return date
        
    def _is_int(self, num):
        if not isinstance(num, int):
            try:
                int(num)
                return True
            except Exception as e:
                self.log.error("Не является целым числом: {num}")
                return False
        else:
            return True
