'''
Report maker 0.0.1
Скрипт формирования отчета по выполненным помидоркам
Функции:
+ 0.1 Парсинг параметров отчета из командной строки
    + использовать подпарсеры для командной строки
    + реализовать только подпарсер week
+ 0.2 Парсинг настроек из файла
+ 1. Парсинг записей из папки Daily за выделенный интервал времени
+ 2. Подсчет потраченных помидорок с глубиной до эпика
+ 2.1 Подсчет дополнительных статистик:
    + количество дней
    + общее количество осмысленных помидорок
    + процент осмысленных помидорок от максимально реализуемого количества помидорок
+ 3. Формирование структуры данных отчета
+ 4. Формирование представления отчета в виде json-файла
+ 5. Формирование представления отчета в виде Markdown файла.

Учебные цели
+ 1. Реализовать скриптом, а не ноутбуком
+ 2. Разобраться со структурой скрипта и входными параметрами
3. Делать все маленькими функциями
+ 4. Использовать классы
    + не использовать глобальные переменные
    - использовать наследование
'''

import sys
import argparse
from manager import WeekManager

def createParser ():
    '''Реализация парсера входных аргументов'''
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers (dest='command')
 
    week_parser = subparsers.add_parser ('period')
    week_parser.add_argument ('--startdate', '-s', required=True)
    week_parser.add_argument ('--lastdate', '-l', required=True)
    week_parser.add_argument ('--deep', '-d', type=int, choices= range(1,5), default=3)
    week_parser.add_argument ('--type', '-t', choices= ['period', 'week'], default='period')
    week_parser.add_argument ('--vistype', '-vt', choices= ['short', 'detail', 'full'], default= 'full')
    week_parser.add_argument ('--visout', '-vo', choices= ['json', 'screen', 'md'], default= 'screen')

    return parser

def main():
    '''Парсинг параметров командной строки'''
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    '''Создание менеджера задачи в зависимости от типа'''
    match namespace.command:
        case 'period': 
            week_manager = WeekManager()
            week_manager.setTask(namespace.startdate, namespace.lastdate, namespace.deep, namespace.type, namespace.vistype, namespace.visout, 'setting.ini')
            if week_manager.isTaskValid():
                print ('Параметры задачи корректны')
                week_manager.startTask()
            else:
                print (*week_manager.getLog()) 
        case 'theme': print('THEEEME')

if __name__ == "__main__":
    main()