'''
Формирователь отчетов
Предназначен для анализа файлов в формате markdown на наличие записей об осмысленных помидорках
и подготовке отчетов на основе выполненного анализа
'''

import sys
from common.control import ReportMaker, CommandLineParameterMiss


def main():
    report_maker = ReportMaker(sys.argv)
    try:
        report_maker.start()
    except CommandLineParameterMiss as e:
        print("Отсутствуют параметры командной строки")

if __name__ == "__main__":
    main()
