import datetime

import pymongo
import requests

dbClient = pymongo.MongoClient('mongodb://data:2020data0414@172.16.10.61:27777')

myDb = dbClient['dqj_jinshidata']
myCol = myDb['news']

url = "https://flash-api.jin10.com/get_flash_list"
header = {
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0",
}
queryParam = {
    "channel": "-8200",
}

curr_time = datetime.datetime.now()
queryParam['max_time'] = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')

totalCount = 0
json = requests.get(url, queryParam, headers=header).json()
Data = json['data']
length = len(Data)
_list = []
# while ( length > 0 ):
for i in range(length):
    try:
        _id = Data[i]['id']
        time = Data[i]['time']
        _type = Data[i]['type']
        if _type == 0:
            content = Data[i]['data']['content']
            doc = {"_id": _id, "time": time, "content": content}
            _list.append(doc)
            print(_id, time, content)
    except Exception as e:
        print(e)
        continue
myCol.insert_many(_list)
totalCount += length

# 修正下一个查询时间
queryParam['max_time'] = Data[length - 1]['time']
print('next queryParam is', queryParam['max_time'])

# 再请求一次数据
# try:
#     s = requests.Session()
#     s.mount('http://', HTTPAdapter(max_retries=3))
#     s.mount('https://', HTTPAdapter(max_retries=3))
#     Data = requests.get(url, queryParam, timeout=5, headers=header).json()['data']
#     length = len(Data)
# except Exception as e:
#     print(e)
