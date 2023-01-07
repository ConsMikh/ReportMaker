'''
Классы, формирующие агрегированную часть отчета
'''

from common.worker import PartMaker

class AggregatedPartMaker(PartMaker):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self.report['aggregated'] = {}
        self.data = self.report['dataframe']


    def make_short_part(self):
        self.log.debug(f"Не реализовано")


    def process(self):
        self.log.info(f"Начало формирования агрегированной части")
        if self.data['pom_num'].loc[self.data['file_exist'] == True].count() > 0:
            self.make_part()
        else:
            self.report['detailed']['str_aggregated'] = []
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
                entity_struct.append(f"{theme}: {theme_pom} - {theme_proc}%\n")

            # self.log.debug(f"{theme}: {theme_pom} - {theme_proc}%\n")

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

        real_days = self.data['date'].loc[self.data['file_exist'] == True].nunique()
        self.log.debug(f"{self.data['date'].loc[self.data['file_exist'] == True].unique()}")
        real_norma = real_days * self.report['metadata']['norma']
        self.report['aggregated']['real_pom_part'] = round(self.report['aggregated']['total_pom']*100.0/real_norma,2)

