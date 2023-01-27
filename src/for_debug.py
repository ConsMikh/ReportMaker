from report.etl import PomidorRulesList
from common.complainer import *

cmp = Complainer(PomidorRulesList())

pom = "Обычный текст без разделителя\n"

result = cmp.compliance(pom)

print(result)
