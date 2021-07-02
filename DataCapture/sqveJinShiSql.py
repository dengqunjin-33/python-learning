# 用于解决爬取的数据格式化
import io
import re
import sys
import time
import traceback

import pymysql
import requests
from DBUtils.PooledDB import PooledDB
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup

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
)

# 爬取接口地址
url = "https://flash-api.jin10.com/get_flash_list"

# 爬取数据页面地址(备用)
html_url = 'https://www.jin10.com/example/jin10.com.html'
header = {
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0",
}

queryParam = {
    'vip': 1,
    "channel": "-8200",
}

select_sql = "select * from data as a where a.id = %s "
update_sql = "update data as d set d.status=0 where d.id = %s "

# 记录请求数据接口失败次数
num = 0


def doSave():
    save_info()
    # global num
    # try:
    #     # 连接mysql
    #     my_db = POOL.connection()
    #     my_cursor = my_db.cursor()
    #     curr_time = datetime.now()
    #     queryParam['max_time'] = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    #     responseData = None
    #     try:
    #         responseData = requests.get(url, queryParam, headers=header, timeout=1000).json()
    #         if None is responseData:
    #             num += 1
    #             print("数据接口请求失败！次数:" + str(num))
    #     except:
    #         num += 1
    #         print("数据接口请求失败！次数:" + str(num))
    #     # 超过五次改用请求页面方式
    #     if 5 <= num:
    #         save_info()
    #         return
    #     jinShiJson = responseData['data']
    #     for index in range(0, len(jinShiJson)):
    #         try:
    #             # todo 过滤广告
    #             id = jinShiJson[index]['id']
    #             result = my_cursor.execute(select_sql, id)
    #             if 0 is result:
    #                 saveJinShiData(jinShiJson[index], my_cursor)
    #                 remark = jinShiJson[index]['remark']
    #                 if remark is not None and len(remark) > 0:
    #                     saveJinShiRemark(id, remark, my_cursor)
    #                     my_cursor.execute(update_sql, [id])
    #                 saveJinShiInfo(id, jinShiJson[index]['data'], my_cursor)
    #                 print(jinShiJson[index], flush=True)
    #                 my_db.commit()
    #         except:
    #             my_db.rollback()
    #
    #     my_cursor.close()
    #     my_db.close()
    #     # 为什么要停两秒？爬太快的话容易封
    #     # time.sleep(5)
    # except:
    #     print("发生异常!")


save_data_sql = "insert into data (id,create_time,type,important,tags,channel) values (%s, %s, %s, %s, %s, %s) "


def saveJinShiData(dataJson, my_cursor):
    dataList = []
    keyList = ['id', 'time', 'type', 'important', 'tags', 'channel']
    for index in range(0, len(keyList) - 2):
        dataList.append(dataJson[keyList[index]])
    for i in range(len(keyList) - 2, len(keyList)):
        key = dataJson[keyList[i]]
        if key is not None and len(key) > 0:
            dataList.append(str(key))
        else:
            dataList.append(None)
    ids = dataList[0]
    times = dataList[1].replace('-', '').replace(' ', '').replace(':', '')
    my_cursor.execute(save_data_sql, dataList)
    if times not in ids:
        my_cursor.execute(update_sql, ids)


save_remark_sql = "insert into remark (id, jid, remark_id, link, type, title, content) values(null, %s, " \
                  "%s, %s, %s, " \
                  "%s,%s) "


def saveJinShiRemark(jid, dataJson, my_cursor):
    for jsonIndex in range(0, len(dataJson)):
        json = dataJson[jsonIndex]
        dataList = [jid]
        keyList = ['id', 'link', 'type', 'title', 'content']
        for index in range(0, len(keyList)):
            if keyList[index] in json:
                dataList.append(json[keyList[index]])
            else:
                dataList.append(None)
        my_cursor.execute(save_remark_sql, dataList)


save_info_sql = "insert into info (id,pic,title,content,flag,name,star,type,unit,actual,affect,country," \
                "data_id,measure,revised,previous,pub_time,consensus,time_period,indicator_id) values (%s, %s, %s, " \
                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "


def saveJinShiInfo(id, dataJson, my_cursor):
    keyList = ['pic', 'title', 'content', 'flag', 'name', 'star',
               'type', 'unit', 'actual', 'affect', 'country', 'data_id', 'measure',
               'revised', 'previous', 'pub_time', 'consensus', 'time_period', 'indicator_id']
    dataList = [id]
    for index in range(0, len(keyList)):
        if keyList[index] in dataJson:
            data_str = dataJson[keyList[index]].replace('<b>', '').replace('</b>', '')
            if 'content' is keyList[index]:
                if None is data_str or '' is data_str or '金十' in data_str or 'href=' in data_str or 'src=' in data_str:
                    my_cursor.execute(update_sql, id)
            dataList.append(data_str)
        else:
            dataList.append(None)
    my_cursor.execute(save_info_sql, dataList)


# 以下为备用代码---------------------------
# 根据标签获取新闻集合
def get_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'x-token=; UM_distinctid=173fb069589235-003061a0798d2d-7a1437-100200-173fb06958a202; Hm_lvt_cb3799a5d94664308995d8b999da7944=1597654316,1597717308,1597738004,1599704320; onSound=1; onNotification=2; jinSize=normal; kind_g=%5B%223%22%2C%227%22%5D; trend=1; Hm_lvt_522b01156bb16b471a7e2e6422d272ba=1603767152,1603774966,1603877902,1603881572; Hm_lpvt_522b01156bb16b471a7e2e6422d272ba=1603883573'
        }
    # 请求
    response = requests.get(html_url, headers = headers)
    response.encoding = None
    result = response.text
    # 再次封装，获取具体标签内的内容
    bs = BeautifulSoup(result, 'html.parser')
    list = bs.select('#jin_flash_list > .jin-flash-item-container')
    print("解析后的数据集合------------------------------->>>>>>>>>>>>")
    return list


