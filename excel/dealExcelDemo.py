import pandas as pd
writer = pd.ExcelWriter('C:/Users/11469/Desktop/xxx/demoHasDeal.xls')
df = pd.read_excel('C:/Users/11469/Desktop/xxx/demo.xls', usecols=range(1, 16), skiprows=range(0, 8), skipfooter=2)
print(df.iloc[:, 0])