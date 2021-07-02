import os
import threading

import pymongo

myClient = pymongo.MongoClient('')

accountDb = myClient['f_account']

orderDb = myClient['f_order']

userDb = myClient['f_user']

orderOpenTmpCol = accountDb['order_open_tmp']

orderOpenIndexCol = accountDb['order_open_Index']

orderopenimplCol = accountDb['orderopenimpl']

accountopendetailsimplCol = accountDb['accountopendetailsimpl']

orderCol = orderDb['orderimpl']

userCol = userDb['simpleuser']


class MyThread(threading.Thread):
    def __init__(self, threadID, myStart, myCount, myPathValue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.myStart = myStart
        self.myCount = myCount
        self.myPathValue = myPathValue

    def run(self):
        print("开启线程：" + self.threadID)
        compareDate(self.myStart, self.myCount, self.myPathValue)


def compareDate(start, count, pathValue):
    dataList = orderOpenTmpCol.find().skip(start).limit(count).sort([("_id", pymongo.DESCENDING)])
    for data in dataList:
        _id = data['_id']

        _id = orderOpenIndexCol.find_one({'_id': _id})['_id']

        _id = orderopenimplCol.find_one({'_id': _id})['_id']

        _id = accountopendetailsimplCol.find_one({'_id': _id})['_id']

        order = orderCol.find_one({'_id': _id})
        vo = order['vo']
        mt_login = vo['mt_login_id']
        user = userCol.find_one({'mt_login_id': mt_login})
        if not os.path.isfile(pathValue):  # 无文件时创建
            fd = open(pathValue, mode="w", encoding="utf-8")
            fd.close()
        with open(pathValue, 'a') as f:
            print(user, file=f)
            print(_id, file=f)


if __name__ == '__main__':
    threadList = ['1', '2', '3']
    startList = [1000, 2000, 3000]
    dataCount = 1000
    pathList = ["C:/Users/11469/Desktop/log1.txt", "C:/Users/11469/Desktop/log2.txt", "C:/Users/11469/Desktop/log3.txt"]
    for index in range(0, len(threadList)):
        runThread = MyThread(threadList[index], myStart=startList[index], myCount=dataCount, myPathValue=pathList[index])
        runThread.start()
