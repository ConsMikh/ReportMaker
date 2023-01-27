from report.etl import PomidorRulesList
from common.complainer import *

l = PomidorRulesList()

pom = "3+++ 5 +++"

num = l._get_pom_num_num(pom)
print(num)
