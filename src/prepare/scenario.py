'''Модуль содержит классы для создания сценария формирования отчета'''

from common.control import Worker
from report.etl import ETLManager
from report.metadata import MetadataPartMaker
from report.period import PeriodPartMaker
from report.title import TitlePartMaker
from export.exporter import JSONExporter, MarkdownExporter, ScreenVisualizer
from report.detailed import DetailedPartMaker
from report.aggregated import PeriodAggregatedPartMaker, PeriodAggregatedPartMakerFull, EntityAggregatedPartMaker, EntityAggregatedPartMakerFull
from report.links import PeriodLinksPartMaker, EntityLinksPartMaker
from report.source import SourcePartMaker

from collections import deque


class ScenarioManager(Worker):

    aggregated_dict = {
        'period': {
            'short': PeriodAggregatedPartMaker,
            'full': PeriodAggregatedPartMakerFull
        },
        'entity': {
            'short': EntityAggregatedPartMaker,
            'full': EntityAggregatedPartMakerFull
        }
    }

    links_dict = {
        'period': PeriodLinksPartMaker,
        'entity': EntityLinksPartMaker
    }

    output_dict = {
        'screen': ScreenVisualizer,
        'md': MarkdownExporter,
        'json': JSONExporter
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
            self.log.warning(
                f"В сценарии отсутствуют задачи")
            return False

    def create_scenario(self, task):
        self.log.debug(f"Формирование сценария")
        self._task = task

        entity_type = self._task['report_type']
        output = self._task['output']

        self._scenario.append(ETLManager)
        if self._task.get('report_type') == 'raw':
            self._scenario.append(JSONExporter)
        else:
            self._scenario.append(MetadataPartMaker)
            if self._task['is_period']:
                self._scenario.append(PeriodPartMaker)
            if self._task['is_title']:
                self._scenario.append(TitlePartMaker)
            if self._task['is_aggregated']:
                self._scenario.append(
                    ScenarioManager.aggregated_dict[entity_type][self._task['aggregated_size']])
            if self._task['is_detailed']:
                self._scenario.append(DetailedPartMaker)
            if self._task['is_links']:
                self._scenario.append(ScenarioManager.links_dict[entity_type])
            if self._task['is_source']:
                self._scenario.append(SourcePartMaker)
            self._scenario.append(ScenarioManager.output_dict[output])

        self.log.debug(f"Сценарий сформирован")
        return self._scenario
