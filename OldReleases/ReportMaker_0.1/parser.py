'''
Получает содержание файла

Выделение записей про помидорки
Транмформация записей о помидорке к нужному виду с условием глубины анализа

Добавление к дереву нового узла или перезапись существующего узла
Возврат дерева
'''
from anytree import AnyNode, RenderTree, LevelOrderGroupIter
from anytree.exporter import DictExporter

class Parser():

    def __init__(self, deep=3):
        self.deep = deep
        self.root = AnyNode(id='Всего')
        self.nodes = {}

    def parseFile(self, lines):
        pomidor = 0
        for line in lines:
            if ('#' in line) & (pomidor == 1):pomidor = 0
            if((pomidor == 1) & (line[0] != '\n')): 
                pom_record = self.parseLine(line)
                self.checkNode(pom_record)
            if '#Помидорки' in line:
                pomidor = 1
    
    def aggNodes(self):
        '''
        Идея:
        Получить списки для все уровней дерева, используя итератор дерева:
        https://anytree.readthedocs.io/en/latest/api/anytree.iterators.html

        Для каждого уровня, начиная с нижнего, посчитать сумму помидорок для детей каждого узла

        Получится, что все узлы будут содержать сумму помидорок для всех детей
        '''
        levels_list = [[node for node in children] for children in LevelOrderGroupIter(self.root)]
        # points = points if points else [] - идея для замены сложного кода на простой
        for level_list in list(reversed(levels_list[:-1])):
            for node in level_list:
                for childnode in node.children:
                    try:
                        node.pom_num += childnode.pom_num
                    except:
                        node.pom_num = childnode.pom_num

    def parseLine(self, line):
        line_parts = line.split(':')
        part_num = 1
        pom_rec = []
        timespend = line_parts[-1]
        if len(line_parts) - 1 < self.deep:
            for part in line_parts:
                if (part != timespend) & (part_num < self.deep):
                    pom_rec.append(part.strip())
                    part_num += 1
                else:
                    break
            while part_num <= self.deep:
                pom_rec.append("Без указания")
                part_num += 1
        else:
            for partn in range(0, self.deep):
                pom_rec.append(line_parts[partn].strip())
        if ('+' in timespend): 
            timespend = timespend.count('+')
        pom_rec.append(int(timespend))
        return pom_rec

    def checkNode(self, pom_record):
        path = ''
        parent = self.root
        for node in pom_record[:-1]:
            path += node
            try:
                if self.nodes[path] in parent.children:
                    parent = self.nodes[path]
            except:
                self.nodes[path] = AnyNode(id=node, parent = parent)
                parent = self.nodes[path]
        try:
            parent.pom_num += pom_record[-1]
        except:
            parent.pom_num = pom_record[-1]

    def getTreeDict(self):
        exporter = DictExporter()
        return exporter.export(self.root)

    def getTree(self):
        return self.root, self.nodes

    def renderTree(self):
        print(RenderTree(self.root))