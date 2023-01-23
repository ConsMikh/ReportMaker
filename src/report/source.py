'''
Классы, описывающие источники
'''

from common.worker import PartMaker


class SourcePartMaker(PartMaker):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)

    def process(self):
        self.log.info(f"Создание части с источниками")
        self.report['source'] = {}
        str_source = []

        data = self.report['dataframe']
        date_num = data['date'].loc[data['file_exist'] == True].nunique()
        if date_num == self.report['period']['days_num']:
            str_source.append(
                f"В базе обнаружены записи за все дни\n")
        elif data['date'].loc[data['file_exist'] == False].nunique() == self.report['period']['days_num']:
            str_source.append(
                f"В базе не обнаружены записи за указанный период\n")
        else:
            str_source.append(
                f"Количество дней, для которых в базе обнаружены файлы заметок: {date_num}\n")

        if self.report['metadata']['report_type'] == 'period':
            date_num_lost = data['date'].loc[data['file_exist']
                                             == False].nunique()
            if date_num_lost > 0:
                str_source.append(
                    f"Не обнаружены записи для следующих дат:\n")
                date_num_lost_list = data['date'].loc[data['file_exist'] == False].unique(
                )
                if len(date_num_lost_list) > 1:
                    date_num_lost_list += ['\n']
                str_source.extend(date_num_lost_list)

        str_source.append(
            f"\n\nДата создания отчета: {self.report['metadata']['report_date']}\n")
        str_source.append(
            f"Отчет создан: {self.report['metadata']['report_maker']}\n")

        self.report['source']['str_source'] = str_source
        self.log.info(f"Часть с источниками создана")
