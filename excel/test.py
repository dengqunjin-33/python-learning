import xlrd
wb = xlrd.open_workbook('C://Users//11469//Desktop//溶洞结算书.xls')
ws = wb.sheets()
ws_name = wb.sheet_names()
# for i in range(0, len(wsname)):
#     print(wsname[i])
print(ws_name)