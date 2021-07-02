from typing import Any, Union

import matplotlib.pyplot as plt
import pymysql
from pymysql.cursors import Cursor

table_dict = {'amount': 3, 'vol': 4, 'open': 5, 'close': 6, 'high': 7, 'low': 8, }

conn = pymysql.connect(host=' ',
                       port= 55555,
                       user=' ',
                       password=' ',
                       database=' ',
                       charset=' ')


def getDataList(search_sql: str, search_list: list, field: int):
    cursor: Union[Cursor, Any] = conn.cursor()
    cursor.execute(search_sql, search_list)
    all_data = cursor.fetchall()
    data_y = []
    for data in all_data:
        data_y.append(data[field])
    return data_y


def getSqlByTableName(table_name: str):
    return "select * from " + table_name + " limit %s,%s"


if __name__ == '__main__':
    btc = "ex_scale_kline_btcusdt"
    eth = "ex_scale_kline_ethusdt"

    plt.subplot(6, 2, 1)
    data_y = getDataList(getSqlByTableName(btc), [220, 30], table_dict['amount'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 2)
    data_y = getDataList(getSqlByTableName(eth), [220, 30], table_dict['amount'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 3)
    data_y = getDataList(getSqlByTableName(btc), [220, 30], table_dict['vol'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 4)
    data_y = getDataList(getSqlByTableName(eth), [220, 30], table_dict['vol'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 5)
    data_y = getDataList(getSqlByTableName(btc), [220, 30], table_dict['open'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 6)
    data_y = getDataList(getSqlByTableName(eth), [220, 30], table_dict['open'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 7)
    data_y = getDataList(getSqlByTableName(btc), [220, 30], table_dict['close'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 8)
    data_y = getDataList(getSqlByTableName(eth), [220, 30], table_dict['close'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 9)
    data_y = getDataList(getSqlByTableName(btc), [220, 30], table_dict['high'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 10)
    data_y = getDataList(getSqlByTableName(eth), [220, 30], table_dict['high'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 11)
    data_y = getDataList(getSqlByTableName(btc), [220, 30], table_dict['low'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.subplot(6, 2, 12)
    data_y = getDataList(getSqlByTableName(eth), [220, 30], table_dict['low'])
    plt.plot(range(1, len(data_y) + 1), data_y)
    plt.legend()
    plt.show()

