import pandas as pd
import datetime
import configparser
import os

from parser import Parser

class WeekAnalyzerManager():

    def __init__(self) -> None:
        self.log = []
        self.analyst_log = []
        self.analyst_result = {}

    def setAnalyst(self, startdate, lastdate, deep, analyst, settingspath):
        '''Настройка анализатора'''
        self.start_date = startdate
        self.last_date = lastdate
        self.deep = deep
        self.analyst = analyst
        self.settings_path = settingspath
        self.config = configparser.ConfigParser()
        dirname, _ = os.path.split(os.path.abspath(__file__))
        with open(dirname + '\\'+self.settings_path) as f:
            self.config.read_file(f)
        self.norma_pom = self.config['analyst']['norma_pom']
        self.analyst_result = {
            'start_date': self.start_date,
            'last_date': self.last_date,
            'deep': self.deep,
            'themes': [],
            'lost_dates': [],
            'total_pom': 0,
            'days_analyst': 0
            }
        self.parser = Parser(self.deep)
        self.parser_result = {}

    def getDatesList(self):
        '''Определитель списка дат 
        Получает начальую дату и конечную дату
        Возвращет все даты из указанного диапазона
        '''
        start_date = datetime.date.fromisoformat(self.start_date)
        end_date = datetime.date.fromisoformat(self.last_date)
        return pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
            ).strftime('%Y-%m-%d').tolist()

    def aggregate(self):
        '''Обобщает данные полученные из файлов'''
        self.analyst_result['days'] = (datetime.datetime.strptime(self.last_date, '%Y-%m-%d').date() - datetime.datetime.strptime(self.start_date, '%Y-%m-%d').date()).days + 1
        total_pom = self.parser_result['pom_num']
        self.analyst_result['total_pom'] = self.parser_result['pom_num']
        self.analyst_result['max_pom_all_days'] = self.analyst_result['days'] * int(self.norma_pom)
        self.analyst_result['max_pom_know_days'] =  self.analyst_result['days_analyst'] * int(self.norma_pom)
        self.analyst_result['effective_all_days'] = round(total_pom*100.0/float(self.analyst_result['max_pom_all_days']),2)
        self.analyst_result['effective_know_days'] = round(total_pom*100.0/float(self.analyst_result['max_pom_know_days']),2)
        

    def startAnalyst(self):
        '''Запуск анализа'''
        dates_list = self.getDatesList()
        daily_notes_path = self.config['local_path']['daily_notes']
        for analyzed_date in dates_list:
            try:
                with open(daily_notes_path + '\\' + analyzed_date +'.md', encoding="utf-8") as f:
                    lines = f.readlines()
                    self.analyst_result['days_analyst'] += 1
                    self.parser.parseFile(lines)
            except: 
                self.log.append('Дата ' + analyzed_date + ' отсутствует')
                self.analyst_result['lost_dates'].append(analyzed_date)
        self.parser.aggNodes()
        self.parser_result = self.parser.getTreeDict() 

        self.aggregate()

    def getLog(self):
        return self.log

    def getAnalystLog(self):
        return self.analyst_log
    
    def getResult(self):
        return self.analyst_result
    
    def getDetailedResult(self):
        return self.parser_result

