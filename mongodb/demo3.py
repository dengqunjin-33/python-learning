import pymongo

# 创建连接
myClient = pymongo.MongoClient('mongodb://data:2020data0414@172.16.10.61:27777')

# 连接数据库
myDb = myClient['fx_account']

# 连接表
myCol = myDb['accountmonitorimpl']

colCopy = myDb['accountmonitorimpl_copy1']

dbList = colCopy.find()

for data in dbList:
    _id = data['_id']
    vo = data['vo']
    findData = myCol.find_one({'_id': _id})
    if findData is None:
        print(_id)
        print("原始：" + str(vo))
        print('=============================================================')
        continue
    findVo = findData['vo']
    print(_id)
    print("原始：" + str(vo))
    print("统计：" + str(findVo))
    print('=============================================================')