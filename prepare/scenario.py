'''Модуль содержит классы для создания сценария формирования отчета'''

from common.control import Worker
from report.etl import ETLManager
from report.metadata import MetadataPartMaker
from report.period import PeriodPartMaker
from report.title import TitlePartMaker
from export.exporter import JSONExporter, MarkdownExporter, ScreenVisualizer
from report.detailed import DetailedPartMaker
from report.aggregated import PeriodAggregatedPartMaker, PeriodAggregatedPartMakerFull, EntityAggregatedPartMaker, EntityAggregatedPartMakerFull

from collections import deque


class ScenarioManager(Worker):

    SCENARIO_ACTORS = {
        'raw': ETLManager,
        'metadata': MetadataPartMaker,
        'period': PeriodPartMaker,
        'title': TitlePartMaker,
        'detailed': DetailedPartMaker,
        'aggregated': EntityAggregatedPartMakerFull,
        'output': {
            'screen': ScreenVisualizer,
            'md': MarkdownExporter,
            'json': JSONExporter
        }
    }


    def __init__(self, log_level="ERROR") -> None:
        super().__init__(log_level)
        self._scenario = deque()

    @property
    def scenario(self):
        return self._scenario

    def pop_part_worker(self):
        try:
            return self._scenario.popleft()
        except IndexError as e:
            self.log.warning(f"В сценарии отсутствуют задачи")
            return False

    def create_scenario(self, task):
        self.log.debug(f"Формирование сценария")
        self._task = task
        self._create_etl_part()
        self._create_metadata_part()
        self._create_period_part()
        self._create_title_part()
        self._create_detailed_part()
        self._create_aggregated_part()


        self._add_output_worker()
        self.log.debug(f"Сценарий сформирован")
        return self._scenario

    def _create_etl_part(self):
        if self._task.get('is_raw', False):
            self._scenario.append(ScenarioManager.SCENARIO_ACTORS['raw'])

    def _create_metadata_part(self):
        self._scenario.append(ScenarioManager.SCENARIO_ACTORS['metadata'])

    def _create_period_part(self):
        self._scenario.append(ScenarioManager.SCENARIO_ACTORS['period'])

    def _create_title_part(self):
        self._scenario.append(ScenarioManager.SCENARIO_ACTORS['title'])

    def _create_detailed_part(self):
        self._scenario.append(ScenarioManager.SCENARIO_ACTORS['detailed'])

    def _create_aggregated_part(self):
        self._scenario.append(ScenarioManager.SCENARIO_ACTORS['aggregated'])

    def _add_output_worker(self):
        self._scenario.append(ScenarioManager.SCENARIO_ACTORS['output']['screen'])
        # self._scenario.append(ScenarioManager.SCENARIO_ACTORS['output']['json'])
        self._scenario.append(ScenarioManager.SCENARIO_ACTORS['output']['md'])
        
