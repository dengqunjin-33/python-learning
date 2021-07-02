import datetime
import time

from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Chrome()
# 窗口最大化显示
driver.maximize_window()

def buy(buy_time):
    '''
    购买函数

    buy_time:购买时间
    mall:商城类别

    获取页面元素的方法有很多，获取得快速准确又是程序的关键
    在写代码的时候运行测试了很多次，css_selector的方式表现最佳
    '''

    btn_buy = '#J_LinkBuy'
    btn_order = '#submitOrder_1 > div > a'

    while True:
        # 现在时间大于预设时间则开售抢购
        if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') > buy_time:
            try:
                # 找到“立即购买”，点击
                if driver.find_element_by_css_selector(btn_buy):
                    driver.find_element_by_css_selector(btn_buy).click()
                    break
                time.sleep(0.1)
            except:
                time.sleep(0.3)
        else:
            print("校对时间:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    print("==================================下单=======================")
    while True:
        try:
            # 找到“立即下单”，点击，
            if driver.find_element_by_css_selector(btn_order):
                driver.find_element_by_css_selector(btn_order).click()
                # 下单成功，跳转至支付页面
                print("购买成功")
                break
        except:
            if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') > '2021-01-12 20:00:05' :
                break
            else:
                time.sleep(0.5)


if __name__ == "__main__":
    url = 'https://detail.m.tmall.com/item.htm?id=20739895092&hybrid=true&ut_sk=1.XTvQIWFIFcQDAJ11fsm/ov9U_21380790_1610292678904.Copy.1&sourceType=item&price=1499&suid=F9DD3B28-771B-41B6-98DF-186EA2E880C7&shareUniqueId=7021495285&un=6ae3a1fe0543c792acddb6ba99b396ee&share_crt_v=1&spm=a2159r.13376460.0.0&sp_tk=V2NlU2N0V0FaNkc=&cpp=1&shareurl=true&short_name=h.47bqVFS&bxsign=scd3_KOj8VPN4ubpUmmrIlT3bXCq6fNPgXR9cfd1177IHxfeh7D9Jd0gWBMaycALEXYoMnc1Pf-2dL-mtgk84DJr80cQhXABKgoeUvaMuK_IUA&sm=06f341&app=macos_safari&skuId=4227830352490'
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(2)
    #"请输入开售时间【2019-02-15（空格）12:55:50】"
    bt = '2021-01-12 19:59:59'
    buy(bt)