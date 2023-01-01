'''Модуль содержит классы для создания сценария формирования отчета'''

from common.control import Worker
from collections import deque


class ScenarioManager(Worker):
    
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
        self._scenario.append('Step 1')
        self._scenario.append('Step 2')
        self._scenario.append('Step 3')
        self.log.debug(f"Сценарий сформирован")