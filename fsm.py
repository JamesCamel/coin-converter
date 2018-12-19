from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url, send_button_message
import requests
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}
playload = {
    'template': '9a-hk',
    'Amount': '',
    'From': '',
    'To': '',
    'submit': '開始進行貨幣換算'
}
cashOptions = ["美金", "新台幣", "美元", "台幣", "港元", "港幣",
               "人民幣", "英鎊", "歐元", "加元", "日圓", "日幣", "日元", "澳幣", "澳元"]

graphOptions=[ "澳幣", "澳元", "英鎊", "日圓","日幣","日元","人民幣","歐元","加元","加幣"]
cashGraph = {"url":""}

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
    
    def is_going_to_guide(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text != "貨幣換算" and text!= "匯率走勢"
        return False

    def is_going_to_cashSource(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text == '貨幣換算'
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state2'
        return False

    def is_going_to_cashAmount(self, event):
        if event.get("message"):
            text = event['message']['text']
            playload['From'] = toEn(text)
            for cash in cashOptions:
                if text == cash:
                    return True
        return False

    def is_going_to_cashDest(self, event):
        if event.get("message"):
            text = event['message']['text']
            playload['Amount'] = text
            for amount in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if text[0] == amount:
                    return True
        return False

    def is_going_to_requestData(self, event):
        if event.get("message"):
            text = event['message']['text']
            playload['To'] = toEn(text)
            for cash in cashOptions:
                if text == cash:
                    return True
        return False
    
    def is_going_to_pickGraph(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text == '匯率走勢'
        return False

    def is_going_to_showGraph(self, event):
        if event.get("message"):
            text = event['message']['text']
            cashGraph["url"] = toURL(text)
            for graph in graphOptions:
                if text == graph:
                    return True
        return False

    #####        on_enter_state     #####


    def on_enter_guide(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入貨幣換算或匯率走勢啦")
        self.go_back()

    
        
    def on_enter_cashSource(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "輸入待轉貨幣")
    
        # buttons = [
        #     {
        #         "type": "postback",  #postback web_url
        #         #"url": "https://www.messenger.com",
        #         "title": "美金",
        #         "payload": "美金"
        #     }
        # ]
        # send_button_message(sender_id, "fdd", buttons)
        # text = event['message']['text']
        # playload['from'] = toEn(text)
        # print(playload['from'])

        # sourceFlag = text
        # self.go_back()

    # def on_exit_cashSource(self):
    #     print('Leaving state1')


    def on_enter_cashAmount(self, event):

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "輸入轉換金額")
        
        #send_image_url(sender_id, getGraphURL(toURL("澳幣")))
        # self.go_back()

    # def on_exit_cashAmount(self):
    #     print('Leaving state1')

    def on_enter_cashDest(self, event):

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "輸入目標貨幣")
        # self.go_back()

    

    def on_enter_requestData(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, getRequestResult(playload))
        self.go_back()

    def on_enter_pickGraph(self, event):

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "你是想看什麼貨幣的趨勢ㄏㄚˋ")
        #self.go_back()
    
    def on_enter_showGraph(self, event):
        print("enter showGraph\n\n\n\n")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "這是它對美金的實時匯率走勢")
        send_image_url(sender_id, getGraphURL(cashGraph["url"]))
        #send_image_url(sender_id, getGraphURL(toURL("澳幣")))
        self.go_back()

    def on_exit_showGraph(self):
        print('leaving_showGraph')

def getRequestResult(playload):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    res = requests.post('https://www.xe.com/ucc/convert.cgi',
                        data=playload, headers=headers)
    soup = BeautifulSoup(res.text, features='html.parser')
    b_tag = soup.find_all('b')
    result = b_tag[3].string + " = " + b_tag[5].string
    return result

def getGraphURL(url):
    options = Options()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(url)  # 輸入範例網址，交給瀏覽器 
    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource, 'html.parser')
    img = soup.find(id = 'chart_img')#
    driver.close()
    return str(img['src'])

def toEn(ch):
    if ch == "美金" or ch == "美元":
        return "USD"
    elif ch == "新台幣" or ch == "台幣":
        return "TWD"
    elif ch == "港元" or ch == "港幣":
        return "HKD"
    elif ch == "人民幣":
        return "RMB"
    elif ch == "英鎊":
        return "GBP"
    elif ch == "歐元":
        return "EUR"
    elif ch == "加元":
        return "CAD"
    elif ch == "日圓" or ch == "日幣" or ch == "日元":
        return "JPY"
    elif ch == "澳幣" or ch == "澳元":
        return "AUD"

def toURL(ch):
    if ch == "澳幣" or ch == "澳元":
        return "http://www.kitco.cn/hk/charts/precious-metals-trend/24hr-major-currency-us-dollar.html?currency=aud&timePeriod=d&flag=exchangeRate&otherChart=no"
    elif ch == "英鎊":
        return "http://www.kitco.cn/hk/charts/precious-metals-trend/24hr-major-currency-us-dollar.html?currency=gbp&timePeriod=d&flag=exchangeRate&otherChart=no"
    elif ch == "人民幣":
        return "http://www.kitco.cn/hk/charts/precious-metals-trend/24hr-major-currency-us-dollar.html?currency=cny&timePeriod=d&flag=exchangeRate&otherChart=no"
    elif ch == "歐元":
        return "http://www.kitco.cn/hk/charts/precious-metals-trend/24hr-major-currency-us-dollar.html?currency=euro&timePeriod=d&flag=exchangeRate&otherChart=no"
    elif ch == "日圓" or ch == "日幣" or ch == "日元":
        return "http://www.kitco.cn/hk/charts/precious-metals-trend/24hr-major-currency-us-dollar.html?currency=jpy&timePeriod=d&flag=exchangeRate&otherChart=no"
    elif ch == "加元" or ch == "加幣":
        return "http://www.kitco.cn/hk/charts/precious-metals-trend/24hr-major-currency-us-dollar.html?currency=jpy&timePeriod=d&flag=exchangeRate&otherChart=no"
    
