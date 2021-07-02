# https://699pic.com/
import time

import requests
from bs4 import BeautifulSoup

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Cookie': 'uniqid=5f6d5b7d114ba; search_notice=1; FIRSTVISITED=1601002370.443; from_data=YTo3OntzOjQ6Imhvc3QiO3M6MTA6IjY5OXBpYy5jb20iO3M6Mzoic2VtIjtiOjA7czoxMDoic291cmNlZnJvbSI7aTowO3M6NDoid29yZCI7TjtzOjM6ImtpZCI7aTowO3M6ODoic2VtX3R5cGUiO2k6MDtzOjQ6ImZyb20iO2k6MDt9; recent_number_data_20200927=%81%A8photoNum%A546603; Hm_lvt_ddcd8445645e86f06e172516cac60b6a=1601002370,1601171263; s_token=893cfb3fd7ad8f749c1bd90913c7ab59; Hm_lvt_e37e21a48e66c7bbb5d74ea6f717a49c=1601002370,1601171263; Hm_lpvt_e37e21a48e66c7bbb5d74ea6f717a49c=1601171263; Hm_lvt_1154154465e0978ab181e2fd9a9b9057=1601002371,1601171264; login_view=1; redirect=https%3A%2F%2F699pic.com%2Ftupian-500618976.html; Hm_lpvt_ddcd8445645e86f06e172516cac60b6a=1601171802; Hm_lpvt_1154154465e0978ab181e2fd9a9b9057=1601171802',
    'Host': 'img95.699pic.com',
    'If-Modified-Since': 'Sun, 22 Mar 2020 14:00:25 GMT',
    'If-None-Match': "a3e9c2abb2069d3b1da925453af04a56",
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

html_url = 'https://699pic.com/'
file_path = './shexiangtu'


def get_img_list_box(html_url):
    response = requests.get(html_url)
    response.encoding = None
    result = response.text
    # 再次封装，获取具体标签内的内容
    bs = BeautifulSoup(result, 'html.parser')
    return bs.find_all(attrs={'class': 'imgLibox'})


def down_img(img_list_box, file_path):
    for img_box in img_list_box:
        img = img_box.find('img')
        img_src = img['data-original']
        img_src = "http:" + str(img_src)
        result = requests.get(img_src, headers=header, stream=True)
        if result.status_code == 200:
            t = time.time()
            nowTime = int(round(t * 1000))
            print(nowTime)
            open(file_path + "/" + str(nowTime) + ".png", 'wb').write(result.content)
        del result


list_box = get_img_list_box(html_url)

down_img(list_box, file_path)