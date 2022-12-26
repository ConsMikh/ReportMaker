'''
Модуль содержит классы, управляющие выполнением всех этапов создания отчета
'''
import logging
import logging.config

from prepare.settings import SettingsProvider

class ReportMaker():
    '''Основной класс, отвечающий за управление процессом создания отчета
    Создает все необходимые объекты и выполняет вызовы их методов
    '''
    def __init__(self, *args) -> None:
        self.cl_params = args

    def start(self):
        '''Запуск процесса создания отчета'''
        log = self._get_logger()
        log.info("***********Start*************")
        print(self.cl_params)
        if self.cl_params:
            log.debug("Parsing command line")
        else:
            log.critical("There are not command line parameters")
            


    def _get_logger(self):
        '''Создание логгера на основе файла настроек'''
        logging.config.fileConfig('logs/logging.conf')
        return logging.getLogger("ReportMaker")
