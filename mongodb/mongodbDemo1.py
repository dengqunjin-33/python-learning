import pandas as pd
import pymongo


# 面向对象的思想
def openMongodb(dbName, tableName):
    # 创建连接
    dbClient = pymongo.MongoClient('mongodb://dengqunjin:dengqunjin@101.37.79.120:27017')
    # 连接数据库
    db = dbClient[dbName]
    # 连接表
    return db[tableName]


def getDbList(excelPath, sheelName, keyList):
    excel = pd.read_excel(excelPath,
                          sheelName=sheelName,
                          )
    # 要插入的document文档
    dbList = []
    # 临时字典 用于去重
    tempDict = {}
    for row in range(0, len(excel.iloc[:, 1])):
        # 如果在字典里面 说明已经插入过了
        if str(excel.iloc[row, 0]) in tempDict:
            continue
        else:
            tempDict = {str(excel.iloc[row, 0]): str(excel.iloc[row, 0])}
            dbDict = {keyList[0]: str(excel.iloc[row, 0])}
            for col in range(0, len(keyList) - 1):
                dbDict[keyList[col + 1]] = str(excel.iloc[row, col])
            dbList.append(dbDict)
    return dbList


# 获取表
myCol = openMongodb('admin', 'areaCode')
excelPath = "C://Users//11469//Downloads//weather_district_id.xlsx"
keyList = ["_id", "district_id", "province", "city", "city_geocode", "district", "district_geocode", "lon", "lat"]
sheelName = "eather_district_id"
dbList = getDbList(excelPath, sheelName, keyList)

myCol.insert_many(dbList)
