'''
На визуализаторах можно потренировать наследование
'''

# визуализотор MarkDown
'''
Получает словарь с результатами
Получает путь до папки с результатами
Получает настройки полноты

Формирует текст заголовка
Формирует части в соответствии с настройками полноты
Объединяет части 
Сохраняет части в файл по пути
'''

# визуализотор JSON
'''
Получает словарь с результатами
Получает путь до папки с результатами
Получает настройки полноты

Отбирает необходимые части из словаря результатов
Сохраняет в JSON виде в нужный файл
'''

# визуализотор JSON
'''
Получает словарь с результатами
Получает путь до папки с результатами
Получает настройки полноты

Отбирает необходимые части из словаря результатов
Формирует текст заголовка
Формирует части в соответствии с настройками полноты для вывода экран
Объединяет части 
Выводит на экран
'''

# Менеджер визуализации
'''
Получает 
    настройки визуализации
    локальные пути
    словарь с результатами
Запускает визуализотор MarkDown
Запускает визуализотор JSON
Запускает визуализотор на экран
'''

import json
from anytree.importer import DictImporter
from anytree import Node, RenderTree

class WeekVisualizerManager:

    def __init__(self):
        pass

    def setVisual(self, vis_type, vis_out, data, detail,  type, report_path):
        '''Настройка процесса визуализации
        vis_type - полнота визуализации (сокращенный, детальный, полный)
        vis_out - метод вывода отчета (экран, файл json, файл md)
        data - данные для визуализации
        report_path - путь для файла отчета
        '''
        self.vis_type = vis_type
        self.vis_out = vis_out
        self.data = data
        self.type = type
        self.detail = detail
        self.report_path = report_path

        self.title = []
        self.short_part = []
        self.detail_part = []

    def makeTitle(self):
        '''Создание заголовка отчета'''
        self.title.append(f"# {self.getReportType()} за период с {self.data['start_date']} по {self.data['last_date']}\n\n")

    def getReportType(self):
        match self.type:
            case 'week':
                return 'Еженедельный отчет'
            case 'period':
                return 'Отчет'
        return ''

    def makeShortPart(self):
        '''Создание краткой части отчета'''
        self.short_part.append(f"Количество дней в периоде: {self.data['days']}\n")
        self.short_part.append(f"Количество проанализированных дней: {self.data['days_analyst']}\n")
        self.short_part.append(f"Даты, для которых не найдена заметка: {self.data['lost_dates']}\n")
        self.short_part.append(f"Всего осмысленных помидорок: {self.data['total_pom']}\n")
        self.short_part.append(f"Процент учтенных осмысленных помидорок относительно максимально возможного за период: {self.data['effective_all_days']}\n")
        self.short_part.append(f"Процент учтенных осмысленных помидорок относительно проанализированных дней: {self.data['effective_know_days']}\n")

    def makeDetailPart(self):
        '''Создание детализированной части отчета'''
        self.detail_part.append(f"Учет помидорок для тем по проектам:\n")
        importer = DictImporter()
        root = importer.import_(self.detail)
        for pre, fill, node in RenderTree(root):
            self.detail_part.append("%s%s - %s\n" % (pre, node.id, node.pom_num))


    def jsonOutput(self, output):
        '''Вывод в json файл'''
        filename = f"{self.getReportType()} с {self.data['start_date']} по {self.data['last_date']}"
        with open(self.report_path + '\\' + filename + '.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=4, ensure_ascii=False)

    def screenOutput(self, output):
        '''Вывод на экран'''
        print(*output)
        input()

    def fileOutput(self, output):
        '''Вывод в md файл'''
        filename = f"{self.getReportType()} с {self.data['start_date']} по {self.data['last_date']}"
        with open(self.report_path + '\\' + filename + '.md', 'w', encoding="utf-8") as outfile:
            for line in output:
                outfile.write(line)             

    def startVisual(self):
        '''Запуск процесса визулизации'''
        vis_out_map ={
            'json': self.jsonOutput, 
            'screen': self.screenOutput, 
            'md': self.fileOutput
        }
        self.makeTitle()
        self.makeShortPart()
        self.makeDetailPart()

        match self.vis_type:
            case 'short':
                vis_out_map[self.vis_out](self.title + self.short_part)
            case 'detail':
                vis_out_map[self.vis_out](self.title + self.detail_part)
            case 'full':
                vis_out_map[self.vis_out](self.title + self.short_part + self.detail_part)    






