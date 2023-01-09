'''
Классы, формирующие агрегированную часть отчета
'''

from common.worker import PartMaker

class AggregatedPartMaker(PartMaker):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self.report['aggregated'] = {}
        self.data = self.report['dataframe'].fillna('Без указания')


    def make_part(self):
        self.log.debug(f"Не реализовано")


    def process(self):
        self.log.info(f"Начало формирования агрегированной части")
        if self.data['pom_num'].loc[self.data['file_exist'] == True].count() > 0:
            self.make_part()
        else:
            self.report['aggregated']['str_aggregated'] = []
            self.log.debug(f"В dataframe отсутствуют данные о помидорках")
        self.log.info(f"Агрегированная часть сформирована")


class PeriodAggregatedPartMaker(AggregatedPartMaker):

    def make_part(self):
        
       self.report['aggregated']['total_pom'] =  self.set_total_pom()
       self.report['aggregated']['max_norma_pom'] =  self.report['period']['days_num']*self.report['metadata']['norma']
       self.report['aggregated']['norma_pom_part'] = round(self.report['aggregated']['total_pom']*100.0/self.report['aggregated']['max_norma_pom'],2)
       self.report['aggregated']['entity_struct'] = self.set_entity_struct()
       self.make_full_part()
       self.make_str_aggregated()

    def set_total_pom(self):

        return self.data['pom_num'].loc[self.data['file_exist'] == True].sum()


    def set_entity_struct(self):
        entity_struct = []
        data = self.data.loc[self.data['file_exist'] == True]
        theme_list = list(data['theme'].unique())
        for theme in theme_list:
            if theme != 'Без указания':
                theme_pom = data['pom_num'].loc[data['theme']==theme].sum()
                theme_proc = round(theme_pom*100.0/self.report['aggregated']['total_pom'],2)
                entity_struct.append(f"{theme}: {theme_pom} - {theme_proc}%:\n")

                # self.log.debug(f"{theme}: {theme_pom} - {theme_proc}%")

                epic_list = list(data['epic'].loc[data['theme']==theme].unique())
                for epic in epic_list:
                    epic_pom = data['pom_num'].loc[(data['theme']==theme) & (data['epic']==epic)].sum()
                    epic_proc = round(epic_pom*100.0/theme_pom,2)
                    entity_struct.append(f"\t{epic}: {epic_pom} - {epic_proc}%:\n")

                    # self.log.debug(f"\t{epic}: {epic_pom} - {epic_proc}%:\n")

        return entity_struct 

    def make_full_part(self):
        self.log.debug(f"Не реализовано")

    def make_str_aggregated(self):
        str_aggregated = []

        str_aggregated.append(f"Всего учтенных осмысленных помидорок: {self.report['aggregated']['total_pom']}\n")
        str_aggregated.append(f"Зафиксированы осмысленные помидорки по следующим темам: \n")
        str_aggregated += self.report['aggregated']['entity_struct']
        str_aggregated.append(f"Максимально возможное количество помидорок по нормативу: {self.report['aggregated']['max_norma_pom']}\n")
        str_aggregated.append(f"Процент учтенных осмысленных помидорок от возможного количества по нормативу: {self.report['aggregated']['norma_pom_part']}")
        self.report['aggregated']['str_aggregated'] = str_aggregated


class PeriodAggregatedPartMakerFull(PeriodAggregatedPartMaker):


    def set_entity_struct(self):
        entity_struct = []
        data = self.data.loc[self.data['file_exist'] == True]
        theme_list = list(data['theme'].unique())
        for theme in theme_list:
            if theme != 'Без указания':
                theme_pom = data['pom_num'].loc[data['theme']==theme].sum()
                theme_proc = round(theme_pom*100.0/self.report['aggregated']['total_pom'],2)
                entity_struct.append(f"{theme}: {theme_pom} - {theme_proc}%\n")

            # self.log.debug(f"{theme}: {theme_pom} - {theme_proc}%\n")

        return entity_struct
    

    def make_full_part(self):

        real_days = self.data['date'].loc[self.data['file_exist'] == True].nunique()
        self.log.debug(f"{self.data['date'].loc[self.data['file_exist'] == True].unique()}")
        real_norma = real_days * self.report['metadata']['norma']
        self.report['aggregated']['real_pom_part'] = round(self.report['aggregated']['total_pom']*100.0/real_norma,2)

    def make_str_aggregated(self):
        str_aggregated = []

        str_aggregated.append(f"Всего учтенных осмысленных помидорок: {self.report['aggregated']['total_pom']}\n")
        str_aggregated.append(f"Зафиксированы осмысленные помидорки по следующим темам: \n")
        str_aggregated += self.report['aggregated']['entity_struct']
        str_aggregated.append(f"Максимально возможное количество помидорок по нормативу: {self.report['aggregated']['max_norma_pom']}\n")
        str_aggregated.append(f"Процент учтенных осмысленных помидорок от возможного количества по нормативу: {self.report['aggregated']['norma_pom_part']}\n")
        str_aggregated.append(f"Процент учтенных осмысленных помидорок от возможного количества без учета отсутствующих записей: {self.report['aggregated']['real_pom_part'] }\n")
        self.report['aggregated']['str_aggregated'] = str_aggregated

