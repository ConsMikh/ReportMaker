'''
Модуль, содержащий классы для парсинга параметров командной строки
'''

import argparse
import pathlib

from common.worker import Worker


class CLParser(Worker):
    '''Парсер параметров командной строки'''

    def __init__(self, *args, log_level='ERROR') -> None:
        super().__init__(log_level)
        self.parser = self._createParser()

    def get_input_namespace(self, parseline):
        '''Распрарсить параметры командной строки и вернуть их словарем'''
        self.log.info(
            'Парсинг командной строки начат')
        try:
            namespace = self.parser.parse_args(parseline)
            self.log.info(
                'Парсинг командной строки выполнен')
            return vars(namespace)
        except Exception as e:
            self.log.error(
                f'Ошибка парсинга командной строки: {e}')
            raise ParsingCommandLineError(e)

    def _createParser(self):
        '''Реализация парсера входных аргументов'''
        self.log.debug(
            'Создание парсера командной строки')
        parser = argparse.ArgumentParser(add_help=True, )
        subparsers = parser.add_subparsers(dest='command')

        period = subparsers.add_parser('period')
        period.add_argument(
            '--type', '-t', choices=['period', 'week', 'month'], default='period')
        period.add_argument('--startdate', '-s')
        period.add_argument('--enddate', '-l')
        period.add_argument('--currentperiod', '-cp')
        period.add_argument('--monthname', '-mn')
        period.add_argument('--year', '-y', type=int)
        period.add_argument(
            '--structure', '-st', choices=['short', 'summary', 'detailed', 'full'], default='full')
        period.add_argument(
            '--output', '-o', choices=['screen', 'md', 'json'], default='screen')
        period.add_argument('--reportpath', '-rp', type=pathlib.Path)

        entity = subparsers.add_parser('entity')
        entity.add_argument(
            '--type', '-t', choices=['theme', 'epic', 'project', 'task'], default='theme')
        entity.add_argument('--entityname', '-e', required=True)
        entity.add_argument('--startdate', '-s')
        entity.add_argument('--enddate', '-l')
        entity.add_argument('--currentperiod', '-cp')
        entity.add_argument('--monthname', '-mn')
        entity.add_argument('--year', '-y', type=int)
        entity.add_argument(
            '--structure', '-st', choices=['short', 'summary', 'detailed', 'full'], default='full')
        entity.add_argument(
            '--output', '-o', choices=['screen', 'md'], default='screen')
        entity.add_argument('--reportpath', '-rp', type=pathlib.Path)

        raw = subparsers.add_parser('raw')
        raw.add_argument('--currentperiod', '-cp')
        raw.add_argument('--monthname', '-mn')
        raw.add_argument('--year', '-y', type=int)
        raw.add_argument('--reportpath', '-rp', type=pathlib.Path)

        set = subparsers.add_parser('set')
        set.add_argument('--set_param', '-sp')
        set.add_argument('--del_param', '-dp')
        set.add_argument('--group', '-g')
        set.add_argument('--show', '-s', action='store_const', const=True)
        set.add_argument('--set_default', '-sd',
                         action='store_const', const=True)

        return parser


class ParsingCommandLineError(Exception):
    pass
