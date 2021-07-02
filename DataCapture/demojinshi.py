import datetime

import pymongo
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

dbClient = pymongo.MongoClient('mongodb://data:2020data0414@172.16.10.61:27777')

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
    Data = json['data']
    try:
        _id = Data[0]['id']
        flag = myCol.find_one({"_id": _id})
        if flag is None:
            time = Data[0]['time']
            if Data[0]['type'] == 0:
                content = Data[0]['data']['content']
                doc = {"_id": _id, "time": time, "content": content}
                myCol.insert_one(doc)
                print(_id, time, content)
    except Exception as e:
        print(e)


# 定时爬取数据
def doJob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔1S
    scheduler.add_job(doScheduled, 'interval', max_instances=10, seconds=1)
    scheduler.start()


doJob()
