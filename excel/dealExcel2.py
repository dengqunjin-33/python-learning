import pandas as pd

filexxxx11 = pd.ExcelFile('C:/Users/11469/Desktop/xxx/xxx11.xls')
writer = pd.ExcelWriter('C:/Users/11469/Desktop/xxx/demoHasDeal.xls')
dealReader = pd.ExcelFile('C:/Users/11469/Desktop/xxx/demoHasDeal.xls')
# 获取sheet集合
dealSheet = dealReader.sheet_names
# 控制demoHasDeal表格的sheet
start = 0
for filexxxx1SheetName in filexxxx11.sheet_names:
    df = pd.read_excel('C:/Users/11469/Desktop/xxx/xxx111.xls',
                                              sheet_name=filexxxx1SheetName, keep_default_na=False)
    if start < len(dealSheet):
        dfDeal = pd.read_excel('C:/Users/11469/Desktop/xxx/demoHasDeal.xls',
                               sheet_name=dealSheet[start])
    size = df.iloc[:, 0].size
    for index in range(0, size, 4):
        flag = True
        while flag:
            for i in range(0, dfDeal.iloc[:, 2].size):
                if df.iloc[index, 0] == dfDeal.iloc[i, 2]:
                    dfDeal.iloc[i, 10] = df.iloc[index, 1]
                    dfDeal.iloc[i, 11] = df.iloc[index+3, 2]
                    flag = False
                    break
            if df.iloc[index, 0] == dfDeal.iloc[dfDeal.iloc[:, 2].size-1, 2]:
                print(dfDeal.iloc[:, [0, 10, 11]])
                dfDeal.to_excel(writer, dealSheet[start], index=False)
                start = start + 1
                print(start)
                if start < len(dealSheet):
                    dfDeal = pd.read_excel('C:/Users/11469/Desktop/xxx/demoHasDeal.xls',
                                           sheet_name=dealSheet[start])

writer.save()
print('结束')
