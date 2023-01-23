'''
Формирователь отчетов
Предназначен для анализа файлов в формате markdown на наличие записей об осмысленных помидорках
и подготовке отчетов на основе выполненного анализа
'''

__version__ = "v2.2.2"

import sys
from common.control import ReportMaker


def main():
    report_maker = ReportMaker(sys.argv, log_level='INFO')
    try:
        report_maker.start()
    except Exception as e:
        print(f"Ошибка выполнения программы: {e}")


if __name__ == "__main__":
    main()
