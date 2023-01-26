from report.etl import Extractor

extr = Extractor(log_level='CRITICAL')
path = 'D:\\3. Михайлов\\Develop\\PythonTraining\\ReportMaker\\tests\\testdata\\TestNotes'
file = 'err_empty_pom_part.md'
ext_data = extr.parseFile(path, file)
print(ext_data)
