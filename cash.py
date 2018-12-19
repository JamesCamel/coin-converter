#coding:utf-8
import requests, json
from bs4 import BeautifulSoup
import re

headers = {
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}
playload = {
'template': '9a-hk',
'Amount': '1',
'From': 'USD',
'To': 'RMB',
'submit': '開始進行貨幣換算'
}
res=requests.post('https://www.xe.com/ucc/convert.cgi', data = playload, headers = headers)
soup = BeautifulSoup(res.text, features='html.parser')
b_tag = soup.find_all('b')
result = b_tag[3].string + " = " + b_tag[5].string
print(result)
# for tag in b_tag:
#     print(tag.string)
#print(b_tag[5].string)
