'''
Модуль содержит классы, управляющие выполнением всех этапов создания отчета
'''
import logging
import logging.config

from prepare.settings import SettingsProvider
from prepare.cl_parser import CLParser, ParsingCommandLineError

class ReportMaker():
    '''Основной класс, отвечающий за управление процессом создания отчета
    Создает все необходимые объекты и выполняет вызовы их методов
    '''
    def __init__(self, *args) -> None:
        self.cl_params = list(*args)[1:]
        self.log = self._get_logger()

    def start_CL_parser(self):
        self.log.debug(self.cl_params)
        if self.cl_params:
            self.log.info("Start command line parsing")
            cl_parser = CLParser(self.cl_params)
            try:
                namespace = cl_parser.get_input_namespace()
            except ParsingCommandLineError as e:
                self.log.error(f'Commandline parser error (argparse problem): {e}')
            else:
                
                self.log.info('Finish command line parsing')

        else:
            self.log.critical("There are not command line parameters")
            raise CommandLineParameterMiss()
    
    def start(self):
        '''Запуск процесса создания отчета'''
        self.log.info("***********Start*************")
        
        # Start commnan line parser
        self.start_CL_parser()

        
    def _get_logger(self):
        '''Создание логгера на основе файла настроек'''
        logging.basicConfig(filename='logs/report.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
        return logging.getLogger('ReportMaker')


class CommandLineParameterMiss(Exception):
    pass
