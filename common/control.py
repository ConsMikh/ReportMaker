'''
Модуль содержит классы, управляющие и обеспечивающие выполнение всех этапов создания отчета
'''

from common.worker import Worker
from prepare.settings import SettingsParser
from prepare.cl_parser import CLParser, ParsingCommandLineError
from prepare.task import TaskManager, WrongInputParameter, WrongTaskParameter
from prepare.scenario import ScenarioManager


class ReportMaker(Worker):
    '''Основной класс, отвечающий за управление процессом создания отчета
    Создает все необходимые объекты и выполняет вызовы их методов
    '''
    def __init__(self, *args, log_level = 'ERROR') -> None:
        super().__init__(log_level)
        self.cl_params = list(*args)[1:]
        self.prog_name = list(*args)[0]
        self.report = {}

    def command_line_parsing(self):
        '''Создание парсера командной строки и получение словаря параметров командной строки'''
        self.log.info("Парсинг командной строки")
        cl_parser = CLParser(log_level='INFO')
        try:
            self.namespace = cl_parser.get_input_namespace(self.cl_params)
            self.log.debug(f"****************INPUT*********************")
            self.log.debug(f"{self.namespace}")
            self.log.debug(f"*****************************************")   
        except ParsingCommandLineError as e:
            self.log.error(f"Возвращена ошибка из парсера командной строки: {e}")

    def settings_file_parsing(self):
        '''Парсинг файла настроек'''
        self.log.info("Парсинг файла настроек")
        set_parser = SettingsParser(log_level='INFO')
        try:
            self.settings = set_parser.get_settings_namespace()
            self.log.debug(f"****************SETTINGS*********************")
            self.log.debug(f"{self.settings}")
            self.log.debug(f"*****************************************")   
        except Exception as e:
            self.log.warning(f'Получена ошибка при выполнении парсинга файла настроек: {e}')

    def make_task(self):
        '''Создание задачи для создания отчета'''
        self.log.info("Создание задачи")
        task_manager = TaskManager(log_level='INFO')
        try:
            task_manager.set_task_param(task_input = {
                'settings': self.settings,
                'input': self.namespace
            }, prog_name = self.prog_name)
            if task_manager.check_task():
                self.task = task_manager.task
                self.log.debug(f"****************TASK*********************")
                self.log.debug(f"{self.task}")
                self.log.debug(f"*****************************************")
        except WrongInputParameter as e:
            self.log.critical('Завершение работы из-за некорректных входных данных')
            raise Exception(f'Завершение работы из-за некорректных входных данных: {e}')
        except WrongTaskParameter as e:
            self.log.critical('Завершение работы из-за некорректных параметров задачи')
            raise Exception(f'Завершение работы из-за некорректных параметров задачи: {e}')        
        self.log.info("Задача создана")

    def make_scenario(self):
        '''Создание сценария формирования отчета'''
        self.log.info("Создание сценария формирования отчета")
        scenario_manager = ScenarioManager(log_level='INFO')
        try:
            self.scenario = scenario_manager.create_scenario(self.task)
            self.log.debug(f"***************SCENARIO******************")
            self.log.debug(f"{list(scenario_manager.scenario)}")
            self.log.debug(f"*****************************************")   
        except Exception as e:
            self.log.warning(f'Получена ошибка при создании сценария формирования отчета: {e}')
        self.log.info("Сценарий сформирован")

    def start(self):
        '''Запуск процесса создания отчета'''
        self.log.info("***********Start************")
        self.command_line_parsing()
        self.settings_file_parsing()
        self.make_task()
        self.make_scenario()
        for ind, part in enumerate(self.scenario):
            self.log.info(f"****************STEP {ind+1}*********************")
            part_worker = part(self.task, self.report)
            try:
                part_worker.process()
            except Exception as e:
                self.log.error(f"При выполнении {part_worker.__class__.__name__} произошла ошибка: {e}")
        




