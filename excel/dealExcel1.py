import pandas as pd

writer = pd.ExcelWriter('C:/Users/11469/Desktop/xxx/demoHasDeal.xls')
filexxxx2 = pd.ExcelFile('C:/Users/11469/Desktop/xxx/xxx2.xls')
# 遍历每一个sheet
for xxxx2SheetName in filexxxx2.sheet_names:
    # sheet_name--->通过名称获取sheet，(通过索引也是这个方法)
    # usecols--->选取列
    # skiprows---->忽略行
    # skipfooter-->不要后面k行
    df = pd.read_excel('C:/Users/11469/Desktop/xxx/xxx2.xls',
                       sheet_name=xxxx2SheetName,
                       usecols=[1, 3, 6, 10, 11],
                       skiprows=range(0, 6),
                       skipfooter=1)
    dfDeal = pd.read_excel('C:/Users/11469/Desktop/xxx/demo.xls', usecols=range(1, 16), skiprows=range(0, 8), skipfooter=2)
    # inplace=True（删除空的列和行，如果不为true的话删除失败）
    df.dropna(inplace=True)
    dfDealSize = dfDeal.iloc[:, 0].size
    if df.iloc[:, 1].size < dfDealSize:
        dfDealSize = df.iloc[:, 1].size
        dfDeal.drop(range(df.iloc[:, 1].size, dfDeal.iloc[:, 0].size), inplace=True)
    # 批量赋值，行号一定要对应，不然赋值会失败
    dfDeal.iloc[:, 0] = pd.Series(df.iloc[:dfDealSize, 0])
    dfDeal.iloc[:, 2] = df.iloc[:dfDealSize, 1]
    dfDeal.iloc[:, 3] = df.iloc[:dfDealSize, 4]
    dfDeal.iloc[:, 8] = df.iloc[:dfDealSize, 2]
    dfDeal.iloc[:, 12] = df.iloc[:dfDealSize, 3]
    # 写入excel中的sheet（还没保存）
    dfDeal.to_excel(writer, xxxx2SheetName, index=False)

    if df.iloc[:, 1].size > dfDealSize:
        dfDeal = pd.read_excel('C:/Users/11469/Desktop/xxx/demo.xls', usecols=range(1, 16), skiprows=range(0, 8),
                               skipfooter=2)
        flag = 0
        for index in range(dfDealSize, df.iloc[:, 1].size):
            flag += 1
            dfDeal.iloc[(index-14), 0] = df.iloc[index, 0]
            dfDeal.iloc[(index-14), 2] = df.iloc[index, 1]
            dfDeal.iloc[(index-14), 3] = df.iloc[index, 4]
            dfDeal.iloc[(index-14), 8] = df.iloc[index, 2]
            dfDeal.iloc[(index-14), 12] = df.iloc[index, 3]
        row = dfDeal.iloc[:, 0].size
        dfDeal.drop(range(flag, row), inplace=True)
        print(dfDeal.iloc[:, [0, 10, 11]])
        dfDeal.to_excel(writer, xxxx2SheetName+'（2）', index=False)
# 保存
writer.save()
print('结束')
