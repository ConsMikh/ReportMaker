'''
Классы для создания метаданных отчета
'''
import pandas as pd

from common.worker import PartMaker

class MetadataPartMaker(PartMaker):

    def process(self):
        self.log.info(f"Формирование метадаты")
        self.report['metadata'] = {}
        self._copy_task()
        self.report['entity'] = {}
        if self.task.get('report_type') == 'period':
            self._set_entity_report_for_period()
        elif self.task.get('report_type') == 'entity':
            self._set_entity_report_for_entity()
        self.log.info(f"Формирование метадаты завершено")

    def _copy_task(self):
        self.report['metadata']['report_date'] = self.task.get('report_date')
        self.report['metadata']['report_maker'] = self.task.get('report_maker')
        self.report['metadata']['report_type'] = self.task.get('report_type')
        self.report['metadata']['is_title'] = self.task.get('is_title')
        self.report['metadata']['is_period'] = self.task.get('is_period')
        self.report['metadata']['is_aggregated'] = self.task.get('is_aggregated')
        self.report['metadata']['aggregated_size'] = self.task.get('aggregated_size')
        self.report['metadata']['is_detailed'] = self.task.get('is_detailed')
        self.report['metadata']['is_links'] = self.task.get('is_links')
        self.report['metadata']['links_size'] = self.task.get('links_size')
        self.report['metadata']['is_source'] = self.task.get('is_source')
        self.report['metadata']['is_footer'] = self.task.get('is_footer')
        self.report['metadata']['is_raw'] = self.task.get('is_raw')            
        self.report['metadata']['norma'] = self.task.get('norma')

    def _set_entity_report_for_period(self):
        self.report['entity']['entity_type'] = self.task.get('entity_type')
        self.report['entity']['entity_theme'] = None
        self.report['entity']['entity_epic'] = None
        self.report['entity']['entity_project'] = None


    def _set_entity_report_for_entity(self):
        self.report['entity']['entity_type'] = self.task.get('entity_type')
        self.report['entity']['entity_name'] = self.task.get('entity_name')

        entity_type = self.task.get('entity_type')
        entity_name = self.task.get('entity_name')
        data = self.report.get('dataframe')
        
        all_entities = data.loc[data[entity_type] == entity_name]
        self.report['entity']['entity_theme'] = all_entities['theme'].iloc[0]
        self.report['entity']['entity_epic'] = all_entities['epic'].iloc[0]
        self.report['entity']['entity_project'] = all_entities['project'].iloc[0]



