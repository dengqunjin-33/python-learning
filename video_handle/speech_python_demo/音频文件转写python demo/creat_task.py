#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import time

import requests

IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode

    timer = time.perf_counter
else:
    from urllib import urlopen
    from urllib import Request
    from urllib import URLError
    from urllib import urlencode

    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# 填写百度控制台中相关开通了“音频文件转写”接口的应用的的API_KEY及SECRET_KEY
API_KEY = '****'
SECRET_KEY = '****'

"""  获取请求TOKEN start 通过开通音频文件转写接口的百度应用的API_KEY及SECRET_KEY获取请求token"""


class DemoError(Exception):
    pass


TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
# SCOPE = 'brain_bicc'  # 有此scope表示有asr能力，没有请在网页里勾选 bicc
SCOPE = 'brain_asr_async'  # 有此scope表示有asr能力，没有请在网页里勾选


# SCOPE = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里勾选

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if IS_PY3:
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if IS_PY3:
        result_str = result_str.decode()

    #    print(result_str)
    result = json.loads(result_str)
    #    print(result)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        #        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  获取鉴权结束，TOKEN end """

"""  发送识别请求 """

# 待进行语音识别的音频文件url地址，需要可公开访问。建议使用百度云对象存储（https://cloud.baidu.com/product/bos.html）
speech_url_list = [
    "https://platform.bj.bcebos.com/sdk%2Fasr%2Fasr_doc%2Fdoc_download_files%2F16k.pcm",
]

for speech_url in speech_url_list:
    url = 'https://aip.baidubce.com/rpc/2.0/aasr/v1/create'  # 创建音频转写任务请求地址

    body = {
        "speech_url": speech_url,
        "format": "pcm",  # 音频格式，支持pcm,wav,mp3，音频格式转化可通过开源ffmpeg工具（https://ai.baidu.com/ai-doc/SPEECH/7k38lxpwf）或音频处理软件
        "pid": 1537,  # 模型pid，1537为普通话输入法模型，1737为英语模型
        "rate": 16000  # 音频采样率，支持16000采样率，音频格式转化可通过开源ffmpeg工具（https://ai.baidu.com/ai-doc/SPEECH/7k38lxpwf）或音频处理软件
    }

    token = {"access_token": fetch_token()}

    headers = {'content-type': "application/json"}

    response = requests.post(url, params=token, data=json.dumps(body), headers=headers)

    # 返回请求结果信息，获得task_id，通过识别结果查询接口，获取识别结果
    print(response.text)
