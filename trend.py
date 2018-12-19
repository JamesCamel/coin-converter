#coding:utf-8
import requests, json
from bs4 import BeautifulSoup
import re
from selenium import webdriver

driver = webdriver.Chrome('/Users/james/Downloads/chromedriver')  # PhantomJs
driver.get('http://www.kitco.cn/hk/charts/precious-metals-trend/24hr-major-currency-us-dollar.html?currency=aud&timePeriod=d&flag=exchangeRate&otherChart=no')  # 輸入範例網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'html.parser')
img = soup.find(id = 'chart_img')
print(img['src'])
driver.close()


# for tag in b_tag:
#     print(tag.string)
#print(b_tag[5].string)
