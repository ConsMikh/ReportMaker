'''
Классы для вывода отчета
'''

import datetime
import pandas as pd
import os

from common.worker import PartMaker

class Exporter(PartMaker):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self.file_path = self.task['output_path']
        self.report_view = []

    def _get_file_name(self, title, type):
        return self._del_symbols(f"{title[:-1]}.{type}")

    def _add_title(self):
        self.report_view.append(self.report.get('title'))

    def _aggregate_report_view(self):
        self._add_title()
        self.report_view.append(self.report.get('period').get('str_period'))
        self.report_view.append(f"\n\nАгрегированная часть\n")
        self.report_view += self.report['aggregated']['str_aggregated']
        self.report_view.append("\n\nДетализированная часть\n")
        self.report_view += self.report['detailed']['str_detailed']
        self.report_view.append("\n\nСвязи\n")
        self.report_view += self.report['links']['str_links']
        self.report_view.append("\n\nИсточники\n")
        self.report_view += self.report['source']['str_source']

    def _del_symbols(self, str):
        sc = set(['[',']'])
        return ''.join([c for c in str if c not in sc])


class JSONExporter(Exporter):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self.json_dict ={}


    def process(self):
        self.log.info(f"Начат экспорт в файл JSON")
        data = self.report['dataframe'].applymap(lambda x: ''.join([c for c in x if c not in ['[',']']]) if not isinstance(x, bool) and not isinstance(x, int) else x)
        data.to_json(path_or_buf = os.path.join(self.task['raw_path'],f"raw_{datetime.date.today().strftime('%Y-%m-%d')}.json") , orient = 'records')
        # self.report['dataframe'].to_json(path_or_buf = os.path.join(self.task['raw_path'],f"raw_{datetime.date.today().strftime('%Y-%m-%d')}.json") , orient = 'records')
        self.log.info(f"Завершен экспорт в файл JSON")




class MarkdownExporter(Exporter):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        
    def _add_title(self):
        self.report_view.append(f"# {self.report.get('title')}")

    def process(self):
        self.log.info(f"Начат экспорт в файл Markdown")
        self._aggregate_report_view()

        file_name = self._get_file_name(self.report['title'],'md')
        with open(os.path.join(self.file_path,file_name),'w',encoding='utf-8') as f:
            f.writelines(self.report_view)
        self.log.info(f"Завершен экспорт в файл Markdown")

class ScreenVisualizer(Exporter):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self.screen_view = []

    def process(self):
        clean_report = []
        self.log.info(f"Начат вывод на экран")
        self._aggregate_report_view()
        for line in self.report_view:
            clean_report.append(self._del_symbols(line))
        print(*clean_report)
        self.log.info(f"Завершен вывод на экран")

