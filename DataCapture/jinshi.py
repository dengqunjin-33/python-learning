import datetime

import pymongo
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

# 创建连接
myClient = pymongo.MongoClient(' ')

# 连接数据库
myDb = myClient['dqj_jinshidata']

# 连接表
myCol = myDb['jinshinews']

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


def saveJinShiData():
    curr_time = datetime.datetime.now()
    queryParam['max_time'] = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    responseData = requests.get(url, queryParam, headers=header, timeout=100).json()
    jinShiJson = responseData['data']

    for index in range(0, len(jinShiJson)):
        # j_id = jinShiJson[index]['id']
        # j_time = jinShiJson[index]['time']
        # j_type = jinShiJson[index]['type']
        # j_data = jinShiJson[index]['data']
        # j_important = jinShiJson[index]['important']
        # j_tags = jinShiJson[index]['tags']
        # j_channel = jinShiJson[index]['channel']
        # j_remark = jinShiJson[index]['remark']
        # jinShi = JinShi(j_id, j_time, j_type, j_data, j_important, j_tags, j_channel, j_remark)
        _id = jinShiJson[index]['id']
        flag = myCol.find_one({"_id": _id})
        if flag is None:
            keyList = ['id', 'time', 'type', 'data', 'important', 'tags', 'channel', 'remark']
            doc = {'_id': jinShiJson[index]['id']}
            for i in range(0, len(keyList)):
                doc[keyList[i]] = jinShiJson[index][keyList[i]]
            print(doc)
            myCol.insert_one(doc)
            # for i in range(0, len(keyList)):
            #     doc[keyList[i]] = jinShiJson[index][keyList[i]]


# 获取金10数据里面的remark转换成python对象
def getRemarkList(remarkJson):
    remark_list = []
    for remarkData in remarkJson:
        keyList = ['id', 'link', 'type', 'title', 'content']
        dist = getDistByJson(keyList, remarkData)
        remark = JinShiRemark(dist[keyList[0]], dist[keyList[1]], dist[keyList[2]], dist[keyList[3]], dist[keyList[4]])
        remark_list.append(remark)
    return remark_list


# 获取金十数据里面的data封装成python对象
def getJinShiInfo(dataJson):
    if 'pic' in dataJson or 'title' in dataJson or 'content' in dataJson:
        keyList = ['pic', 'title', 'content']
        dist = getDistByJson(keyList, dataJson)
        return JinShiData(dist[keyList[0]], dist[keyList[1]], dist[keyList[2]])
    else:
        keyList = ['flag', 'name', 'star', 'type', 'unit', 'actual', 'affect', 'country', 'data_id',
                   'measure', 'revised', 'previous', 'pub_time', 'consensus', 'time_period', 'indicator_id']
        dist = getDistByJson(keyList, dataJson)
        return JinShiData(dist[keyList[0]], dist[keyList[1]], dist[keyList[2]], dist[keyList[3]],
                          dist[keyList[4]], dist[keyList[5]], dist[keyList[6]], dist[keyList[7]],
                          dist[keyList[8]], dist[keyList[9]], dist[keyList[10]], dist[keyList[11]],
                          dist[keyList[12]], dist[keyList[13]], dist[keyList[14]], dist[keyList[15]])


# Json转换成字典
def getDistByJson(keyList, jsonData):
    dist = {}
    for keyIndex in range(0, len(keyList)):
        key = keyList[keyIndex]
        dist[key] = None
        if key in jsonData:
            dist[key] = jsonData[key]
    return dist


class JinShiData(object):
    def __init__(self, j_id, j_time, j_type, j_important, j_tags, j_channel):
        self.id = j_id
        self.time = j_time
        self.type = j_type
        self.important = j_important
        self.tags = j_tags
        self.channel = j_channel


class JinShiInfo(object):
    def __init__(self,
                 j_id=None,
                 j_pic=None,
                 j_title=None,
                 j_content=None,
                 ):
        self.id = j_id
        self.pic = j_pic
        self.title = j_title
        self.content = j_content

    def __init__(self,
                 j_id=None,
                 j_flag=None,
                 j_name=None,
                 j_star=None,
                 j_type=None,
                 j_unit=None,
                 j_actual=None,
                 j_affect=None,
                 j_country=None,
                 j_data_id=None,
                 j_measure=None,
                 j_revised=None,
                 j_previous=None,
                 j_pub_time=None,
                 j_consensus=None,
                 j_time_period=None,
                 j_indicator_id=None):
        self.id = j_id
        self.flag = j_flag,
        self.name = j_name,
        self.star = j_star,
        self.type = j_type,
        self.unit = j_unit,
        self.actual = j_actual,
        self.affect = j_affect,
        self.country = j_country,
        self.dataId = j_data_id,
        self.measure = j_measure,
        self.revised = j_revised,
        self.previous = j_previous,
        self.pubTime = j_pub_time,
        self.consensus = j_consensus,
        self.timePeriod = j_time_period,
        self.indicatorId = j_indicator_id


class JinShiRemark(object):
    def __init__(self,
                 j_id=None,
                 j_link=None,
                 j_type=None,
                 j_title=None,
                 j_content=None,
                 ):
        self.jid = j_id
        self.link = j_link
        self.type = j_type
        self.title = j_title
        self.content = j_content


# 定时爬取数据
def doJob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔1S
    scheduler.add_job(saveJinShiData, 'interval', max_instances=10, seconds=1)
    scheduler.start()


if __name__ == '__main__':
    doJob()
