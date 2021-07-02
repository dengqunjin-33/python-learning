from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome = webdriver.Chrome()

chrome.get("https://www.91didilf.cc/")

sleep(2)

try:
    search_keywords = chrome.find_element_by_id('search-keywords')
    search_keywords.send_keys("西乡塘")
    search_keywords.send_keys(Keys.RETURN)
    bs = BeautifulSoup(chrome.page_source, 'html.parser')
    placeholders = bs.select('.placeholder a')
    for item in placeholders:
    # item = placeholders[2]
        url = item['href']
        chrome.get(url=url)
        bs = BeautifulSoup(chrome.page_source, 'html.parser')
        quotes = bs.select('article')
        if not len(quotes) == 0:
            print(quotes[0])
        sleep(1)
except Exception as err:
    print("发生异常!", err)

sleep(5)
chrome.quit()
