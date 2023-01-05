'''
Классы для создания части с описание периода отчета
'''
import datetime
import pandas as pd

from common.worker import PartMaker

class PeriodPartMaker(PartMaker):

    MONTH_NAME = {
        1: 'январь',
        2: 'февраль',
        3: 'март',
        4: 'апрель',        
        5: 'май',
        6: 'июнь',
        7: 'июль',
        8: 'август',
        9: 'сентябрь',
        10: 'октябрь',
        11: 'ноябрь',
        12: 'декабрь'  
        }



    def process(self):
        self.log.info(f"Формирование данных о периоде")
        self.report['period'] = {}
        start_date = self._get_start_date(self.task.get('start_date'))
        end_data = self._get_end_date(self.task.get('end_date'))
        self.report['period']['start_date'] = start_date.strftime('%Y-%m-%d')
        self.report['period']['start_date_task'] = self.task.get('start_date').strftime('%Y-%m-%d')
        self.report['period']['end_date'] = end_data.strftime('%Y-%m-%d')
        self.report['period']['days_num'] = (end_data - start_date).days + 1
        
        self.report['period']['start_year'] = start_date.year
        self.report['period']['start_month_num'] = start_date.month
        self.report['period']['start_month_name'] = PeriodPartMaker.MONTH_NAME[start_date.month]
        self.report['period']['start_week_num'] = start_date.isocalendar()[1]
        
        self.report['period']['end_year'] = end_data.year
        self.report['period']['end_month_num'] = end_data.month
        self.report['period']['end_month_name'] = PeriodPartMaker.MONTH_NAME[end_data.month]
        self.report['period']['end_week_num'] = end_data.isocalendar()[1]

        self.report['period']['str_period'] = self._get_str_period()

        self.log.info(f"Формирование данных о периоде завершено")

    def _get_start_date(self,start_date):
        if start_date == datetime.date(self.task['min_year'],1,1):
            data = self.report['dataframe']
            return datetime.date.fromisoformat(data['date'].loc[data['file_exist']==True].iloc[0])
        else:
            return start_date

    def _get_end_date(self,end_date):
        if end_date == datetime.date(self.task['max_year'],12,31):
            return datetime.date.today()
        else:
            return end_date

    def _get_str_period(self):
        STR_PERIOD_TEMPLATE = {
        'period': f"\nНачало периода: {self.report['period']['start_date']}\nКонец периода: {self.report['period']['end_date']}\nКоличество дней в периоде: {self.report['period']['days_num']}",
        'week': f"\nНачало недели: {self.report['period']['start_date']}\nКонец недели: {self.report['period']['end_date']}\nНомер недели: {self.report['period']['start_week_num']}",
        'month': f"\nНачало месяца: {self.report['period']['start_date']}\nКонец месяца: {self.report['period']['end_date']}\nКоличество дней в месяце: {self.report['period']['days_num']}",
        'theme': f"\nПериод: {self.report['period']['start_date']} - {self.report['period']['end_date']}\nКоличество дней в периоде: {self.report['period']['days_num']}",
        'epic': f"\nПериод: {self.report['period']['start_date']} - {self.report['period']['end_date']}\nКоличество дней в периоде: {self.report['period']['days_num']}\nТема, к которой относится эпик: {self.report.get('entity',{}).get('entity_theme')}",
        'project': f"\nПериод: {self.report['period']['start_date']} - {self.report['period']['end_date']}\nКоличество дней в периоде: {self.report['period']['days_num']}\nЭпик, к которому относится проект: {self.report['entity']['entity_epic']}\nТема, к которой относится эпик: {self.report.get('entity',{}).get('entity_theme')}\n",
        'task': f"\nПериод: {self.report['period']['start_date']} - {self.report['period']['end_date']}\nКоличество дней в периоде: {self.report['period']['days_num']}\nПроект, к которому относится задача: {self.report['entity']['entity_project']}\nЭпик, к которому относится проект: {self.report['entity']['entity_epic']}\nТема, к которой относится эпик: {self.report.get('entity',{}).get('entity_theme')}\n"
        }
        return STR_PERIOD_TEMPLATE[self.report['entity']['entity_type']]
