'''
Классы для создания детализированной части отчета
'''
import pandas as pd

from anytree import AnyNode, RenderTree
from anytree.exporter import DictExporter, JsonExporter

from common.worker import PartMaker, Worker

class DetailedPartMaker(PartMaker):

    def __init__(self, task, report, log_level="ERROR") -> None:
        super().__init__(task, report, log_level)
        self.data = self.report.get('dataframe')
        self.data.fillna('Без указания', inplace = True)
        self.tree = DetailedTree()

    def process(self):
        self.log.info(f"Начато создание детализированной части отчета")
        self.report['detailed'] = {}
        
        deep = self._get_tree_deep()

        if self.report['metadata']['report_type'] == 'period':
            total_pom = self.data['pom_num'].loc[self.data['file_exist']==True].sum()
            self.tree.create_tree(total_pom = total_pom)
            self.data[deep].apply(self.tree.add_node, axis = 1)
        elif self.report['metadata']['report_type'] == 'entity':
            total_pom = self.data['pom_num'].loc[(self.data['file_exist']==True) & (self.data[self.report['entity']['entity_type']] == self.report['entity']['entity_name'])].sum()
            self.tree.create_tree(root_name = self.report['entity']['entity_name'], total_pom = total_pom)
            self.data[deep].loc[(self.data['file_exist']==True) & (self.data[self.report['entity']['entity_type']] == self.report['entity']['entity_name'])].apply(self.tree.add_node, axis = 1)
        # self.report['detailed']['detailed_tree'] = self.tree.get_tree_dict()
        self.report['detailed']['str_detailed'] = self.tree.render_tree()

        self.log.info(f"Завершено создание детализированной части отчета")


    def _get_tree_deep(self):
        tree_deep = {
            'period': ['theme', 'epic', 'project', 'task','pom_num'],
            'week': ['theme', 'epic', 'project', 'task','pom_num'],
            'month': ['theme', 'epic', 'project', 'task','pom_num'],
            'theme': ['epic', 'project', 'task','pom_num'],
            'epic': ['project', 'task','pom_num'],
            'project': ['task','pom_num']
        }
        
        return tree_deep.get(self.report['entity']['entity_type'])


class DetailedTree(Worker):

    def __init__(self, log_level="ERROR") -> None:
        super().__init__(log_level)
        self.tree_nodes = {}

    def create_tree(self, root_name = "Всего", total_pom = 0):

        self.tree_root = AnyNode(id = root_name, pom_num = total_pom, pom_proc = 100.0)
        pass

    def add_node(self, line):

        path = 'root'
        parent = self.tree_root
        total_pom = self.tree_root.pom_num
        for node in line[:-1]:
            path = path + '_' + node
            if self.tree_nodes.get(path) not in parent.children:
                self.tree_nodes[path] = AnyNode(id=node, parent = parent, pom_num = 0, pom_proc = 0.0)
            parent = self.tree_nodes[path]
            parent.pom_num += line[-1]
            parent.pom_proc = round(parent.pom_num*100.0/total_pom,2)
    
    def get_tree_dict(self):
        exporter = DictExporter()
        dict = exporter.export(self.tree_root)
        return dict

    def render_tree(self):
        
        render = []
        for pre, _ , node in RenderTree(self.tree_root):
            if node.id != 'Без указания':
                render.append(f"{pre}{node.id} - {node.pom_num} - {node.pom_proc}%\n")
        return render

    