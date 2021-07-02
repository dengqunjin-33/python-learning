# 自相关分析
from typing import Any, Union

import pandas as pd
import pymysql
from pymysql.cursors import Cursor

conn = pymysql.connect(host='58.67.156.39',
                       port=6033,
                       user='jiyu',
                       password='jiyu',
                       database='mw_aitrade',
                       charset='utf8')

search_list = ['0', '30']

# 自相关 autocorrelation
btc_seach_sql = "select * from ex_scale_kline_btcusdt where id > %s and id <= %s"

eth_seach_sql = "select * from ex_scale_kline_ethusdt where id > %s and id <= %s"

cursor: Union[Cursor, Any] = conn.cursor()
cursor.execute(btc_seach_sql, search_list)
btc_all_data = cursor.fetchall()
result = []
data_list = []
for data in btc_all_data:
    data_list.append([float(data[3]),
                      float(data[4]),
                      float(data[5]),
                      float(data[6]),
                      float(data[7]),
                      float(data[8])])

column_lst = ['amount', 'vol', 'open', 'close', 'high', 'low']

data_dict = {}  # 创建数据字典，为生成Dataframe做准备
for col, gf_lst in zip(column_lst, data_list):
    data_dict[col] = gf_lst

unstrtf_df = pd.DataFrame(data_dict)
cor1 = unstrtf_df.corr()  # 计算相关系数，得到一个矩阵
print(cor1)
