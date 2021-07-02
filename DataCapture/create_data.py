# 用于解决爬取的数据格式化
import io
import json
import os
import sys
import time
import urllib

import requests
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/73.0.3683.86 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

sum_img = 0


def get_list(keyword, file_path, num):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    search_name = urllib.parse.quote(keyword)
    index = num // 30
    if index is 0:
        down_load_img(search_name, file_path, num)
    else:
        for i in range(1, index+1):
            pn = 30 * i
            down_load_img(search_name, file_path, pn)
            if i == index and pn <= num:
                down_load_img(search_name, file_path, num)


def down_load_img(search_name, file_path, pn):
    header.pop('Referer', 'https://image.baidu.com/search/index?&word=' + str(search_name))
    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord=' + str(
        search_name) + '&cl=2&lm=-1&ie=utf-8&oe=utf-8&word=' + str(search_name) + '&nc=1&pn=' + str(pn) + '&rn=30&gsm' \
                                                                                                          '=1e '
    response = requests.get(url, headers=header, allow_redirects=False)
    response.encoding = None
    result = response.text
    bs = BeautifulSoup(result, 'html.parser')
    json_data = json.loads(bs.text)
    data_list = json_data['data']
    for data in data_list:
        if 'thumbURL' in data:
            result = requests.get(data['thumbURL'], headers=header, stream=True)
            if result.status_code == 200:
                t = time.time()
                nowTime = int(round(t * 1000))
                print(nowTime, flush=True)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                open(file_path + "/" + str(nowTime) + ".png", 'wb').write(result.content)  # 将内容写入图片
            del result


get_list('飞鸟斋藤', "./feiniao", 120)
