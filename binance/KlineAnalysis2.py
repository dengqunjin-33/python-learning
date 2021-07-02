# 线相关分析
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql
from pymysql.cursors import Cursor

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False

conn = pymysql.connect(host='',
                       port=6379,
                       user='',
                       password='',
                       database='',
                       charset='utf8')

table_dict = {'amount': 3, 'vol': 4, 'open': 5, 'close': 6, 'high': 7, 'low': 8, }


def getDataList(search_sql: str, search_list: list, field: int):
    cursor: Union[Cursor, Any] = conn.cursor()
    cursor.execute(search_sql, search_list)
    all_data = cursor.fetchall()
    data_list = []
    for data in all_data:
        data_list.append(float(data[field]))
    return data_list


def getBatchCorrelationCoefficient(table_sql_1: str, table_sql_2: str, start: int, step: int):
    corrcoef_dict = {}
    k = 1
    for field in table_dict:
        field_list = []
        table1_data = getDataList(getSqlByTableName(table_sql_1), [start, step], table_dict[field])
        table2_data = getDataList(getSqlByTableName(table_sql_2), [start + k, step], table_dict[field])
        p = np.corrcoef(table1_data, table2_data)
        field_list.append(p[0][1])
        if p[0][1] < 0:
            print(field, '错误')
        corrcoef_dict[field] = field_list
    return pd.DataFrame(corrcoef_dict)


def getSqlByTableName(table_name: str):
    return "select * from " + table_name + " limit %s,%s"


def printInfo(array: list, filed: str):
    print("-------------------------" + filed + "开始-------------------------------")
    print("每组相关系数：", array)
    print("最大值：", max(array))
    print("最小值：", min(array))
    print("极差：", max(array) - min(array))
    print("平均相关系数：" + str(np.array(array).mean()))
    print("-------------------------" + filed + "结束-------------------------------")


def plotImage(array: list, title: str, i: int):
    plt.subplot(i)
    plt.plot(range(1, len(array) + 1), array, c='blue', label=(title + "-corrcoef"))
    plt.axhline(np.array(array).mean(), c='red', label=(title + "-corrcoef-average"))
    plt.title(title + '相关系数分析')
    plt.legend()


def getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, start, end, step):
    for i in range(start, end, step):
        print("---------------" + str(i) + "----------------")
        corrcoef = getBatchCorrelationCoefficient(btc, eth, i, step)
        high_array.append(corrcoef['high'].mean())
        amount_array.append(corrcoef['amount'].mean())
        vol_array.append(corrcoef['vol'].mean())
        open_array.append(corrcoef['open'].mean())
        low_array.append(corrcoef['low'].mean())
        close_array.append(corrcoef['close'].mean())


if __name__ == '__main__':
    btc = "ex_scale_kline_btcusdt"
    eth = "ex_scale_kline_ethusdt"
    # 每一批的相关系数
    high_array = []
    amount_array = []
    vol_array = []
    open_array = []
    close_array = []
    low_array = []

    getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, 0, 140, 10)
    getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, 160, 360, 10)
    getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, 385, 705, 10)
    getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, 720, 880, 10)
    # 910-990
    getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, 909, 989, 10)

    # 991-1208
    getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, 990, 1200, 10)
    # 1209-1400
    getCorrcoefListForRange(amount_array, vol_array, open_array, close_array, high_array, low_array, 1210, 1350, 10)

    printInfo(amount_array, 'amount')
    printInfo(vol_array, 'vol')
    printInfo(open_array, 'open')
    printInfo(close_array, 'close')
    printInfo(high_array, 'high')
    printInfo(low_array, 'low')

    plotImage(amount_array, 'amount', 321)
    plotImage(vol_array, 'vol', 322)
    plotImage(open_array, 'open', 323)
    plotImage(close_array, 'close', 324)
    plotImage(high_array, 'high', 325)
    plotImage(low_array, 'low', 326)
    plt.show()




