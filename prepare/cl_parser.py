'''
Модуль, содержащий классы для парсинга параметров командной строки
'''

import argparse

from common.worker import Worker

class CLParser(Worker):
    '''Парсер параметров командной строки'''

    def __init__(self, *args, log_level='DEBUG') -> None:
        super().__init__(log_level)
        self.cl_params = args
        self.parser = self._createParser()

    def get_input_namespace(self):
        try:
            namespace = self.parser.parse_args(self.cl_params)
            self.log.debug(namespace.command)
            return namespace
        except Exception as e:
            raise ParsingCommandLineError(e)


    def _createParser(self):
        '''Реализация парсера входных аргументов'''
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')
    
        period = subparsers.add_parser('period')
        period.add_argument('--type', '-t', choices= ['period', 'week', 'month'], default='period')
        period.add_argument('--startdate', '-s')
        period.add_argument('--enddate', '-l')
        period.add_argument('--currentperiod', '-cp')
        period.add_argument('--monthname', '-mn')
        period.add_argument('--year', '-y', type=int, choices= range(1,9999))
        period.add_argument('--structure', '-st', choices= ['short', 'summary', 'detailed', 'full'], default='full')
        period.add_argument('--output', '-o', choices= ['screen', 'md', 'json'], default='screen')
        period.add_argument('--reportpath', '-rp')
        period.add_argument('--verbose', '-v', choices= ['critical', 'error', 'warning', 'info','debug','notset'], default='debug')

        entity = subparsers.add_parser('entity')
        entity.add_argument('--type', '-t', choices= ['theme', 'epic', 'project', 'task'], default='theme')
        entity.add_argument('--entityname', '-e')    
        entity.add_argument('--startdate', '-s')
        entity.add_argument('--enddate', '-l')
        entity.add_argument('--currentperiod', '-cp')
        entity.add_argument('--monthname', '-mn')
        entity.add_argument('--year', '-y', type=int, choices= range(1,9999))
        entity.add_argument('--structure', '-st', choices= ['short', 'summary', 'detailed', 'full'], default='full')
        entity.add_argument('--output', '-o', choices= ['screen', 'md', 'json'], default='screen')
        entity.add_argument('--reportpath', '-rp')
        entity.add_argument('--verbose', '-v', choices= ['critical', 'error', 'warning', 'info','debug','notset'], default='debug')

        raw = subparsers.add_parser('raw')
        raw.add_argument('--currentperiod', '-cp')
        raw.add_argument('--monthname', '-mn')
        raw.add_argument('--reportpath', '-rp')
        raw.add_argument('--verbose', '-v', choices= ['critical', 'error', 'warning', 'info','debug','notset'], default='debug')

        return parser


class ParsingCommandLineError(Exception):
    pass