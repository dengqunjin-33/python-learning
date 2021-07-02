import pandas as pd
import pymongo

# 效率慢多了
excel = pd.read_excel("C://Users//11469//Downloads//weather_district_id.xlsx",
                      sheelName="eather_district_id",
                      )
# 创建连接
myClient = pymongo.MongoClient('')

# 连接数据库
myDb = myClient['dengqunjin']

# 连接表
myCol = myDb['areacode']

keyList = ["_id", "district_id", "province", "city", "city_geocode", "district", "district_geocode", "lon", "lat"]
for row in range(0, len(excel.iloc[:, 1])):
    flag = myCol.find_one({keyList[0]: str(excel.iloc[row, 0])})
    print(flag)
    if flag is None:
        dbDict = {keyList[0]: str(excel.iloc[row, 0])}
        for col in range(0, len(keyList) - 1):
            dbDict[keyList[col + 1]] = str(excel.iloc[row, col])
        myCol.insert_one(dbDict)
        print(excel.iloc[row, 0])
print('结束')


