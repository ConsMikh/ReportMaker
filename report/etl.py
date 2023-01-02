'''Классы, обеспечивающие извлечение данных о помидорках из файлов заметок'''

from common.worker import PartMaker


class ETLManager(PartMaker):

    def process(self):
        self.log.info("Начало ETL")
        self.log.info("Конец ETL")

