'''
Базовый модуль для всех классов, которые отвечают за выполнение отдельных этапов процесса создания отчета
'''
import logging

class Worker():
    '''Базовый класс для всех классов, которые отвечают за выполнение отдельных этапов процесса создания отчета'''

    def __init__(self, log_level = "DEBUG") -> None:
        self.log = self._get_logger(log_level)

    def _get_logger(self, log_level):
        '''Создание логера с уровнем сообщений log_level (по-умолчанию - DEBUG)'''
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        try:
            file_handler = logging.FileHandler('logs/report.log')
        except Exception as e:
            print(e)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
