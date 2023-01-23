'''
Модуль, в котором находятся классы для создания части отчета "связи"
'''
import os
import datetime

from common.worker import PartMaker

class LinksPartMaker(PartMaker):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self.data = self.report['dataframe']
        self.kbase_path = self.task['kbase_path']
        self.report['links'] = {}

    def process(self):
        self.log.info(f"Начало формирования части со связями")
        entity_type = self.report.get('entity',{}).get('entity_type')
        entity_name = self.report.get('entity',{}).get('entity_name')
        self.set_list_notes(entity_type = entity_type, entity_name = entity_name)
        self.set_file_lists()
        self.make_str_links()

        self.log.info(f"Часть со связями сформирована")

    def set_list_notes(self, **kwarg):
        pass

    def set_file_lists(self):
        pass

    def make_str_links(self):
        link_str = []
        link_str.append(f"Даты, в которые были записи о помидорках\n")
        for note in self.report['links']['list_notes']:
            str = f"[[{note[0]}]] - {note[1]}\n"
            link_str.append(str)
        
        if self.report['metadata']['report_type'] == 'period':
            if len(self.report.get('links',{}).get('list_create')) > 0:
                link_str.append(f"За период были созданы заметки:\n")
                for note in self.report['links']['list_create']:
                    str = f"[[{note}]]\n"
                    link_str.append(str)

            if len(self.report.get('links',{}).get('list_change')) > 0:
                link_str.append(f"\nЗа период были изменены заметки:\n")
                for note in self.report['links']['list_change']:
                    str = f"[[{note}]]\n"
                    link_str.append(str)      

        self.report['links']['str_links'] = link_str


class PeriodLinksPartMaker(LinksPartMaker):

    def set_list_notes(self, **kwarg):
        
        data = self.data[self.data['file_exist'] == True]
        self.report['links']['list_notes'] = [] 
        list_notes_data = data[['date', 'pom_num']].loc[data['pom_num']>0]
        for date in list_notes_data['date'].unique():
            date_pom = list_notes_data['pom_num'].loc[list_notes_data['date']==date].sum()
            self.report['links']['list_notes'].append([date, date_pom])

    def set_file_lists(self):
        self.report['links']['list_create'] = self.set_list_file(os.path.getctime)
        self.report['links']['list_change'] = self.set_list_file(os.path.getmtime)
    
    def set_list_file(self, func):

        kbase_files = [f for f in os.listdir(self.kbase_path) if os.path.isfile(os.path.join(self.kbase_path, f))]
        kbase_files_list = []
        epoch = datetime.datetime.utcfromtimestamp(0)

        start_date = datetime.datetime.fromisoformat(self.report['period']['start_date'])
        start_sec = (start_date - epoch).total_seconds()
        end_date = datetime.datetime.fromisoformat(self.report['period']['end_date'])
        end_sec = (end_date - epoch).total_seconds()
        for file in kbase_files:
            create_time = func(os.path.join(self.kbase_path, file))
            if create_time > start_sec and create_time < end_sec:
                kbase_files_list.append(file[:-3])
        
        return kbase_files_list


class EntityLinksPartMaker(LinksPartMaker):

    def set_list_notes(self, entity_type, entity_name):
        
        data = self.data[(self.data['file_exist'] == True) & (self.data[entity_type] == entity_name)]
        self.report['links']['list_notes'] = [] 
        list_notes_data = data[['date', 'pom_num']]
        for date in list_notes_data['date'].unique():
            date_pom = list_notes_data['pom_num'].loc[list_notes_data['date']==date].sum()
            self.report['links']['list_notes'].append([date, date_pom])

    def set_file_lists(self):
        pass
