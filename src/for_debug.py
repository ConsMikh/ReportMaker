from report.etl import *
from common.complainer import *

pom = ['0']

tr = Transformer()
ret = tr.transform('2023-01-27', pom, True)
