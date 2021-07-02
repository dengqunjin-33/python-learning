# from datetime import datetime
import datetime
# 用于解决爬取的数据格式化
import io
import json
import sys
from time import sleep

import pymysql
import requests
from DBUtils.PooledDB import PooledDB
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
from selenium import webdriver

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# https://blog.csdn.net/yyangjun/article/details/88716575 代理爬虫博客地址
# 数据库连接池
POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=5,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # host='139.159.244.194',
    # port=3306,
    # user='root',
    # password='abc123456@',
    # database='jinshi',
    host='58.67.156.39',
    port=6033,
    user='jiyu',
    password='jiyu',
    database='exchange_otc',
    charset='utf8'
)

# 爬取接口地址
url = "https://cdn-rili.jin10.com/data/"

header = {
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0",
}

save_calendar_sql = "insert into rili (id, day_time,country, time_period, name, unit, previous," \
                    "consensus, actual, affect, revised, indicator_id, star, pub_time) " \
                    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

calendar_field = ['id', 'day_time', 'country', 'time_period', 'name', 'unit', 'previous', 'consensus', 'actual',
                  'affect', 'revised', 'indicator_id', 'star', 'pub_time']

select_calendar_sql = "select id from rili where id = %s"

update_calendar_sql = "update rili set day_time = %s, country = %s, time_period = %s, name = %s, unit = %s, previous = %s, " \
                      "consensus = %s, actual = %s, affect = %s, revised = %s, indicator_id = %s, star = %s, pub_time = %s where id = %s"


# 几分钟更新一次数据
def getNowData():
    print("数据刷新保存", flush=True)
    getDataByAddDay(add_day=0)


# 每天更新一次
def getTwoWeekData():
    for add_day in range(1, 15):
        sleep(0.9)
        print("保存" + str(add_day) + "天后的数据", flush=True)
        getDataByAddDay(add_day=add_day)


# 通过值获取要添加的天数
def getDataByAddDay(add_day):

    global num
    # 连接mysql
    my_db = POOL.connection()
    my_cursor = my_db.cursor()
    curr_time = datetime.datetime.now()
    day_time = curr_time + datetime.timedelta(days=add_day)
    day_year = str(day_time.year)
    day_day = day_time.strftime('%m%d')
    query_url = url + day_year + '/' + day_day + '/economics.json'

    # 合成十三位时间戳
    query_param = {"_": curr_time.timestamp()}
    try:
        response_data = None
        try:
            response_data = requests.get(query_url, query_param, headers=header, timeout=1000).json()
        except Exception as err:
            print("直接请求数据接口失败！", err, flush=True)

        if None is response_data:
            print("直接请求数据接口失败！改用谷歌浏览器获取接口信息！")
            # 打开浏览器
            chrome = webdriver.Chrome()
            try:
                # 浏览器访问这个页面
                chrome.get(query_url + "?_=" + str(curr_time.timestamp()))
                sleep(3)
                bs = BeautifulSoup(chrome.page_source, 'html.parser')
                pre = bs.find('pre')
                pre_text = pre.text
                response_data = json.loads(pre_text)
            except Exception as err:
                print("直接请求数据接口失败！", err, flush=True)
            finally:
                # 浏览器关闭
                chrome.quit()

        for data in response_data:
            data_list = []
            for fieldIndex in range(0, len(calendar_field) - 1):
                if fieldIndex == 1:
                    day_time_field = day_time.strftime('%Y-%m-%d')
                    data_list.append(day_time_field)
                else:
                    field = calendar_field[fieldIndex]
                    if field in data:
                        data_list.append(data[field])
                    else:
                        print("字段不存在,字段名称为:【" + field + "】", flush=True)
            # utc时间转datetime时间
            if calendar_field[len(calendar_field) - 1] in data:
                pub_time = data[calendar_field[len(calendar_field) - 1]]
                utc_pub_time = datetime.datetime.strptime(pub_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                data_list.append(utc_pub_time)

            # 查找当前数据是否存在
            my_cursor.execute(select_calendar_sql, data[calendar_field[0]])
            rest = my_cursor.fetchone()
            # 不存在 插入
            if rest is None:
                my_cursor.execute(save_calendar_sql, data_list)
            # 数据存在->更新
            else:
                data_list.remove(data[calendar_field[0]])
                data_list.append(data[calendar_field[0]])
                my_cursor.execute(update_calendar_sql, data_list)
            my_db.commit()
    except Exception as e:
        try:
            my_db.rollback()
        except Exception as err:
            print("保存信息回滚时发生异常!吔屎啦你！", err, flush=True)
        print("保存信息时发生异常!", e, flush=True)
    return


def doJob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔1分钟
    scheduler.add_job(getNowData, 'cron', minute='*/2', max_instances=10)
    scheduler.add_job(getTwoWeekData, 'cron', minute="*/7", max_instances=10)
    scheduler.start()


if __name__ == '__main__':
    doJob()
