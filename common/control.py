'''
Модуль содержит классы, управляющие и обеспечивающие выполнение всех этапов создания отчета
'''

from common.worker import Worker
from prepare.settings import SettingsProvider
from prepare.cl_parser import CLParser, ParsingCommandLineError


class ReportMaker(Worker):
    '''Основной класс, отвечающий за управление процессом создания отчета
    Создает все необходимые объекты и выполняет вызовы их методов
    '''
    def __init__(self, *args, log_level = 'ERROR') -> None:
        super().__init__(log_level)
        self.cl_params = list(*args)[1:]

    def start_CL_parser(self):
        '''Создание парсера командной строки и получение словаря параметров командной строки'''
        self.log.info("Начало парсинга командной строки")
        cl_parser = CLParser()
        try:
            self.namespace = cl_parser.get_input_namespace(self.cl_params)
            self.log.debug(f"Получены параметры командной строки: {self.namespace}")
        except ParsingCommandLineError as e:
            self.log.error(f"Возвращена ошибка из парсера командной строки: {e}")
    
    def start(self):
        '''Запуск процесса создания отчета'''
        self.log.critical("*****Start*****")
        self.start_CL_parser()
        




