'''
Базовый модуль для всех классов, которые отвечают за выполнение отдельных этапов процесса создания отчета
'''
import logging
import os

class Worker():
    '''Базовый класс для всех классов, которые отвечают за выполнение отдельных этапов процесса создания отчета'''

    def __init__(self, log_level = "ERROR") -> None:
        self.log = self._get_logger(log_level)

    def _get_logger(self, log_level):
        '''Создание логера с уровнем сообщений log_level'''
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        if not os.path.exists('logs'):
            os.makedirs("logs")


        try:
            file_handler = logging.FileHandler('logs/report.log',encoding='utf-8')
        except Exception as e:
            print(e)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


class PartMaker(Worker):
    '''Базовый класс для всех классов, непосредственно формирующих отчет'''

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(log_level)
        self.task = task
        self.report = report

    def process(self):
        self.log.warning("Часть не реализована")