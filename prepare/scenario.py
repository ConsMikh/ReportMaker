'''Модуль содержит классы для создания сценария формирования отчета'''

from common.control import Worker
from report.etl import ETLManager
from report.metadata import MetadataPartMaker
from report.period import PeriodPartMaker
from report.title import TitlePartMaker

from collections import deque


class ScenarioManager(Worker):

    SCENARIO_ACTORS = {
        'raw': ETLManager,
        'metadata': MetadataPartMaker,
        'period': PeriodPartMaker,
        'title': TitlePartMaker
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