import datetime

import pymongo
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

dbClient = pymongo.MongoClient(' ')

myDb = dbClient['dqj_jinshidata']

myCol = myDb['news']

# 地址
url = "https://flash-api.jin10.com/get_flash_list"
header = {
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0",
}
queryParam = {
    'vip': 1,
    "channel": "-8200",
}


def doScheduled():
    curr_time = datetime.datetime.now()
    queryParam['max_time'] = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    json = requests.get(url, queryParam, headers=header, timeout=100).json()
    data = json['data']
    for index in range(0, len(data)):
        _id = data[0]['id']
        flag = myCol.find_one({"_id": _id})
        if flag is None:
            keyList = ['id', 'time', 'type', 'data', 'important', 'tags', 'channel', 'remark']
            doc = {'_id': data[index]['id']}
            for i in range(0, len(keyList)):
                doc[keyList[i]] = data[index][keyList[i]]
            print(doc)
            myCol.insert_one(doc)


# 定时爬取数据
def doJob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔1S
    scheduler.add_job(doScheduled, 'interval', max_instances=10, seconds=1)
    scheduler.start()


doJob()