def save_info():
    # 连接mysql
    my_db = POOL.connection()
    my_cursor = my_db.cursor()
    for data in get_list():
        try:
            # 取ID  #查询这个ID是否存在，如果存在则不进行后续操作
            id = data.get('id').replace('flash', '')
            r = my_cursor.execute(select_sql, id)
            if 0 is not r:
                # print("存在")
                continue
            # print('id为:'+id)
            # 取第一个div
            result = data.select('.jin-flash-item')[0]
            # 判断类包含某个属性
            # if 'is-important' in result.get('class'):
            #     # 包含这个类属性的为金十广告
            #     continue
            if 'flash' in result.get('class'):
                # 取时间
                time_val = time.strftime("%Y-%m-%d", time.localtime()) + ' ' + result.select('.item-time')[0].get_text()
                # 取content   class="right-content"所在div的第一个子节点
                content = result.select('.right-content')[0].contents[0].get_text()
                # 获图片路径
                pic_tag = result.select('.right-pic > .img-container > img')
                pic = None
                if pic_tag is not None and len(pic_tag) > 0:
                    pic = pic_tag[0].get('src')
                print(id + '-' + time_val + '-' + content)
                # 封装data数据 必须按照这个顺序
                data_list = [id, time_val, 0, None, 0, None]
                info_list = [id, pic, None, content, None, None, None, None, None, None,
                             None, None, None, None, None, None, None, None, None, None]
                remark_list = ['jid', 'remark_id', 'link', 'type', 'title', 'content']
                # 执行sql保存
                my_cursor.execute(save_data_sql, data_list)
                my_cursor.execute(save_info_sql, info_list)
                if None is content or '' is content or '金十' in content or 'href=' in content or 'src=' in content:
                    my_cursor.execute(update_sql, id)
            if 'rili' in result.get('class'):
                # 取时间 这里是拼接上了年月日  格式为 2020-xx-xx xx:xx:xx
                time_val = time.strftime("%Y-%m-%d", time.localtime()) + ' ' + result.select('.item-time')[0].get_text()
                # 取国家图片
                country_img = result.select('.country-img')[0].get('src')
                # 取公布时间
                pub_time = time.strftime("%Y-%m-%d", time.localtime()) + ' ' + result.select('.pub-date')[
                    0].get_text() + ':00'
                # 取标题
                name = result.select('.mid-title')[0].get_text()
                # 取前值、预期、公布、修正值
                data_nums = result.select('.data-nums > .num-item')
                previous = None
                consensus = None
                actual = None
                unit = None
                for n in data_nums:
                    if '前值' in n.get_text():
                        previous = re.findall(r'\d+', n.get_text())[0]
                        if '%' in n.get_text():
                            unit = '%'
                    if '预期' in n.get_text():
                        consensus_list = re.findall(r'\d+', n.get_text())
                        if consensus_list is not None and len(consensus_list) > 0:
                            consensus = consensus_list[0]
                    if '公布' in n.get_text():
                        actual_list = re.findall(r'\d+', n.get_text())
                        if actual_list is not None and len(actual_list) > 0:
                            actual = actual_list[0]
                # 取修正值
                revised_str = result.select('.revised-num')
                revised = None
                if revised_str is not None and len(revised_str) > 0:
                    revised_list = re.findall(r'\d+', revised_str[0].get_text())
                    if revised_list is not None and len(revised_list) > 0:
                        revised = revised_list[0]
                jin_star = result.select('.jin-star > .jin-icon')
                i = 0
                for j in jin_star:
                    if '#ddd' in j.get('style'):
                        i = i + 1
                # 取星数
                star = 5 - i
                # print('时间：' + time_val + ',国家图片：' + country_img + ',公布时间:' + pub_time + ',标题：' + name +
                #       ',前值：' + str(previous) + ',预期:' + str(consensus) + ',公布:' + str(actual) + ',修正：' +
                #       str(revised) + '星数：' + str(star), '符号：' + unit)
                # 封装data数据 必须按照这个顺序
                data_list = [id, time_val, 1, None, 0, None]
                info_list = [id, None, None, None, 0, name, star, 0, unit, actual, 0, None, None, None,
                             revised, previous, pub_time, consensus, None, None]
                remark_list = ['jid', 'remark_id', 'link', 'type', 'title', 'content']
                # 执行sql保存
                my_cursor.execute(save_data_sql, data_list)
                my_cursor.execute(save_info_sql, info_list)
            # 提交事务
            my_db.commit()
        except Exception as e:
            # 打印异常信息
            traceback.print_exc()
            # 回滚事务
            my_db.rollback()
    # 关闭资源
    my_cursor.close()
    my_db.close()
    # 为什么要停n秒？爬太快的话容易封
    # time.sleep(5)


# 备用代码结束------------------------------


# 定时爬取数据
def doJob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔5Smax_instances
    scheduler.add_job(doSave, 'interval', seconds=15)
    scheduler.start()


doJob()

# 每n秒执行一次
# def timer(n):
#     while True:
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         doSave()
#         time.sleep(n)
# timer(5)

# def doJob(inc):
#     # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     t = Timer(inc, doSave)
#     t.start()
# # 5s
# doJob(5)
