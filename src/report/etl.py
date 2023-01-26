'''Классы, обеспечивающие извлечение данных о помидорках из файлов заметок'''
# Проверка формата записи помидорок
# Убрать двойные скобки с отдельных частей


import os
import pandas as pd

from common.worker import PartMaker, Worker

from datetime import date, timedelta


class ETLManager(PartMaker):
    '''
    Класс, обеспечивает процесс извлечения, преобразования и загрузки в датафрейм всех записей о помидорках
    в файлах в указанном диапазоне
    '''

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self._data = []
        self.extractor = Extractor()
        self.transformer = Transformer()
        self.loader = Loader()

    def daterange(self, start_date, end_date):
        '''Генератор для создания полного перечня дат в интересующем диапазоне'''
        for n in range(int((end_date - start_date).days)+1):
            yield start_date + timedelta(n)

    def process(self):
        self.log.info("Начало ETL")
        self.log.debug(
            f"Начальная дата: {self.task.get('start_date')}")
        self.log.debug(
            f"Конечная дата: {self.task.get('end_date')}")
        path = self.task.get('daily_path')
        for single_date in self.daterange(self.task.get('start_date'), self.task.get('end_date')):
            file = single_date.strftime('%Y-%m-%d')+'.md'
            extract_block = self.extractor.parseFile(path, file)
            self._data += self.transformer.transform(single_date.strftime(
                '%Y-%m-%d'), extract_block[1:], file_exist=extract_block[0])
        self.loader.dataframe_load(self._data)
        self.report['dataframe'] = self.loader.dataframe

        self.log.info("Конец ETL")


class Extractor(Worker):
    '''Класс для извлечения записей о помидорках из файлов
    '''

    def parseFile(self, path, file):
        '''Открывает файл. Находит записи о помидорках в файле.
        Если файла нет, возвращает ['0']

        Возможные ошибки:
        - нет тега о помидорках в файле
        - несколько тегов о помидороках в файле
        '''
        try:
            # self.log.debug(f"{file}- обработка")
            with open(os.path.join(path, file), encoding='utf8') as f:
                filedata = f.readlines()
                # self.log.debug(f"{os.path.join(path,file)} прочитан")
        except Exception as e:
            # self.log.debug(f"{os.path.join(path,file)} {e}")
            return [False, '0']

        pomidors = [True]
        pomidor_flag = False
        for line in filedata:
            if ('#' in line) & pomidor_flag:
                pomidor_flag = False
            if (pomidor_flag & (line[0] != '\n')):
                pomidors.append(line)

            if '#Помидорки' in line:
                pomidor_flag = True
        if len(pomidors) > 1:
            return pomidors
        else:
            return [True, '0']


class Transformer(Worker):
    '''Преобразует записи о помидорках из файла в список кортежей

    Возможные ошибки:
    - неверный формат записи
    - неправильные разделители
    - неправильное количество блоков
    - нет количества помидорок вообще
    - количество помидорок не числом и не +
    '''

    def transform(self, date, block, file_exist):
        transform_block = []
        for line in block:
            # self.log.debug(f"Запись для анализа {line}")
            line_parts = line.split(':')
            pom_rec = [date, file_exist]
            timespend = line_parts[-1]
            for ind, part in enumerate(line_parts):
                if (part != timespend):
                    pom_rec.append(part.strip())
                else:
                    while ind < 4:
                        pom_rec.append(pd.NA)
                        ind += 1
            if ('+' in timespend):
                timespend = timespend.count('+')
            pom_rec.append(int(timespend))
            transform_block.append(tuple(pom_rec))
        # self.log.debug(f"Трансформированный блок {transform_block}")
        return transform_block


class Loader(Worker):

    def __init__(self, log_level="ERROR") -> None:
        super().__init__(log_level)
        self._dataframe = pd.DataFrame()

    def dataframe_load(self, data):

        self._dataframe = pd.DataFrame.from_records(
            data, columns=['date', 'file_exist', 'theme', 'epic', 'project', 'task', 'pom_num'])
        # self.log.debug(f"Dataframe {self._dataframe.head}")

    @property
    def dataframe(self):
        return self._dataframe

    def dataframe_to_csv(self):
        self._dataframe.to_csv(
            'Docs\\Base\\Reports\\raw\\report.csv', index=False)
