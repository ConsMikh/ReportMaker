'''
Формирователь отчетов
Предназначен для анализа файлов в формате markdown на наличие записей об осмысленных помидорках
и подготовке отчетов на основе выполненного анализа
'''

import sys
from common.control import ReportMaker


def main():
    report_maker = ReportMaker(sys.argv, log_level='INFO')
    try:
        report_maker.start()
    except Exception:
        print("Отсутствуют параметры командной строки")

if __name__ == "__main__":
    main()
