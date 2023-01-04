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
        start_date = self.get_start_date(self.task.get('start_date'))
        end_data = self.task.get('end_date')
        self.report['period']['start_date'] = start_date.strftime('%Y-%m-%d')
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

        self.log.info(f"Формирование данных о периоде завершено")

    def get_start_date(self,start_date):
        if start_date == datetime.date(self.task['min_year'],1,1):
            pass 

