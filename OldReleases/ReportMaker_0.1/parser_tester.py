from parser import Parser

analyzed_date = ['2022-11-21','2022-11-22','2022-11-23','2022-11-24','2022-11-25','2022-11-27']
daily_notes_path = r'D:\1\DailyNotes'
deep = 4

parser = Parser(4)

for date in analyzed_date:
    try:
        with open(daily_notes_path + '\\' + date +'.md', encoding="utf-8") as f:
            lines = f.readlines()
            parser.parseFile(lines)
    except: 
        print('Дата ' + date + ' отсутствует')


parser.aggNodes()

parser.renderTree()