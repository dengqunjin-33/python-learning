import xlrd
from xlutils.copy import copy

readWb = xlrd.open_workbook("C:/Users/11469/Desktop/xxx/base.xls", formatting_info=True)
writeWb = copy(readWb)
dealWb = xlrd.open_workbook("C:/Users/11469/Desktop/xxx/demoHasDeal.xls")

