

# Менеджер задачи для недельного отчета
'''
Определение начальной даты анализа
Определение конечной даты анализа
Определение глубины анализа записи о помидорке (в текущей реализации - не глубже 3)
Определение вида представления
Определение локальных настроек с путями
Определение нормативного количества помидорок

Определение параметров представления
    полнота:
    - подробное - вся информация за каждый день
    - краткое - только обобщенные параметры
    - полное - краткое + полное
    
    способ вывода:
    - вывод на экран
    - вывод в json
    - вывод в markdown

Вызов определителя списка дат

Создание словаря для хранения результатов анализа

Вызов анализатора

Создание параметров представления

Вызов Менеджера визуализации
'''

import datetime
import configparser
import os
import sys


from analyzer import WeekAnalyzerManager
from visualizer import WeekVisualizerManager

class WeekManager():
    '''Менеджер для создания недельно отчета'''

    def __init__(self) -> None:
        self.log = [] # log list for writing error in parameters
        self.analyst = {}

    def setTask(self, startdate, lastdate, deep, type, vistype, visout, settingspath):
        '''Получение параметров для создания отчета, настройка задачи
        startdate - дата начала анализа
        lastdate - дата конца анализа
        deep - глубина анализа (1 - до темы, 2 - до эпика, 3 - до проекта, 4 - до задачи)
        vistype
        visout
        settingspath
        '''
        self.startdate = startdate
        self.lastdate = lastdate
        self.deep = deep
        self.type = type
        self.vistype = vistype
        self.visout = visout
        self.settingspath = settingspath
        self.config = configparser.ConfigParser()
    
    def checkDateFormate(self, date):
        '''Проверка формата даты'''
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except:
            self.log.append(f'У даты {date} неверный формат (YYYY-mm-dd)\n')

    def checkPeriod(self):
        '''Проверка того, что стартовая дата раньше конечной'''
        try:
            datetime.datetime.strptime(self.lastdate, '%Y-%m-%d').date() - datetime.datetime.strptime(self.startdate, '%Y-%m-%d').date()
        except:
            self.log.append(f'Дата {self.startdate} и {self.lastdate} не образует диапазон\n')
        else:
            if (datetime.datetime.strptime(self.lastdate, '%Y-%m-%d').date() - datetime.datetime.strptime(self.startdate, '%Y-%m-%d').date()).days < 0:
                self.log.append(f'Конечная дата раньше начальной\n')

    def checkSettings(self):
        '''Проверка файла настроек'''
        try:
            # path = 'ObsidianAnalys\ReportMaker_1.0\setting.ini'
            dirname, _ = os.path.split(os.path.abspath(__file__))
            with open(dirname + '\\'+'setting.ini') as f:
                self.config.read_file(f)
            if self.config.get('local_path','week_report') == '':
                self.log.append(f'Отсутсвует путь до папки с еженедельными отчетами\n')
            if self.config['local_path']['daily_notes'] == '':
                self.log.append(f'Отсутсвует путь до папки с еженедельными заметками\n')
            if self.config['local_path']['kbase_notes'] == '':
                self.log.append(f'Отсутсвует путь до папки с заметками\n')
            if self.config['analyst']['norma_pom'] == '':
                self.log.append(f'Отсутсвует нормативное значение помидорок\n')
        except:
            self.log.append(f'Файл с настройками недоступен\n')

    def isTaskValid(self):
        '''Проверка параметров отчета на валидность'''
        self.checkDateFormate(self.startdate)
        self.checkDateFormate(self.lastdate)
        self.checkPeriod()
        self.checkSettings()
        if len(self.log) == 0:
            return True
        else:
            return False

    def startTask(self):
        '''Запуск анализа'''
        analyzer = WeekAnalyzerManager()
        analyzer.setAnalyst(self.startdate, self.lastdate, self.deep, self.analyst, self.settingspath)
        analyzer.startAnalyst()
        analyzer.aggregate()

        visualizer = WeekVisualizerManager()
        visualizer.setVisual(self.vistype, self.visout, analyzer.getResult(), analyzer.getDetailedResult(), self.type, self.config.get('local_path','week_report'))
        visualizer.startVisual()

    def getLog(self):
        '''Доступ к логу выполнения задачи'''
        return self.log



# Менеджер задачи для проектного отчета