class EntityAggregatedPartMaker(AggregatedPartMaker):


    def make_part(self):
        
        data = self.data.loc[self.data['file_exist'] == True]
        entity_type = self.report['entity']['entity_type']
        entity_name = self.report['entity']['entity_name']
        self.report['aggregated']['total_pom'] =  self.set_total_pom(entity_type = entity_type, entity_name = entity_name)
        self.report['aggregated']['entity_first_date'] =  data['date'].loc[data[entity_type] == entity_name].iloc[0]
        self.report['aggregated']['entity_last_date'] =  data['date'].loc[data[entity_type] == entity_name].iloc[-1]
        self.report['aggregated']['entity_struct'] = self.set_entity_struct(entity_type = entity_type, entity_name = entity_name)
        self.make_full_part(entity_type = entity_type, entity_name = entity_name)
        self.make_str_aggregated(entity_type = entity_type, entity_name = entity_name)


    def set_total_pom(self, entity_type = None, entity_name = None):

        return self.data['pom_num'].loc[(self.data['file_exist'] == True) & (self.data[entity_type] == entity_name)].sum()


    def make_full_part(self, entity_type = None, entity_name = None):
        pass

    def set_entity_struct(self, entity_type = None, entity_name = None):
        
        data = self.data.loc[(self.data['file_exist'] == True) & (self.data[entity_type] == entity_name)]
        entity_struct = []
        parent_entity_pom = data['pom_num'].sum()
        columns = ['theme', 'epic', 'project', 'task']
        ind = columns.index(entity_type) + 1
        if ind <= 2:
            entity_list = list(data[columns[ind]].unique())
            for entity in entity_list:
                if entity != 'Без указания':
                    entity_pom =  data['pom_num'].loc[data[columns[ind]]==entity].sum()
                    entity_proc = round(entity_pom*100.0/parent_entity_pom,2)
                    entity_struct.append(f"\t{entity}: {entity_pom} - {entity_proc}%:\n")
            return entity_struct
        else:
            return [] 

    def make_str_aggregated(self, entity_type = None, entity_name = None):
        
        entity_spell = {
            'theme': 'темы',
            'epic': 'эпика',
            'project': 'проекта',
            'task': 'задачи'
        }

        str_aggregated = []

        str_aggregated.append(f"Всего учтенных осмысленных помидорок: {self.report['aggregated']['total_pom']}\n")
        str_aggregated.append(f"Дата первого упоминания {entity_spell[entity_type]}: {self.report['aggregated']['entity_first_date']}\n")
        str_aggregated.append(f"Дата последнего упоминания {entity_spell[entity_type]}: {self.report['aggregated']['entity_last_date']}\n")
        if entity_type != 'task':
            str_aggregated.append(f"Структура {entity_spell[entity_type]}:\n")
            str_aggregated += self.report['aggregated']['entity_struct']
        self.report['aggregated']['str_aggregated'] = str_aggregated


class EntityAggregatedPartMakerFull(EntityAggregatedPartMaker):


    def make_part(self):
        
        data = self.data.loc[self.data['file_exist'] == True]
        entity_type = self.report['entity']['entity_type']
        entity_name = self.report['entity']['entity_name']
        self.report['aggregated']['total_pom'] =  self.set_total_pom(entity_type = entity_type, entity_name = entity_name)
        self.report['aggregated']['entity_first_date'] =  data['date'].loc[data[entity_type] == entity_name].iloc[0]
        self.report['aggregated']['entity_last_date'] =  data['date'].loc[data[entity_type] == entity_name].iloc[-1]
        self.report['aggregated']['entity_struct'] = self.set_entity_struct(entity_type = entity_type, entity_name = entity_name)
        self.make_full_part(entity_type = entity_type, entity_name = entity_name)
        self.make_str_aggregated(entity_type = entity_type, entity_name = entity_name)


    def set_total_pom(self, entity_type = None, entity_name = None):

        return self.data['pom_num'].loc[(self.data['file_exist'] == True) & (self.data[entity_type] == entity_name)].sum()


    def make_full_part(self, entity_type = None, entity_name = None):

        data = self.data.loc[self.data['file_exist'] == True]
        self.report['aggregated']['entity_num_dates'] =  data['date'].loc[data[entity_type] == entity_name].nunique()
        self.report['aggregated']['entity_part_dates'] = round(self.report['aggregated']['entity_num_dates']*100.0/self.report['period']['days_num'],2)

    def make_str_aggregated(self, entity_type = None, entity_name = None):
        
        entity_spell = {
            'theme': 'темы',
            'epic': 'эпика',
            'project': 'проекта',
            'task': 'задачи'
        }

        entity_spell_2 = {
            'theme': 'упоминалась тема',
            'epic': 'упоминался эпик',
            'project': 'упоминался проект',
            'task': 'упоминалась задача'
        }

        str_aggregated = []

        str_aggregated.append(f"Всего учтенных осмысленных помидорок: {self.report['aggregated']['total_pom']}\n")
        str_aggregated.append(f"Дата первого упоминания {entity_spell[entity_type]}: {self.report['aggregated']['entity_first_date']}\n")
        str_aggregated.append(f"Дата последнего упоминания {entity_spell[entity_type]}: {self.report['aggregated']['entity_last_date']}\n")
        if len(self.report['aggregated']['entity_struct'])>0:
            str_aggregated.append(f"Структура {entity_spell[entity_type]}:\n")
            str_aggregated += self.report['aggregated']['entity_struct']
        str_aggregated.append(f"Всего дней, в которые {entity_spell_2[entity_type]}: {self.report['aggregated']['entity_num_dates']}\n")
        str_aggregated.append(f"Процент дней от общего количества, в которых были помидорки {entity_spell[entity_type]}: {self.report['aggregated']['entity_part_dates']}%\n")
        self.report['aggregated']['str_aggregated'] = str_aggregated








