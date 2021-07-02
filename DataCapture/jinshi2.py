import json
import re
import time

import pymongo
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

url = "https://www.jin10.com/flash_newest.js?"

header = {
    "accept": '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'referer': 'https://www.jin10.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


# 爬取金10数据并处理转换成json串
def doCrawlingJinShi():
    curr_time = time.time()
    queryParam = {"t": curr_time}
    response = requests.get(url, queryParam, headers=header, timeout=100).text
    # 查询第一个等号出现的下标dou'hao
    result = re.search("=", response)
    # 获取下标
    span = result.span()
    string = str(response)
    # 等号后面到导数第二个的范围（倒数第一个是逗号）
    responseList = string[span[-1]:-1]
    return json.loads(responseList)


def saveJinShiData():
    jinShiJson = doCrawlingJinShi()

    # 创建连接
    myClient = pymongo.MongoClient(' ')

    # 连接数据库
    myDb = myClient['dqj_jinshidata']

    # 连接表
    myCol = myDb['jinshinews']

    for index in range(0, len(jinShiJson)):
        _id = jinShiJson[index]['id']
        print(_id)
        flag = myCol.find_one({"_id": _id})
        if flag is None:
            keyList = ['id', 'time', 'type', 'data', 'important', 'tags', 'channel', 'remark']
            doc = {'_id': jinShiJson[index]['id']}
            for i in range(0, len(keyList)):
                doc[keyList[i]] = jinShiJson[index][keyList[i]]
            print(doc)
            myCol.insert_one(doc)


# 定时爬取数据
def doJob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔1S
    scheduler.add_job(saveJinShiData(), 'interval', max_instances=10, seconds=1)
    scheduler.start()


doJob()
