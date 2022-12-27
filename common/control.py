'''
Модуль содержит классы, управляющие и обеспечивающие выполнение всех этапов создания отчета
'''

from common.worker import Worker
from prepare.settings import SettingsParser
from prepare.cl_parser import CLParser, ParsingCommandLineError


class ReportMaker(Worker):
    '''Основной класс, отвечающий за управление процессом создания отчета
    Создает все необходимые объекты и выполняет вызовы их методов
    '''
    def __init__(self, *args, log_level = 'ERROR') -> None:
        super().__init__(log_level)
        self.cl_params = list(*args)[1:]

    def start_CL_parsing(self):
        '''Создание парсера командной строки и получение словаря параметров командной строки'''
        self.log.info("Парсинг командной строки")
        cl_parser = CLParser(log_level='INFO')
        try:
            self.namespace = cl_parser.get_input_namespace(self.cl_params)
            self.log.debug(f"Получены параметры командной строки: {self.namespace}")
        except ParsingCommandLineError as e:
            self.log.error(f"Возвращена ошибка из парсера командной строки: {e}")

    def start_set_parsing(self):
        '''Парсинг файла настроек'''
        self.log.info("Парсинг файла настроек")
        set_parser = SettingsParser(log_level='INFO')
        try:
            self.settings = set_parser.get_settings_namespace()
        except Exception as e:
            self.log.warning(f'Получена ошибка при выполнении парсинга файла настроек: {e}')
        self.log.debug(f"Получены параметры файла настроек: {self.settings}")




    def start(self):
        '''Запуск процесса создания отчета'''
        self.log.info("***********Start************")
        self.start_CL_parsing()
        self.start_set_parsing()
        




