'''
Классы для создания заголовка отчета
'''

from common.worker import PartMaker

class TitlePartMaker(PartMaker):

    def process(self):
        self.log.info(f"Начало создания заголовка")
        STR_TITLE_TEMPLATE = {
        'period': f"# Отчет за период с {self.report.get('period',{}).get('start_date')} по {self.report['period']['end_date']}\n",
        'week': f"# Недельный отчет с {self.report['period']['start_date']} по {self.report['period']['end_date']} ({self.report['period']['start_year']}_{self.report['period']['start_week_num']})\n",
        'month': f"# Месячный отчет за {self.report['period']['start_month_name']} {self.report['period']['start_year']} года ({self.report['period']['start_year']}_{self.report['period']['start_month_num']})\n",
        'theme': f"# Отчет по теме {self.report.get('entity',{}).get('entity_name')}\n",
        'epic': f"# Отчет по эпику {self.report.get('entity',{}).get('entity_name')}\n",
        'project': f"# Отчет по проекту {self.report.get('entity',{}).get('entity_name')}\n",
        'task': f"# Отчет по задаче {self.report.get('entity',{}).get('entity_name')}\n",
        }
        self.log.info(f"Заголовок создан")
        value = STR_TITLE_TEMPLATE.get(self.report['entity']['entity_type'],"Неверный тип сущности")
        self.report['title'] = STR_TITLE_TEMPLATE.get(self.report['entity']['entity_type'],"Неверный тип сущности")

