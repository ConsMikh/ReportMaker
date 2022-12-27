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
    def __init__(self, *args, log_level = 'DEBUG') -> None:
        super().__init__(log_level)
        self.cl_params = list(*args)[1:]

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
        self.log.critical("*****Start*****")
        
        # Start commnan line parser
        self.start_CL_parser()


class CommandLineParameterMiss(Exception):
    pass

