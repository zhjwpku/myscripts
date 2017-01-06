#!/usr/bin/python
#coding:utf8
# before running this script, do:
#   sudo pip install twilio
#   sudo pip install selenium
# on some distro, you will need to install geckodriver
#   wget https://github.com/mozilla/geckodriver/releases/download/v0.12.0/geckodriver-v0.12.0-linux64.tar.gz
#   tar -C /usr/local/bin -xmf geckodriver-v0.12.0-linux64.tar.gz
# usage:
#   ./alter_with_twilio.py 2&>1 &

from twilio.rest import TwilioRestClient
from selenium import webdriver
import os
import time

account_sid = os.environ['TW_SID']
auth_token = os.environ['TW_TK']
num_to = os.environ['MY_PHONE_NUM']
num_from = os.environ['TW_NUM']

time_interval = 30

def sendmessage(msg):
    client = TwilioRestClient(account_sid, auth_token)
    try:
        message = client.messages.create(body=msg,
            to = num_to,
            from_ = num_from)
        print("Send Msg Success. "+ message.sid)
    except TwilioRestException as e:
        print(e)

def check_product():
    url = "http://item.mi.com/buy/air2"
    browser = webdriver.Firefox()
    browser.get(url)
    elem = browser.find_element_by_id("J_chooseResultInit")
    res = elem.is_displayed()
    browser.quit()
    return res

if __name__ == '__main__':
    while True:
        if check_product():
            sendmessage("小米空气净化器有货啦！")
        # try every half an hour
        time.sleep(30*60)
